import base64
import json
import re
import secrets
from datetime import datetime

import plotly
import plotly.graph_objects as go
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from llm_blocks import block_factory
from passlib.context import CryptContext

from . import config, io_operations, logger, models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_llm() -> callable:
    return block_factory.get(
        "template",
        template=config.PROMPT,
        temperature=config.TEMPERATURE,
        model_name=config.MODEL_NAME,
    )


def parse_response(text: str) -> float:
    try:
        match = re.search(r"(\d{1,2})/10", text)
        response = int(match.group(1))
    except AttributeError as e:
        logger.logger(f"Error parsing LLM response={text} with error={e}")
        response = -1
    return response


def extract_metrics(file_id: str, filepath: str, code: str, metric: str) -> int:
    gpt_interface = get_llm()
    description = config.METRIC_DESCRIPTIONS[metric]
    response = gpt_interface(
        filepath=filepath,
        code=code,
        metric=metric.replace("_", " "),
        description=description,
    )
    metric_quantity = int(parse_response(response))
    io_operations.write_metrics(
        file_id=file_id,
        metric=metric,
        metric_quantity=metric_quantity,
        reasoning=response,
    )
    return metric_quantity


def validate_user(email: str, password: str) -> None:
    user = io_operations.get_user(email)

    if not user or not pwd_context.verify(password, user["password"]):
        logger.logger(f"Unauthorized login attempt: email={email}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")


def generate_new_api_key():
    random_bytes = secrets.token_bytes(32)
    return base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")


def join_files_metrics(
    user_email: str, project_name: str
) -> models.FileJoinedOnMetrics:
    # get all files from user="test", project="maintainability"
    files = io_operations.get_files(user_email, project_name)
    if not files.data:
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"user_email={user_email}, project_name={project_name} combination not found"
            },
        )
    # get all metrics associated with files
    file_dict = {file["file_id"]: file for file in files.data}
    metrics = io_operations.get_metrics(list(file_dict))
    if not metrics.data:
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"No metrics found for user_email={user_email}, project_name={project_name} combination"
            },
        )
    # join tables
    for metric in metrics.data:
        if metric["file_id"] in file_dict:
            metric.update(file_dict[metric["file_id"]])

    return metrics.data


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


def generate_plotly_fig(data):
    """
    Generate a Plotly figure based on the given metrics data, using a polished,
    production-ready design.
    """
    # Create the figure
    fig = go.Figure()

    # Define a polished color palette
    color_palette = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD"]

    # Iterate through metrics in the data
    for idx, (metric_name, metric_data) in enumerate(data.items()):
        x_values = list(metric_data.keys())
        y_values = list(metric_data.values())

        # Add trace for the metric
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=y_values,
                mode="lines+markers",
                name=metric_name.capitalize(),
                marker=dict(size=10, color=color_palette[idx % len(color_palette)]),
                line=dict(width=3, color=color_palette[idx % len(color_palette)]),
            )
        )

    fig.update_layout(
        template="plotly_dark",  # Dark theme
        title={
            "text": "Metrics Overview",
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
        width=980,
        height=500,
    )
    return fig.to_dict()
