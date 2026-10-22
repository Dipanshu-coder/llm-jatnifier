"""Optional FastAPI wrapper. Install with: pip install -e ".[api]"."""
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .core import Polisher

app = FastAPI(
    title="LLM Jatnifier API",
    description="Clean, polish, and batch-process LLM responses.",
    version="0.3.0",
)
polisher = Polisher()


class PolishRequest(BaseModel):
    text: str = Field(min_length=1, max_length=100_000)
    profile: str = "general"
    instructions: Optional[str] = Field(default=None, max_length=2_000)
    format_only: bool = False


class PolishResponse(BaseModel):
    text: str
    profile: str
    format_only: bool


class BatchPolishRequest(BaseModel):
    texts: List[str] = Field(min_length=1, max_length=20)
    profile: str = "general"
    instructions: Optional[str] = Field(default=None, max_length=2_000)
    format_only: bool = False

    @staticmethod
    def _validate_texts(texts):
        for index, text in enumerate(texts):
            if not text.strip():
                raise ValueError(f"texts[{index}] must not be blank")
            if len(text) > 100_000:
                raise ValueError(f"texts[{index}] exceeds the 100,000 character limit")
        return texts


class BatchPolishResponse(BaseModel):
    results: List[PolishResponse]
    count: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "llm-jatnifier"}


def _polish_one(req: PolishRequest) -> PolishResponse:
    try:
        result = (
            polisher.format_only(req.text)
            if req.format_only
            else polisher.polish(
                req.text,
                profile=req.profile,
                instructions=req.instructions,
                raise_errors=True,
            )
        )
        return PolishResponse(text=result, profile=req.profile, format_only=req.format_only)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Polishing provider request failed.") from exc


@app.post("/polish", response_model=PolishResponse)
def polish(req: PolishRequest):
    return _polish_one(req)


@app.post("/polish/batch", response_model=BatchPolishResponse)
def polish_batch(req: BatchPolishRequest):
    """Polish up to 20 independent outputs in one request.

    Each item is processed sequentially to avoid unexpectedly flooding a local
    model server or provider account. Set format_only=true to avoid model calls.
    """
    BatchPolishRequest._validate_texts(req.texts)
    results = []
    for text in req.texts:
        results.append(
            _polish_one(
                PolishRequest(
                    text=text,
                    profile=req.profile,
                    instructions=req.instructions,
                    format_only=req.format_only,
                )
            )
        )
    return BatchPolishResponse(results=results, count=len(results))
