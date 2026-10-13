# LLM Jatnifier

**A simple output-polishing layer for LLMs, designed to be easy to try in Google Colab.** Give it raw text from an LLM and get cleaner, more readable Markdown back.

## Easiest: run it in Google Colab

Open the ready-to-run notebook: **[LLM Jatnifier Quick Start](https://colab.research.google.com/github/Dipanshu-coder/llm-jatnifier/blob/main/notebooks/LLM_Jatnifier_Quickstart.ipynb)**.

1. Run the install cell.
2. Choose `huggingface` or `nvidia`.
3. Enter your provider API token when prompted.
4. Paste raw model output and run the polish cell.

The notebook uses hosted API endpoints, so you do **not** need to set up a GPU in Colab. Provider access, model availability, and usage limits depend on your account. Keep tokens private.

## What can it connect to?

- **Hugging Face Inference Providers** through its OpenAI-compatible router.
- **NVIDIA NIM** through its OpenAI-compatible API.
- **Ollama**, **LM Studio**, **vLLM**, and other OpenAI-compatible chat endpoints.
- Any model's output as plain text: paste the raw output into Jatnifier, then polish it.

Jatnifier is a post-processing layer, not a model host. It does not automatically run every Hugging Face model locally. Running a model locally in Colab requires installing/loading that model separately; hosted APIs are the simplest starting point.

## Use in Python

Install from GitHub:

```python
%pip install "git+https://github.com/Dipanshu-coder/llm-jatnifier.git"
```

Then configure an OpenAI-compatible endpoint:

```python
from getpass import getpass
from llm_output_polisher import Polisher

polisher = Polisher(
    base_url="https://router.huggingface.co/v1",
    model="Qwen/Qwen2.5-7B-Instruct",
    api_key=getpass("Hugging Face token: "),
)

raw_output = "photosynthesis is process plants use sunlight and co2 water to make glucose oxygen"
print(polisher.polish(raw_output, profile="study"))
```

For NVIDIA, use `base_url="https://integrate.api.nvidia.com/v1"`, your NVIDIA API key, and a model currently available to your account, such as `meta/llama-3.1-8b-instruct`.

## Profiles

- `general` — clearer, natural, easy-to-scan text
- `study` — student-friendly notes, headings, and bullets
- `technical` — preserve code, identifiers, commands, equations, and exact values
- `concise` — reduce repetition while keeping important details

No API call needed for basic cleanup:

```python
from llm_output_polisher import Polisher
print(Polisher.format_only("###heading\n\n\n• first point"))
```

## Use after another LLM

```text
Your model generates text -> polisher.polish(text) -> display polished Markdown
```

The model-backed polish step makes a **second inference call**, so it may add latency and cost. Jatnifier improves presentation; it is not a fact-checker and cannot guarantee perfect preservation. Review important code, numbers, citations, and high-stakes output.

## Local endpoints

```python
# Ollama
p = Polisher(base_url="http://localhost:11434/v1", model="qwen2.5:3b", api_key="ollama")

# LM Studio
p = Polisher(base_url="http://localhost:1234/v1", model="your-loaded-model", api_key="lm-studio")

# vLLM
p = Polisher(base_url="http://localhost:8000/v1", model="your-model", api_key="EMPTY")
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

MIT License. See [LICENSE](LICENSE).
