from datetime import datetime
import plotly.graph_objects as go
from pydantic import BaseModel
from typing import List
from uuid import UUID

from . import models, config


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


def join_files_metrics(metrics: list[models.Metric], files: List[models.File]):
    joined_data = []
    for metric in metrics:
        file = files.get(metric.file_id)
        joined_data.append({**metric.model_dump(), **file.model_dump()})
    return [FileMetric(**data) for data in joined_data]


def group_metrics(file_metrics: List[FileMetric]):
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


def calculate_weighted_metrics(grouped_metrics):
    # aggregate scores weighted by loc
    weighted_metrics = {}
    for metric, dates in grouped_metrics.items():
        weighted_metrics[metric] = {}
        for date, file_metrics in dates.items():
            total_loc = sum(file_metric.loc for file_metric in file_metrics)
            weighted_score = sum(
                file_metric.score * (file_metric.loc / total_loc)
                for file_metric in file_metrics
            )
            weighted_metrics[metric][date] = weighted_score

    return weighted_metrics


def generate_plotly_figs(data):
    """
    Generate a list of individual Plotly figures based on the given metrics data.
    """
    # Define a polished color palette
    color_palette = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD"]

    figs_json = []

    # Iterate through metrics in the data
    for idx, (metric_name, metric_data) in enumerate(data.items()):
        title = metric_name.replace("_", " ").capitalize()

        # Create the figure
        fig = go.Figure()

        # Sort the dates in metric_data before plotting
        sorted_dates = sorted(metric_data.keys())
        x_values = sorted_dates
        y_values = [metric_data[date] for date in sorted_dates]

        # Add trace for the metric
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=y_values,
                mode="lines+markers",
                name=title,
                marker=dict(size=10, color=color_palette[idx % len(color_palette)]),
                line=dict(width=3, color=color_palette[idx % len(color_palette)]),
            )
        )

        # Repeating layout code. Consider centralizing if getting more complex.
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
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )

        figs_json.append(fig.to_dict())

    return figs_json


def enrich_description(plot_json):
    """Add a description to each Plotly figure based on the metric name"""
    for fig in plot_json:
        metric_name = fig["data"][0]["name"].lower().replace(" ", "_")
        fig["description"] = config.METRIC_DESCRIPTIONS[metric_name]
    return plot_json
