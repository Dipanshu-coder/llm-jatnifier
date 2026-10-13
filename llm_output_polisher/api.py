"""Optional FastAPI wrapper. Install with: pip install -e ".[api]"."""
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .core import Polisher

app = FastAPI(title="LLM Jatnifier", version="0.1.0")
polisher = Polisher()


class PolishRequest(BaseModel):
    text: str = Field(min_length=1, max_length=100_000)
    profile: str = "general"
    instructions: Optional[str] = None
    format_only: bool = False


class PolishResponse(BaseModel):
    text: str
    profile: str
    format_only: bool


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/polish", response_model=PolishResponse)
def polish(req: PolishRequest):
    try:
        result = (
            polisher.format_only(req.text)
            if req.format_only
            else polisher.polish(req.text, profile=req.profile, instructions=req.instructions, raise_errors=True)
        )
        return PolishResponse(text=result, profile=req.profile, format_only=req.format_only)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Polishing failed: {exc}") from exc
