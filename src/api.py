import json
from typing import Any, Callable

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ollama import chat

try:
    from .tools import DATASETS_DIR, available_tools, get_first_rows, get_last_rows
except ImportError:
    # Allows running as a script from the repository root.
    from tools import DATASETS_DIR, available_tools, get_first_rows, get_last_rows


DEFAULT_MODEL = "functiongemma"
MAX_RESULT_PREVIEW_CHARS = 600

tool_registry: dict[str, Callable[..., str]] = {
    tool.__name__: tool for tool in available_tools
}

app = FastAPI(
    title="Intent Control Layer API",
    description="Simple API for dataset tooling and intent-driven execution.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IntentRequest(BaseModel):
    prompt: str = Field(min_length=1, description="User prompt")
    model: str = Field(default=DEFAULT_MODEL, description="Ollama model name")
    max_steps: int = Field(
        default=8,
        ge=1,
        le=20,
        description="Maximum number of tool-execution rounds",
    )


class ToolTrace(BaseModel):
    tool: str
    arguments: dict[str, Any]
    result_preview: str


class IntentResponse(BaseModel):
    answer: str
    model: str
    tools_used: list[ToolTrace]


def _parse_tool_arguments(raw_arguments: Any) -> dict[str, Any]:
    if raw_arguments is None:
        return {}
    if isinstance(raw_arguments, dict):
        return raw_arguments
    if isinstance(raw_arguments, str):
        stripped = raw_arguments.strip()
        if not stripped:
            return {}
        parsed = json.loads(stripped)
        if not isinstance(parsed, dict):
            raise ValueError("Tool arguments must decode to a JSON object.")
        return parsed
    raise ValueError(
        f"Unsupported tool argument type: {type(raw_arguments).__name__}"
    )


def _normalize_dataset_name(dataset: str) -> str:
    name = dataset.strip()
    if not name.lower().endswith(".csv"):
        name = f"{name}.csv"
    return name


def _run_intent_loop(prompt: str, model: str, max_steps: int) -> tuple[str, list[ToolTrace]]:
    messages = [{"role": "user", "content": prompt}]
    traces: list[ToolTrace] = []

    for _ in range(max_steps):
        response = chat(model, messages=messages, tools=available_tools)

        if not response.message.tool_calls:
            return (response.message.content or "", traces)

        messages.append(response.message)

        for tool_call in response.message.tool_calls:
            tool_name = tool_call.function.name
            parsed_arguments: dict[str, Any] = {}

            function_to_call = tool_registry.get(tool_name)
            if function_to_call is None:
                result = f"Error: Tool '{tool_name}' not found."
            else:
                try:
                    parsed_arguments = _parse_tool_arguments(
                        tool_call.function.arguments
                    )
                    result = function_to_call(**parsed_arguments)
                except Exception as error:
                    result = f"Error executing {tool_name}: {error}"

            result_str = str(result)
            traces.append(
                ToolTrace(
                    tool=tool_name,
                    arguments=parsed_arguments,
                    result_preview=result_str[:MAX_RESULT_PREVIEW_CHARS],
                )
            )

            messages.append(
                {
                    "role": "tool",
                    "name": tool_name,
                    "content": result_str,
                }
            )

    raise RuntimeError(
        "Max tool steps reached before producing a final response.")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "intent-control-layer",
        "message": "FastAPI server is running.",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/datasets")
def list_datasets() -> dict[str, Any]:
    datasets = sorted(path.name for path in DATASETS_DIR.glob("*.csv"))
    return {"count": len(datasets), "datasets": datasets}


@app.get("/datasets/{dataset}/head")
def dataset_head(
    dataset: str,
    n_rows: int = Query(default=5, ge=1, le=200),
) -> dict[str, str]:
    dataset_name = _normalize_dataset_name(dataset)
    if not (DATASETS_DIR / dataset_name).exists():
        raise HTTPException(
            status_code=404, detail=f"Dataset '{dataset_name}' was not found.")
    return {
        "dataset": dataset_name,
        "preview_markdown": get_first_rows(dataset=dataset_name, n_rows=n_rows),
    }


@app.get("/datasets/{dataset}/tail")
def dataset_tail(
    dataset: str,
    n_rows: int = Query(default=5, ge=1, le=200),
) -> dict[str, str]:
    dataset_name = _normalize_dataset_name(dataset)
    if not (DATASETS_DIR / dataset_name).exists():
        raise HTTPException(
            status_code=404, detail=f"Dataset '{dataset_name}' was not found.")
    return {
        "dataset": dataset_name,
        "preview_markdown": get_last_rows(dataset=dataset_name, n_rows=n_rows),
    }


@app.post("/intent/query", response_model=IntentResponse)
def query_intent(request: IntentRequest) -> IntentResponse:
    try:
        answer, traces = _run_intent_loop(
            prompt=request.prompt,
            model=request.model,
            max_steps=request.max_steps,
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return IntentResponse(answer=answer, model=request.model, tools_used=traces)
