# LLM Jatnifier

**A plug-in output beautifier for local and open-source LLMs.** Turn raw model responses into clear, readable Markdown with a small Python API, CLI, or optional HTTP endpoint.

Works with OpenAI-compatible chat endpoints such as **Ollama, LM Studio, vLLM, LocalAI**, and compatible endpoints exposed from Google Colab or another machine. No proprietary hosted model is required.

## Features

- Simple API: `polisher.polish(text)`
- Model-backed editing profiles: `general`, `study`, `technical`, `concise`
- Local formatting-only cleanup with no extra model call
- Configurable endpoint, model, API key, and timeout
- CLI and optional FastAPI service
- Graceful fallback to the original text if the model request fails (configurable)

## Install

Clone this repository, then install it:

```bash
pip install -e .
```

For optional HTTP API and development tools:

```bash
pip install -e ".[api,dev]"
```

## Quick start with Ollama

Install [Ollama](https://ollama.com/) and pull a model, for example:

```bash
ollama pull qwen2.5:3b
```

Then run:

```python
from llm_output_polisher import Polisher

polisher = Polisher(
    base_url="http://localhost:11434/v1",
    model="qwen2.5:3b",
    api_key="ollama",  # placeholder accepted by Ollama's OpenAI-compatible API
)

raw = "photosynthesis is process plants use sunlight and co2 water to make glucose oxygen"
print(polisher.polish(raw, profile="study"))
```

For a no-model-call cleanup pass:

```python
clean = Polisher.format_only("###heading\n\n\n• first point")
print(clean)
```

## Connect a different model

Configuration can be supplied directly or with environment variables:

- `POLISHER_BASE_URL` (default: `http://localhost:11434/v1`)
- `POLISHER_MODEL` (default: `qwen2.5:3b`)
- `POLISHER_API_KEY` (default: `ollama`)

**LM Studio**
```python
p = Polisher(base_url="http://localhost:1234/v1", model="your-loaded-model", api_key="lm-studio")
```

**vLLM**
```python
p = Polisher(base_url="http://localhost:8000/v1", model="your-model", api_key="EMPTY")
```

**Google Colab / remote server**

Start an OpenAI-compatible server in your notebook and set `POLISHER_BASE_URL` to its reachable `/v1` endpoint. Use an authenticated/private tunnel; do not expose a model server to the public internet without access controls. See `examples/colab_or_remote.py`.

## Profiles

- `general` — clear, natural, easy-to-scan response
- `study` — student-friendly notes, headings, definitions, and bullets
- `technical` — prioritize precision; preserve code, commands, identifiers, and equations
- `concise` — remove repetition without intentionally dropping important details

Extra instructions are supported:

```python
print(polisher.polish(raw, profile="general", instructions="Use short paragraphs and keep the tone friendly."))
```

## CLI

```bash
llm-polish --text "raw model output" --profile general
llm-polish --file response.txt --profile study
llm-polish --format-only --file response.txt
```

## Optional HTTP API

Start the service locally:

```bash
uvicorn llm_output_polisher.api:app --host 127.0.0.1 --port 8787
```

Check health or polish text:

```bash
curl http://127.0.0.1:8787/health
curl -X POST http://127.0.0.1:8787/polish -H "Content-Type: application/json" -d '{"text":"raw model output","profile":"general"}'
```

The API listens on localhost in this example. Add appropriate authentication and deployment protections before exposing it to other machines.

## How it fits into an app

```text
Your LLM -> Polisher.polish(raw_text) -> polished Markdown -> your UI
```

Call it after your model generates a response and before rendering the response in your app.

## Important limitations

Jatnifier improves presentation and organization; it is **not a fact-checker** and cannot guarantee that every detail is preserved. Review important outputs, especially code, citations, numbers, and high-stakes content. Model-backed polishing makes a second inference call and may add latency and compute cost. Use `format_only` when you need deterministic, local whitespace/Markdown cleanup only.

## Development

```bash
pip install -e ".[dev]"
pytest
```

MIT License. See [LICENSE](LICENSE).
