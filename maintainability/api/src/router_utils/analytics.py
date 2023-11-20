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


class KeyFile(BaseModel):
    file_path: str
    contrib_percent: float
    score: int


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


def group_calc_helper(file_metrics: List[FileMetric]) -> GroupMetrics:
    total_loc = sum(file_metric.loc for file_metric in file_metrics)
    weighted_score = 0
    key_files = []
    for file_metric in file_metrics:
        contrib_percent = file_metric.loc / total_loc
        weighted_score += file_metric.score * contrib_percent
        key_files.append(
            KeyFile(
                file_path=file_metric.file_path,
                contrib_percent=contrib_percent,
                score=file_metric.score,
            )
        )

    key_files = sorted(key_files, key=lambda x: x.contrib_percent, reverse=True)[:5]
    return {"score": weighted_score, "key_files": key_files}


def calculate_weighted_metrics(grouped_metrics: GroupedMetrics) -> WeightedMetrics:
    """Orchestrate the calculation of weighted metrics for each metric type."""
    weighted_metrics = {}
    for metric, dates in grouped_metrics.items():
        metric_name = metric.replace("_", " ").capitalize()
        weighted_metrics[metric_name] = {}
        for date, file_metrics in dates.items():
            weighted_metrics[metric_name][date] = group_calc_helper(file_metrics)

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
    return [
        f"<b>({date}) Score: {scores[date]['score']:.2f}</b><br>"
        + "<br>".join(
            [
                f"{file.file_path}: {file.score} ({file.contrib_percent:.2f}%)"
                for file in scores[date]["key_files"]
            ]
        )
        for date in sorted(scores.keys())
    ]


def generate_plotly_figs(weighted_metrics: WeightedMetrics) -> List[Dict]:
    """
    Generate a list of individual Plotly figures based on the given metrics data.
    """
    color_palette = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD"]
    figs_json = []

    for idx, (metric, scores) in enumerate(weighted_metrics.items()):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=sorted(scores.keys()),
                y=[scores[date]["score"] for date in sorted(scores.keys())],
                mode="lines+markers",
                name=metric,
                marker=dict(size=10, color=color_palette[idx % len(color_palette)]),
                line=dict(width=3, color=color_palette[idx % len(color_palette)]),
                hovertemplate=create_hover_templates(scores),
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
