from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load CVE dataset
df = pd.read_csv("cve.csv")

# Set up the embedding model using HuggingFace with a fully qualified model name
# Using a simpler model that's more compatible with Hugging Face Spaces
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",  # Smaller, more compatible model
    model_kwargs={'device': 'cpu'}  # Ensure it runs on CPU for compatibility
)

# Directory for the vector store - use /tmp for proper permissions in containerized environments
db_location = "/tmp/chrome_langchain_db"
add_documents = not os.path.exists(db_location)

# Initialize Chroma DB
vector_store = Chroma(
    collection_name="cve_data",
    persist_directory=db_location,
    embedding_function=embeddings
)

# Add documents only if DB doesn't exist yet
if add_documents:
    documents = []
    ids = []

    for i, row in df.iterrows():
        # Replace with actual column names in your CSV
        cve_id = row.get("CVE_ID", f"CVE-{i}")
        description = row.get("Description", "")
        date = row.get("PublishedDate", "")

        content = f"CVE ID: {cve_id}\nDescription: {description}\nPublished Date: {date}"
        
        document = Document(
            page_content=content,
            metadata={"published_date": date},
            id=str(i)
        )

        documents.append(document)
        ids.append(str(i))

    vector_store.add_documents(documents=documents, ids=ids)

# Create retriever from the vector store
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
