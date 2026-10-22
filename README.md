# LLM Jatnifier

**Ask a question and automatically get a cleaner answer.** Use the chat UI, or call the Python function from your own project.

## Automatic mode (chat UI)

### Google Colab
Run these cells:

```python
!git clone https://github.com/Dipanshu-coder/llm-jatnifier.git
%cd llm-jatnifier
!pip install -e ".[ui]"

from app import demo
demo.launch(share=True)
```

Colab will show a temporary link to the interface. Open it, choose a provider, enter your API key, ask your question, and click **Ask and polish**. Jatnifier gets the model's answer and polishes it automatically. The original answer is available in a dropdown.

**Security:** a Gradio share link makes the interface reachable by people who have the link while it is running. Do not share it with others when using your API key, and stop the notebook when finished.

### Your computer
Install Python, then run in a terminal:

```bash
git clone https://github.com/Dipanshu-coder/llm-jatnifier.git
cd llm-jatnifier
pip install -e ".[ui]"
python app.py
```

Open the local address printed in the terminal.

### Providers
The interface includes Hugging Face, NVIDIA, Ollama, and LM Studio. Hosted providers need a valid API key and model access. For local providers, start Ollama or LM Studio first and make sure the selected model is available. You can override the default model name in the interface.

## Use the polishing function in your own code

Install the core package:

```bash
pip install git+https://github.com/Dipanshu-coder/llm-jatnifier.git
```

Then:

```python
from llm_output_polisher import polish

improved = polish(
    "Paste an existing LLM answer here",
    provider="huggingface",
    api_key="YOUR_HUGGINGFACE_TOKEN",
    style="study",
)
print(improved)
```

Supported styles: `general`, `study`, `concise`, and `technical`.

Other provider examples:

```python
polish("raw answer", provider="nvidia", api_key="YOUR_NVIDIA_KEY")
polish("raw answer", provider="ollama")
polish("raw answer", provider="lmstudio", model="your-loaded-model")
```

## What it does (and doesn't do)

The automatic chat UI makes one call to generate an answer and a second call to improve its presentation. That adds some latency and may incur provider usage costs. Polishing can still introduce errors, so it does not guarantee factual accuracy. This app does **not** automatically change answers inside the ChatGPT, Gemini, or other existing websites; doing that would require a separate browser extension or integration.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

MIT License.


## Tool-using personal AI agent (new prototype)

The newer `personal_agent.py` prototype is more than the planner: it supports multi-step model tool-calling, public web search, arithmetic, local SQLite notes, and an activity log.

### Run locally

```bash
pip install -e ".[ui]"
# Configure an OpenAI-compatible provider; example for Hugging Face:
# Windows PowerShell:
$env:AGENT_BASE_URL="https://router.huggingface.co/v1"
$env:AGENT_MODEL="Qwen/Qwen2.5-7B-Instruct"
$env:AGENT_API_KEY="your-provider-key"
python personal_agent.py
```

You can also configure those variables in your hosting provider's environment settings. Use a model/provider that supports OpenAI-compatible tool/function calling. Local Ollama is possible with `AGENT_BASE_URL=http://localhost:11434/v1` and a compatible model already installed.

### Current capability boundary

- **Works in this prototype:** public web search, calculations, save/list local notes, multi-step tool loop, conversation history while the session remains open.
- **Not implemented yet:** secure multi-user accounts, remote database sync, Gmail/WhatsApp/calendar connectors, browser automation for logged-in sites, purchases, sending messages, background jobs, mobile app, and Meta Muse's private internals.
- **Safety:** do not deploy it publicly without authentication, per-user data isolation, rate limits, secret management, and SSRF protections hardened for your hosting environment. Notes are stored in a local SQLite file. A shared server would need user-isolated storage before real users are allowed.
- The web-search HTML parser is a prototype and may break if the search provider changes its markup. Check cited sources before relying on results.

This is an independent project inspired by the personal-agent product category. It is not Meta Muse, does not use Meta's private code or APIs, and does not bypass regional access controls.

For a public Render deployment, also set `AGENT_USERNAME` and `AGENT_PASSWORD`; the app refuses to start on Render without both. The free Render filesystem may be ephemeral, so local notes can be lost on restart. Do not use this prototype for sensitive personal data.

See [the architecture and safety plan](docs/INDIA_PERSONAL_AGENT_MVP.md) for the intended next steps.
