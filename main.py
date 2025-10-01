import os
import shutil
import dotenv
import streamlit as st
from llmware.library import Library
from llmware.retrieval import Query
from groq import Groq

# --- CONFIGURATION ---
LIBRARY_NAME = "scientific_papers_lib"
RESEARCH_PAPERS_PATH = "./research_papers"
EMBEDDING_MODEL = "jinaai/jina-embeddings-v2-small-en"
LLM_MODEL = "llama-3.3-70b-versatile"


# --- BACKEND LOGIC (from your code) ---

# Use Streamlit's cache to load the library only once
@st.cache_resource
def setup_library(library_name: str):
    """
    Loads the llmware library if it exists.
    """
    st.write(f"Loading library: {library_name}...")
    # Make sure the base library folder exists
    if not os.path.exists(os.path.join(os.path.expanduser('~'), 'llmware', 'library')):
        os.makedirs(os.path.join(os.path.expanduser('~'), 'llmware', 'library'))

    library = Library().load_library(library_name)
    st.success(f"Library '{library_name}' loaded successfully.")
    return library


def process_and_embed_files(library_name: str, folder_path: str):
    """
    Creates a new library, adds files, and generates embeddings from a folder.
    This function is intended for one-time setup or reprocessing.
    """
    st.info(f"Creating a new library: '{library_name}'. This may take a moment...")

    # Clear out the old library directory if it exists to ensure a fresh start
    library_path = os.path.join(os.path.expanduser('~'), 'llmware', 'library', library_name)
    if os.path.exists(library_path):
        shutil.rmtree(library_path)

    library = Library().create_new_library(library_name)

    st.write(f"Parsing and chunking files from: {folder_path}...")
    library.add_files(input_folder_path=folder_path, chunk_size=400, max_chunk_size=600, smart_chunking=1)

    st.write(f"Creating embeddings with model: {EMBEDDING_MODEL}...")
    library.install_new_embedding(embedding_model_name=EMBEDDING_MODEL, vector_db="chromadb")

    st.success("Library setup and embedding complete.")
    st.balloons()
    # Rerun to clear the "processing" state and load the new library
    st.rerun()


def semantic_search(library: Library, user_query: str, result_count: int = 20) -> list:
    """
    Performs a semantic query on the library.
    """
    with st.spinner(f"Performing semantic search for: '{user_query}'..."):
        query_results = Query(library).semantic_query(user_query, result_count=result_count)
    return query_results


def ask_groq(user_prompt: str, model: str) -> str:
    """
    Sends a prompt to the Groq API and returns the model's response.
    """
    api_key = os.environ.get("GROQ")
    if not api_key:
        return "Error: GROQ environment variable not set. Please add it to your .env file."

    client = Groq(api_key=api_key)

    try:
        with st.spinner("Calling Groq's LPU to synthesize the answer..."):
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": user_prompt}],
                model=model,
            )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error during Groq API call: {e}")
        return ""


# --- STREAMLIT FRONTEND ---

st.set_page_config(layout="wide", page_title="Scientific Research Agent")

st.title("🔬 Scientific Research Agent")
st.markdown("Powered by `llmware` for RAG, `Groq` for high-speed inference, and `Streamlit` for the UI.")

# Load environment variables
dotenv.load_dotenv()

# --- SIDEBAR FOR FILE MANAGEMENT ---
with st.sidebar:
    st.header("📚 Document Setup")
    st.write("Upload your scientific papers here. The system will process them into a searchable library.")

    uploaded_files = st.file_uploader(
        "Upload research papers (PDF, DOCX, TXT)",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt']
    )

    if uploaded_files:
        # Create the folder if it doesn't exist
        if not os.path.exists(RESEARCH_PAPERS_PATH):
            os.makedirs(RESEARCH_PAPERS_PATH)

        # Save uploaded files to the folder
        for file in uploaded_files:
            with open(os.path.join(RESEARCH_PAPERS_PATH, file.name), "wb") as f:
                f.write(file.getbuffer())
        st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")

    if st.button("Process & Embed Documents"):
        if not os.listdir(RESEARCH_PAPERS_PATH):
            st.warning("No files found in the research_papers folder. Please upload documents first.")
        else:
            # This will create and embed, then trigger a rerun
            process_and_embed_files(LIBRARY_NAME, RESEARCH_PAPERS_PATH)

# --- MAIN CHAT INTERFACE ---
try:
    # Attempt to load the library
    library = setup_library(LIBRARY_NAME)

    st.header("❓ Ask a Question")
    st.write("Pose a question to the agent based on the documents you provided.")

    user_query = st.text_input("Enter your scientific question:", "")

    if st.button("Get Answer"):
        if not user_query:
            st.warning("Please enter a question.")
        else:
            # 1. Retrieve context
            query_results = semantic_search(library, user_query)

            if not query_results:
                st.error("Could not find any relevant information in the provided documents for your query.")
            else:
                # 2. Assemble the prompt
                prompt_template = """You are a world-renowned scientific genius. Your intellect is unparalleled.
Based *only* on the provided context from research papers, provide a clear, concise, and accurate answer to the query.
If the context does not contain the answer, state that clearly.
Format your response in neatly structured markdown.

Context:
{context}

Query:
{query}

Reply:
"""
                context = "\n---\n".join([result['text'] for result in query_results[:7]])  # Use top 7 results
                final_prompt = prompt_template.format(context=context, query=user_query)

                # 3. Get the final answer
                answer = ask_groq(final_prompt, model=LLM_MODEL)

                st.subheader("💡 Answer")
                st.markdown(answer)

except Exception as e:
    st.error(f"Failed to load or find the library: '{LIBRARY_NAME}'.")
    st.info("Please upload documents and click 'Process & Embed Documents' in the sidebar to create the library.")
    st.warning(f"Detailed Error: {e}")