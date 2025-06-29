from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv(override=True)

deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

deepseek = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com/v1")
openai = OpenAI(api_key=openai_api_key)

prompt = input("Please enter your prompt: ")
generator_message = [{"role": "user", "content": prompt}]

generator_response = openai.chat.completions.create(
    model="gpt-4.1-nano",
    messages=generator_message,
)

generator_result = generator_response.choices[0].message.content

print(generator_result)

while True:
    evaluator_prompt = f"""
    The following prompt was given to OpenAI's o3-mini model:

    {prompt}

    And it gave out the following response:

    {generator_result}

    Do you think this result is perfect or not? Provide your reasoning.

    Now respond with a JSON with two keys: "perfect" and "reasoning". In "perfect", have the value be either "y" for yes or "n" for no. In "reasoning", have the value be your reasoning for why you think the result o3-mini gave was perfect or not.

    Do not add anything besides that JSON to the response. Do not include markdown formatting or code blocks.
    """

    message = [{"role": "user", "content": evaluator_prompt}]

    evaluator_response = deepseek.chat.completions.create(
        model="deepseek-reasoner",
        messages=message,
    )

    evaluator_result = evaluator_response.choices[0].message.content

    print(evaluator_result)

    json_evaluator_result = json.loads(evaluator_result)

    if json_evaluator_result["perfect"] == "y":
        print(f"Final Answer: \n{generator_result}")
        break
    
    generator_prompt = f"""
    This prompt was originally given to you:

    {prompt}

    And your response was:

    {generator_result}

    Your response was not deemed perfect by the evaluator and this was the reasoning as to why:

    {json_evaluator_result["reasoning"]}

    Write a new response to the original prompt given to you by taking into account the feedback on your prior response by the evaluator.
    """

    generator_message = [{"role": "user", "content": generator_prompt}]

    generator_response = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=generator_message,
    )

    generator_result = generator_response.choices[0].message.content

    print(generator_result)

        
    
