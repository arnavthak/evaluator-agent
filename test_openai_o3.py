from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')

openai = OpenAI(api_key=openai_api_key)

request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaluate their intelligence. "
request += "Answer only with the question, no explanation."
message = [{"role": "user", "content": request}]

response = openai.chat.completions.create(
    model="o3-mini",
    messages=message,
)

result = response.choices[0].message.content

print(result)