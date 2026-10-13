"""Simple chat UI: ask a model and automatically polish its answer."""
import os

import gradio as gr
from openai import OpenAI

from llm_output_polisher import polish


PROVIDERS = {
    "Hugging Face": {
        "base_url": "https://router.huggingface.co/v1",
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "key_env": "HF_TOKEN",
    },
    "NVIDIA": {
        "base_url": "https://integrate.api.nvidia.com/v1",
        "model": "meta/llama-3.1-8b-instruct",
        "key_env": "NVIDIA_API_KEY",
    },
    "Ollama (local)": {
        "base_url": "http://localhost:11434/v1",
        "model": "qwen2.5:3b",
        "key_env": "",
    },
    "LM Studio (local)": {
        "base_url": "http://localhost:1234/v1",
        "model": "",
        "key_env": "",
    },
}


def answer_and_polish(question, provider, api_key, model, style):
    if not question or not question.strip():
        raise gr.Error("Type a question first.")

    config = PROVIDERS[provider]
    chosen_model = (model or "").strip() or config["model"]
    if not chosen_model:
        raise gr.Error("Enter the model name loaded in LM Studio.")

    key = (api_key or "").strip()
    if not key and config["key_env"]:
        key = os.getenv(config["key_env"], "")
    if not key and not config["key_env"]:
        key = "ollama"
    if not key:
        raise gr.Error(
            f"Enter your API key, or set the {config['key_env']} environment variable."
        )

    try:
        client = OpenAI(base_url=config["base_url"], api_key=key, timeout=90)
        response = client.chat.completions.create(
            model=chosen_model,
            messages=[
                {
                    "role": "system",
                    "content": "Answer the user's question helpfully, accurately, and directly. "
                    "Use clear formatting where useful. Do not claim certainty when unsure.",
                },
                {"role": "user", "content": question.strip()},
            ],
            temperature=0.4,
        )
        raw = response.choices[0].message.content
        if not raw or not raw.strip():
            raise ValueError("The model returned an empty answer.")

        improved = polish(
            raw,
            provider=provider.lower().replace(" (local)", "").replace(" ", ""),
            model=chosen_model,
            api_key=key,
            style=style,
            base_url=config["base_url"],
        )
        return improved, raw
    except Exception as exc:
        raise gr.Error(
            f"Request failed: {exc}\n\nCheck your API key, model name, provider access, "
            "and (for local models) that the model server is running."
        ) from exc


with gr.Blocks(title="LLM Jatnifier") as demo:
    gr.Markdown(
        "# LLM Jatnifier\n"
        "Ask a question. Jatnifier gets an answer from your chosen model and automatically "
        "polishes it before showing the final result."
    )
    with gr.Row():
        provider = gr.Dropdown(
            choices=list(PROVIDERS),
            value="Hugging Face",
            label="AI provider",
        )
        style = gr.Dropdown(
            choices=["general", "study", "concise", "technical"],
            value="general",
            label="Answer style",
        )
    api_key = gr.Textbox(
        label="API key (leave blank if using an environment variable or local model)",
        type="password",
        placeholder="Paste your Hugging Face or NVIDIA key",
    )
    model = gr.Textbox(
        label="Model name (optional)",
        placeholder="Leave blank to use the provider default",
    )
    question = gr.Textbox(
        label="Your question",
        placeholder="Ask anything...",
        lines=5,
    )
    run = gr.Button("Ask and polish", variant="primary")
    final_answer = gr.Markdown(label="Polished answer")
    with gr.Accordion("View original model answer", open=False):
        original_answer = gr.Markdown()
    run.click(
        answer_and_polish,
        inputs=[question, provider, api_key, model, style],
        outputs=[final_answer, original_answer],
    )


if __name__ == "__main__":
    # In Colab, launch with share=True in the notebook. Locally, use this file directly.
    demo.launch()
