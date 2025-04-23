import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
models = client.models.list()
print([m.id for m in models.data])
