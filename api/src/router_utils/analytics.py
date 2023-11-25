from datetime import datetime
import plotly.graph_objects as go
from pydantic import BaseModel
from typing import List, Dict, Any, Callable
from uuid import UUID

from .. import models, config, io_operations


class FileMetric(BaseModel):
    primary_id: UUID
    file_id: UUID
    user_email: str
    project_name: str
    file_path: str
    file_size: int
    loc: int
    extension: str
    content: str
    session_id: UUID
    timestamp: datetime
    metric: str
    score: int
    reasoning: str


class AggFileMetric(BaseModel):
    file_path: str
    loc: int
    scores: List[float]


class KeyFile(BaseModel):
    file_path: str
    contrib_percent: float
    score: float


class GroupMetrics(BaseModel):
    score: float
    key_files: List[KeyFile]


GroupedMetrics = Dict[str, Dict[datetime, List[FileMetric]]]
WeightedMetrics = Dict[str, Dict[datetime, GroupMetrics]]


def join_files_metrics(
    metrics: list[models.Metric], files: Dict[UUID, models.File]
) -> list[FileMetric]:
    joined_data = []
    for metric in metrics:
        file = files[metric.file_id]
        joined_data.append({**metric.model_dump(), **file.model_dump()})
    return [FileMetric(**data) for data in joined_data]


def group_metrics(file_metrics: List[FileMetric]) -> GroupedMetrics:
    grouped_metrics = {}
    for file_metric in file_metrics:
        if file_metric.metric not in grouped_metrics:
            grouped_metrics[file_metric.metric] = []
        grouped_metrics[file_metric.metric].append(file_metric)

    for metric_name, file_metrics_group in grouped_metrics.items():
        dates = {}
        for file_metric in file_metrics_group:
            date = file_metric.timestamp.date()
            if date not in dates:
                dates[date] = []
            dates[date].append(file_metric)
        grouped_metrics[metric_name] = dates
    return grouped_metrics


def group_calc_helper(aggregated_file_metrics: List[AggFileMetric]) -> GroupMetrics:
    total_loc = sum(file_metric.loc for file_metric in aggregated_file_metrics)
    weighted_score = 0
    key_files = []
    for aggregated_file_metric in aggregated_file_metrics:
        contrib_percent = aggregated_file_metric.loc / total_loc
        score = sum(aggregated_file_metric.scores) / len(aggregated_file_metric.scores)
        weighted_score += score * contrib_percent
        key_files.append(
            KeyFile(
                file_path=aggregated_file_metric.file_path,
                contrib_percent=contrib_percent * 100,
                score=score,
            )
        )

    key_files = sorted(key_files, key=lambda x: x.contrib_percent, reverse=True)[:8]
    return {"score": weighted_score, "key_files": key_files}


def aggregate_file_metrics(file_metrics: List[FileMetric]) -> List[AggFileMetric]:
    """Aggregate file metrics by file path, and calculate a weighted score"""
    agg_file_metrics = {}
    for file_metric in file_metrics:
        if file_metric.file_path not in agg_file_metrics:
            agg_file_metrics[file_metric.file_path] = AggFileMetric(
                file_path=file_metric.file_path, loc=file_metric.loc, scores=[]
            )
        agg_file_metrics[file_metric.file_path].scores.append(file_metric.score)
    return list(agg_file_metrics.values())


def calculate_weighted_metrics(grouped_metrics: GroupedMetrics) -> WeightedMetrics:
    """Orchestrate the calculation of weighted metrics for each metric type."""
    weighted_metrics = {}
    for metric, dates in grouped_metrics.items():
        metric_name = metric.replace("_", " ").capitalize()
        weighted_metrics[metric_name] = {}
        for date, file_metrics in dates.items():
            aggregated_file_metrics = aggregate_file_metrics(file_metrics)
            weighted_metrics[metric_name][date] = group_calc_helper(
                aggregated_file_metrics
            )

    return weighted_metrics


def generate_plotly_layout(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        title={
            "text": title,
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=24, color="#FFFFFF"),
        },
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor="white",
            linewidth=2,
            ticks="outside",
            tickfont=dict(
                family="Arial, Helvetica, sans-serif", size=14, color="white"
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True,
            tickfont=dict(
                family="Arial, Helvetica, sans-serif", size=14, color="white"
            ),
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=50,
            r=50,
            t=100,
        ),
        showlegend=True,
        plot_bgcolor="#2a2a2a",
        paper_bgcolor="#2a2a2a",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def create_hover_templates(scores: Dict[datetime, GroupMetrics]) -> List[str]:
    hover_templates = []
    for date in sorted(scores.keys()):
        hover_text = f"<b>Date:</b> {date.strftime('%Y-%m-%d')}<br><b>Score:</b> {scores[date]['score']:.2f}<br>"

        max_len = max([len(file.file_path) for file in scores[date]["key_files"]])

        for file in scores[date]["key_files"]:
            padding = max_len - len(file.file_path)
            file_path = f"<span style='font-family: monospace;'>{file.file_path} {' ' * padding}</span>"
            score = f"<span style='font-weight: bold;'>{file.score:.1f}</span>"
            contrib_percent = f"({int(file.contrib_percent)}%)"
            hover_text += f"{file_path} {score} {contrib_percent}<br>"

        hover_text += "<extra></extra>"
        hover_templates.append(hover_text)
    return hover_templates


def generate_plotly_figs(weighted_metrics: WeightedMetrics) -> List[Dict]:
    color_palette = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD"]
    figs_json = []

    for idx, (metric, scores) in enumerate(weighted_metrics.items()):
        hover_templates = create_hover_templates(scores)
        dates_sorted = sorted(scores.keys())

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=dates_sorted,
                y=[scores[date]["score"] for date in dates_sorted],
                mode="lines+markers",
                name=metric,
                marker=dict(size=10, color=color_palette[idx % len(color_palette)]),
                line=dict(width=3, color=color_palette[idx % len(color_palette)]),
                hovertemplate=hover_templates,
            )
        )
        fig = generate_plotly_layout(fig, metric)
        figs_json.append(fig.to_dict())

    return figs_json


def enrich_description(plot_json: List[Dict]) -> List[Dict]:
    """Add a description to each Plotly figure based on the metric name"""
    for fig in plot_json:
        metric_name = fig["data"][0]["name"].lower().replace(" ", "_")
        fig["description"] = config.METRICS[metric_name]
    return plot_json


def batch_process(
    items: List[Any],
    proccess_function: Callable,
    batch_size: int = 100,
    *args,
    **kwargs,
):
    """Generically applies a function to a list of items in batches"""
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i : i + batch_size]
        result = proccess_function(batch, *args, **kwargs)
        results.extend(result)
    return results


def get_metrics(user_email: str, project_name: str):
    """
    query database for all files associated with the project, join data between
    files and metrics tables, calculate weighted metrics, and generate plotly
    """
    files = io_operations.get_files(user_email, project_name)
    metrics = batch_process(list(files), io_operations.get_metrics)

    files_metrics = join_files_metrics(metrics, files)
    grouped_metrics = group_metrics(files_metrics)
    weighted_metrics = calculate_weighted_metrics(grouped_metrics)
    plot_json = generate_plotly_figs(weighted_metrics)
    enriched_plot = enrich_description(plot_json)

    return enriched_plot
