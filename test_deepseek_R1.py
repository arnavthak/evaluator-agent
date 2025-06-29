from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')

openai = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com/v1")

request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaluate their intelligence. "
request += "Answer only with the question, no explanation."
message = [{"role": "user", "content": request}]

response = openai.chat.completions.create(
    model="deepseek-reasoner",
    messages=message,
)

result = response.choices[0].message.content

print(result)