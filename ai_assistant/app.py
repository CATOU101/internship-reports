from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

# Prompt templates
answer_question_prompts = [
    "Give a concise answer to the question: {question}",
    "You're a smart assistant. Answer this briefly: {question}",
    "Provide factual information in 2-3 sentences: {question}"
]

summarize_text_prompts = [
    "Summarize the following text: {text}",
    "List the key points from this article: {text}",
    "Give a short summary of this: {text}"
]

creative_content_prompts = [
    "Write a short fantasy story about: {idea}",
    "Create a poem on the theme: {idea}",
    "Invent a sci-fi concept based on: {idea}"
]

# Groq API
GROQ_API_KEY = "xxxxxxxxxxx" #Api Key
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_response(prompt):
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post(GROQ_API_URL, headers=HEADERS, json=data)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"].strip()
    return f"Error: {res.status_code}"

feedback_store = []  # In-memory list to store feedback

@app.route('/', methods=['GET', 'POST'])
def index():
    response = ''
    user_input = ''
    selected_function = ''
    if request.method == 'POST':
        selected_function = request.form['function']
        user_input = request.form['user_input']

        if selected_function == 'question':
            prompt = answer_question_prompts[0].format(question=user_input)
        elif selected_function == 'summary':
            prompt = summarize_text_prompts[0].format(text=user_input)
        elif selected_function == 'creative':
            prompt = creative_content_prompts[0].format(idea=user_input)
        else:
            prompt = ""

        if prompt:
            response = get_response(prompt)

    return render_template('index.html', response=response, user_input=user_input, selected_function=selected_function)

@app.route('/feedback', methods=['POST'])
def feedback():
    feedback = request.form.get('feedback')
    user_input = request.form.get('user_input')
    selected_function = request.form.get('selected_function')

    response_text = request.form.get('response')
    log_entry = f"""
    --- FEEDBACK ENTRY ---
    Function: {selected_function}
    Input: {user_input}
    Response: {response_text}
    Feedback: {feedback}
    ----------------------
    """

    # Append to file
    with open("feedback_log.txt", "a") as log_file:
        log_file.write(log_entry + "\n")

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

