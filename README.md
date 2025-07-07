# 🤖 Agentic Evaluator

This is a simple Streamlit web app that demonstrates agentic evaluation: an AI model generates a response to a prompt, another model evaluates its quality, and the generator iteratively improves its response based on feedback until a satisfactory answer is reached.

This workflow showcases how two LLMs — OpenAI's `gpt-4.1-nano` and DeepSeek's `deepseek-chat` — can collaborate in a loop of self-improvement and judgment.

---

## 🚀 Features

- User inputs a custom prompt.
- `gpt-4.1-nano` generates a response.
- `deepseek-chat` evaluates the response using structured JSON scoring and reasoning.
- If the response isn't perfect, feedback is sent back to the generator.
- This loop repeats up to 3 times or until a perfect response is achieved.
- Final answer is displayed on screen.

---

## 🔐 Setup

1. **Clone the repository** or save the script as `app.py`.

2. **Create a `.env` file** in the same directory with your API keys:

    ```env
    OPENAI_API_KEY=your-openai-api-key-here
    DEEPSEEK_API_KEY=your-deepseek-api-key-here
    ```

    Replace the placeholders with your actual keys.

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit app**:

    ```bash
    streamlit run app.py
    ```

    This will launch the app in your default browser.

---