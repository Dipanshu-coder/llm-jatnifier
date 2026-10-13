# LLM Jatnifier

**Make any LLM answer easier to read — in Colab or on your computer.**

## Easiest way: Google Colab

[**Open the ready-to-run Colab notebook**](https://colab.research.google.com/github/Dipanshu-coder/llm-jatnifier/blob/main/notebooks/LLM_Jatnifier_Quickstart.ipynb)

1. Run the install cell.
2. Choose a provider.
3. Enter your API key when asked.
4. Paste your text and run.

## Use it in one line

Install once:

```bash
pip install git+https://github.com/Dipanshu-coder/llm-jatnifier.git
```

Then use in Colab, Jupyter, VS Code, or a Python script:

```python
from llm_output_polisher import polish

print(polish("paste your raw LLM answer here", api_key="hf_YOUR_TOKEN"))
```

That defaults to Hugging Face. Your API key is never hard-coded by Jatnifier; for repeat use, set `HF_TOKEN` as an environment variable instead.

## Pick another provider

```python
from llm_output_polisher import polish

# Hugging Face
print(polish("raw answer", provider="huggingface", api_key="hf_..."))

# NVIDIA NIM
print(polish("raw answer", provider="nvidia", api_key="YOUR_NVIDIA_KEY"))

# Ollama running on this computer
print(polish("raw answer", provider="ollama"))

# LM Studio running on this computer
print(polish("raw answer", provider="lmstudio", model="your-loaded-model"))

# Any OpenAI-compatible endpoint
print(polish("raw answer", base_url="http://localhost:8000/v1",
             model="your-model", api_key="YOUR_KEY"))
```

Choose a style with `style="study"`, `"technical"`, `"concise"`, or `"general"`.

## Simple local cleanup — no model or API key

```python
from llm_output_polisher import Polisher
print(Polisher.format_only("###heading\n\n\n• first point"))
```

## What it does

Jatnifier takes text from any LLM, sends it to the provider you choose for editing, and returns cleaner Markdown. It does not host the LLM itself. Hosted Hugging Face/NVIDIA calls need internet and provider access; Ollama/LM Studio need a model running locally. Model-backed polishing makes an extra model call and can add cost/latency. It improves presentation, not factual accuracy.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

MIT License.
