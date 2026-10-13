from llm_output_polisher import Polisher

# Example using Ollama. Change the model to one installed locally.
polisher = Polisher(
    base_url="http://localhost:11434/v1",
    model="qwen2.5:3b",
    api_key="ollama",
)

raw_output = """
photosynthesis is process plants use sunlight and co2 water to make glucose oxygen
it happens in chloroplasts chlorophyll captures light
"""
print(polisher.polish(raw_output, profile="study"))
