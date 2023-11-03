from datetime import datetime

import plotly.graph_objects as go
from fastapi.responses import JSONResponse

from . import config, io_operations, models


# TODO these types should be hard defined (in analytics.py probably)
def join_files_metrics(metrics, files) -> models.FileJoinedOnMetrics:
    for metric in metrics:
        if metric["file_id"] in files:
            metric.update(files[metric["file_id"]])
    return metrics


def calculate_weighted_metrics(files_metrics: models.FileJoinedOnMetrics):
    # group metrics by metric name
    groupby_metrics = {}
    for obj in files_metrics:
        if obj["metric"] not in groupby_metrics:
            groupby_metrics[obj["metric"]] = []
        groupby_metrics[obj["metric"]].append(obj)

    # convert timestamp to datetime object
    strptime_fmt = "%Y-%m-%dT%H:%M:%S.%f%z"
    for metric_name, objs in groupby_metrics.items():
        for obj in objs:
            obj["timestamp"] = datetime.strptime(obj["timestamp"], strptime_fmt)

    # groupby date within each metric group
    for metric_name, objs in groupby_metrics.items():
        dates = {}
        for obj in objs:
            date = obj["timestamp"].date()
            if date not in dates:
                dates[date] = []
            dates[date].append(obj)
        groupby_metrics[metric_name] = dates

    # aggregate scores weighted by loc
    weighted_metrics = {}
    for metric, dates in groupby_metrics.items():
        weighted_metrics[metric] = {}
        for date, objs in dates.items():
            total_loc = sum(obj["loc"] for obj in objs)
            weighted_score = sum(
                obj["score"] * (obj["loc"] / total_loc) for obj in objs
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
