print("load_vectorstore.py started")
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

print("GOOGLE_API_KEY:", GOOGLE_API_KEY)
print("PINECONE_API_KEY:", PINECONE_API_KEY)

PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = "medicalindex"

if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    
UPLOAD_DIR="./uploaded_docs"
os.makedirs(UPLOAD_DIR,exist_ok=True)


# initialize pinecone instance
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY missing in .env")

# pc = Pinecone(api_key=PINECONE_API_KEY)
# spec=ServerlessSpec(cloud="aws",region=PINECONE_ENV)
# existing_indexes=[i["name"] for i in pc.list_indexes()]
# existing_indexes = pc.list_indexes().names()
pc = Pinecone(api_key=PINECONE_API_KEY)

spec = ServerlessSpec(
    cloud="aws",
    region=PINECONE_ENV
)

existing_indexes = pc.list_indexes().names()

if PINECONE_INDEX_NAME in existing_indexes:
    pc.delete_index(PINECONE_INDEX_NAME)
    time.sleep(5)

pc.create_index(
    name=PINECONE_INDEX_NAME,
    dimension=384,
    metric="dotproduct",
    spec=spec
)

while not pc.describe_index(PINECONE_INDEX_NAME).status.ready:
    time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)
# load,split,embed and upsert pdf docs content
print("before function")
def load_vectorstore(uploaded_files):
    embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    file_paths = []
    #1. upload
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))
    #2. split
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]
        #3.Embedding
        print(f"🔍 Embedding {len(texts)} chunks...")
        embeddings = embed_model.embed_documents(texts)
        #4.upsert
        print("📤 Uploading to Pinecone...")
        with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
            index.upsert(vectors=zip(ids, embeddings, metadatas))
            progress.update(len(embeddings))

        print(f"✅ Upload complete for {file_path}")