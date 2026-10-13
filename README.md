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
