from flask import Flask, render_template, request, session
import markdown
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session

# Load model using OpenRouter with simplified configuration
model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-3.5-turbo"  # Using a model supported by OpenRouter
)

template = """
You are a cybersecurity expert trained to answer questions about software vulnerabilities using CVE data.

Format your answer using Markdown. Use clear **headings**, bullet points, and examples where possible.

Here are some relevant CVE entries: 
{reviews}

Here is the question to answer: 
{question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        question = request.form.get("question")
        if question:
            reviews = retriever.invoke(question)
            result = chain.invoke({"reviews": reviews, "question": question})
            answer = markdown.markdown(str(result.content), extensions=["extra", "nl2br"])

            session["chat_history"].append({"role": "user", "text": question})
            session["chat_history"].append({"role": "bot", "text": answer})
            session.modified = True

    return render_template("index.html", chat_history=session["chat_history"])

@app.route("/clear", methods=["GET"])
def clear():
    session.clear()
    return render_template("index.html", chat_history=[])


if __name__ == "__main__":
    # Use the port provided by Hugging Face Spaces or default to 7860
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
