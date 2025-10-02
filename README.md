# 🔬 Scientific Research Agent

This project is a powerful, local-first RAG (Retrieval-Augmented Generation) application designed to answer complex questions about a collection of scientific research papers. It leverages llmware for state-of-the-art document processing, Groq for ultra-fast LLM inference, and Streamlit for a clean, interactive user interface.



## 🌟 Features

- **Easy Document Upload**: Upload multiple research papers (PDF, DOCX, TXT) directly through the web interface.
    
- **Automated RAG Pipeline**: Handles parsing, smart chunking, and vector embedding of your documents automatically.
    
- **High-Performance Search**: Uses llmware and a local ChromaDB vector store to perform fast and accurate semantic searches.
    
- **Blazing-Fast Answers**: Integrates with the Groq LPU™ Inference Engine to generate answers from a powerful LLM (Llama 3.3 70B) with minimal latency.
    
- **User-Friendly Interface**: A simple, intuitive UI built with Streamlit that guides you through uploading documents and asking questions.
    
- **Efficient Caching**: Caches the document library after initial processing for near-instant reloads.
    

## ⚙️ How It Works

The application follows a standard RAG pipeline:

1. **Upload & Process**: You upload your scientific papers through the sidebar. When you click "Process", the application uses llmware to parse the files, break them into intelligent chunks, and generate vector embeddings using the jina-embeddings-v2-small-en model.
    
2. **Store**: These embeddings are stored locally in a ChromaDB vector database, creating a searchable knowledge library.
    
3. **Query & Retrieve**: When you ask a question, the application converts your query into a vector and performs a semantic search against the database to find the most relevant text chunks from your documents.
    
4. **Synthesize & Answer**: The retrieved context chunks and your original question are sent to the Groq API. A large language model (Llama 3.3 70B) then synthesizes this information to provide a comprehensive and accurate answer, based only on the provided documents.
    

## 🛠️ Tech Stack

- **Backend**: Python
    
- **Document Processing & RAG**: llmware
    
- **Vector Database**: ChromaDB (managed by llmware)
    
- **LLM Inference**: Groq
    
- **Web Framework**: Streamlit
    
- **Environment Management**: python-dotenv
    

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### 1. Prerequisites

- Python 3.9 or higher.
    
- A free [Groq API Key](https://www.google.com/url?sa=E&q=https%3A%2F%2Fconsole.groq.com%2Fkeys).
    

### 2. Installation

1. **Clone the Repository**
    
    ```Bash
    git clone <your-repository-url>
    cd <repository-folder-name>
    ```
    
2. **Create and Activate a Virtual Environment**  
    It's highly recommended to use a virtual environment to manage dependencies.
    

    
    ```
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate
    
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
    
3. **Install Dependencies**  
    The requirements.txt file contains all necessary packages. Install them using pip:
    
    
    ```
    pip install -r requirements.txt
    ```
    
4. **Set Up Environment Variables**  
    Create a file named .env in the root of your project directory. Add your Groq API key to this file:
    
    
    ```
    GROQ="gsk_YourSecretGroqApiKeyGoesHere"
    ```
    
    (Note: The .gitignore file is already set up to prevent this file from being committed to your repository.)
    

### 3. Running the Application

1. **Launch the Streamlit App**  
    Run the following command in your terminal from the project's root directory:
    
    
    ```
    streamlit run main.py
    ```
    
2. Your default web browser should automatically open a new tab with the application running.
    

## 📖 Usage Guide

1. **Upload Documents**: On the left sidebar, use the file uploader to select the scientific papers you want to include in your knowledge base.
    
2. **Process & Embed**: Once your files are uploaded, click the **"Process & Embed Documents"** button. This will take a few moments as the system parses the files and generates embeddings. You will see status messages and a success animation upon completion.
    
3. **Ask a Question**: In the main area of the page, type your question into the text input field.
    
4. **Get Answer**: Click the **"Get Answer"** button. The application will perform a search and use the Groq LLM to generate a detailed answer based on the retrieved context.
    

## 🔧 Configuration

You can easily customize the core components of the RAG pipeline by modifying the configuration constants at the top of the main.py script:

```Python


# --- CONFIGURATION ---
LIBRARY_NAME = "scientific_papers_lib"
RESEARCH_PAPERS_PATH = "./research_papers"
EMBEDDING_MODEL = "jinaai/jina-embeddings-v2-small-en"
LLM_MODEL = "llama-3.3-70b-versatile"
```