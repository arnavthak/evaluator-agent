import streamlit as st
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

deepseek = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com/v1")
openai = OpenAI(api_key=openai_api_key)

st.set_page_config(page_title="Agentic Evaluator", layout="centered")

st.title("Agentic Evaluator 🤖🔁")

prompt = st.text_area("Enter your question or prompt:", height=150)

if st.button("Submit"):
    with st.spinner("Generating and evaluating response..."):
        generator_message = [{"role": "user", "content": prompt}]

        generator_response = openai.chat.completions.create(
            model="gpt-4.1-nano",
            messages=generator_message,
        )
        generator_result = generator_response.choices[0].message.content

        generator_message = [
            {"role": "system", "content": "You are a helpful assistant who improves your responses based on external feedback."},
            {"role": "user", "content": prompt},
            {"role": "assistant", "name": "gpt-4.1-nano", "content": generator_result}
        ]

        responses = dict()
        final_result = ""

        while len(responses) <= 3:
            evaluator_prompt = f"""
            The following prompt was given to OpenAI's gpt-4.1-nano model:

            {prompt}

            And it gave out the following response:

            {generator_result}

            Do you think this response is perfect or not? Provide your reasoning. Rate how good the response is out of 10, 0 is completely incorrect and 10 is a perfect response. The score should be a decimal rounded to the hundredth place.

            Now respond with a JSON with three keys: "perfect", "reasoning", and "score". In "perfect", have the value be either "y" for yes or "n" for no. In "reasoning", have the value be your reasoning for why you think the result gpt-4.1-nano gave was perfect or not. In "score", have the value be only a decimal number 0-10 that represents how good the response was according to the scale I mentioned earlier.

            Do not add anything besides that JSON to the response. 
            Do not include markdown formatting or code blocks.
            Ensure this is machine-parsable.
            """

            message = [
                {"role": "system", "content": "You are a JSON API. All outputs must be valid JSON and must not contain any commentary, Markdown, or extra formatting. This will be parsed by a script, so any deviation from JSON will cause errors."},
                {"role": "user", "content": evaluator_prompt}
            ]

            evaluator_response = deepseek.chat.completions.create(
                model="deepseek-chat",
                messages=message,
                response_format={'type': 'json_object'}
            )

            evaluator_result = evaluator_response.choices[0].message.content
            json_evaluator_result = json.loads(evaluator_result)
            responses[generator_result] = float(json_evaluator_result["score"])

            if json_evaluator_result["perfect"] == "y":
                final_result = generator_result
                break

            if len(responses) == 3:
                final_result = max(responses, key=responses.get)
                break

            generator_prompt = f"""
            This prompt was originally given to you:

            {prompt}

            And your response was:

            {generator_result}

            Your response was not deemed perfect by the deepseek-chat evaluator model and this was the reasoning as to why:

            {json_evaluator_result["reasoning"]}

            Write a new response to the original prompt given to you by taking into account the feedback on your prior response by the deepseek-chat evaluator model.
            """

            generator_message.append({"role": "assistant", "name": "deepseek-chat", "content": evaluator_result})
            generator_message.append({"role": "user", "content": generator_prompt})

            generator_response = openai.chat.completions.create(
                model="gpt-4.1-nano",
                messages=generator_message,
            )

            generator_result = generator_response.choices[0].message.content
            generator_message.append({"role": "assistant", "name": "gpt-4.1-nano", "content": generator_result})

        st.subheader("Final Answer")
        st.write(final_result)
