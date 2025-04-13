from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load the LLM using OpenRouter with simplified configuration
model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-3.5-turbo"  # Using a model supported by OpenRouter
)

# Prompt template customized for CVE Q&A
template = """
You are a cybersecurity expert trained to answer questions about software vulnerabilities using CVE data.

Here are some relevant CVE entries: 
{reviews}

Here is the question to answer: 
{question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Interactive Q&A loop
while True:
    print("\n\n-------------------------------")
    question = input("Ask your cybersecurity question (q to quit): ")
    print("\n\n")
    if question.lower() == "q":
        break
    
    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews": reviews, "question": question})
    print(result.content)
