# LLM Jatnifier

**Ask a question, get an answer, and automatically improve its readability.** Jatnifier is a provider-agnostic Python library with a Gradio chat UI and an optional HTTP API.

## Quick start

### Google Colab

```python
!git clone https://github.com/Dipanshu-coder/llm-jatnifier.git
%cd llm-jatnifier
!pip install -e ".[ui]"

from app import demo
demo.launch(share=True)
```

Choose a provider, enter your API key (or use a local model), ask a question, and click **Ask and polish**. The original answer remains available in a dropdown.

A Gradio share link is accessible to anyone who has it while the notebook is running. Avoid sharing it when entering API credentials and stop the notebook when finished.

### Run locally

```bash
git clone https://github.com/Dipanshu-coder/llm-jatnifier.git
cd llm-jatnifier
pip install -e ".[ui]"
python app.py
```

## Providers

The interface supports Hugging Face, NVIDIA, Ollama, and LM Studio. Hosted providers need valid credentials and model access. For local providers, start the model server and ensure the selected model is loaded.

| Provider | Default model | Credential |
|---|---|---|
| Hugging Face | `Qwen/Qwen2.5-7B-Instruct` | `HF_TOKEN` |
| NVIDIA | `meta/llama-3.1-8b-instruct` | `NVIDIA_API_KEY` |
| Ollama | `qwen2.5:3b` | Local server |
| LM Studio | Your loaded model | Local server |

## Python library

```bash
pip install git+https://github.com/Dipanshu-coder/llm-jatnifier.git
```

```python
from llm_output_polisher import polish

clean = polish(
    "Paste an existing LLM answer here",
    provider="huggingface",
    api_key="YOUR_HUGGINGFACE_TOKEN",
    style="study",
)
print(clean)
```

Styles: `general`, `study`, `concise`, and `technical`. The editor is instructed to preserve meaning, figures, uncertainty, code, commands, equations, URLs, and quoted text. Always verify important facts: rewriting can still introduce mistakes.

## HTTP API

Install the API dependencies and start the server:

```bash
pip install -e ".[api]"
uvicorn llm_output_polisher.api:app --host 127.0.0.1 --port 8000
```

- `GET /health` — health check.
- `POST /polish` — polish one text.
- `POST /polish/batch` — process up to 20 texts in one request.

Example single request:

```bash
curl -X POST http://127.0.0.1:8000/polish \
  -H "Content-Type: application/json" \
  -d '{"text":"###heading\n\n• item","profile":"study","format_only":true}'
```

Example batch request:

```json
{
  "texts": ["###First answer", "• Second answer"],
  "profile": "general",
  "format_only": true
}
```

Send that JSON to `POST /polish/batch`. The endpoint accepts 1–20 texts, each up to 100,000 characters, and processes them sequentially to avoid flooding a provider. Set `format_only: true` for local Markdown cleanup without any model calls. The interactive API schema is available at `/docs` when the server is running.

**Deployment safety:** the optional API is intended for local/trusted deployment and currently has no built-in user authentication or rate limiting. Do not expose it directly to the public internet until authentication, rate limits, HTTPS, and provider-cost controls are configured. Never commit API keys.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Scope

Jatnifier improves presentation of model-generated text; it does not guarantee factual accuracy and does not automatically modify answers inside other AI websites. Browser extensions or explicit integrations would be separate projects.

MIT License.
