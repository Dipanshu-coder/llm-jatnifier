"""Use an OpenAI-compatible endpoint exposed from Colab or another machine.

Keep endpoints private/authenticated. Do not expose a model server publicly without
appropriate access controls.
"""
import os
from llm_output_polisher import Polisher

polisher = Polisher(
    base_url=os.environ["POLISHER_BASE_URL"],  # typically ends with /v1
    model=os.getenv("POLISHER_MODEL", "your-model-name"),
    api_key=os.getenv("POLISHER_API_KEY", "EMPTY"),
)
print(polisher.polish("raw model response goes here", profile="general"))
