# 🩺 RAG Based Medical Chatbot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge\&logo=python)

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge\&logo=fastapi)

![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge\&logo=streamlit)

![Pinecone](https://img.shields.io/badge/Pinecone-VectorDB-purple?style=for-the-badge)

![RAG](https://img.shields.io/badge/RAG-Powered-orange?style=for-the-badge)

![LLM](https://img.shields.io/badge/LLM-Groq-black?style=for-the-badge)

### AI Medical Assistant with PDF Understanding + Retrieval Augmented Generation

</div>

---

# ✨ Features

✅ Upload Medical PDFs
✅ Retrieve answers from uploaded documents
✅ Medical fallback knowledge mode
✅ Prevent non-medical hallucinations
✅ Vector Search using Pinecone
✅ Modern Streamlit UI
✅ Chat History Support
✅ FastAPI REST Backend

---

# 🧠 Project Architecture

```text
                    USER

                     │

                     ▼

             Streamlit Frontend

                     │

                     ▼

            FastAPI Backend API

                     │

      ┌──────────────┴──────────────┐

      ▼                             ▼

Upload PDFs                  Ask Question

      │                             │

      ▼                             ▼

PDF Loader                  Embed Query

      │                             │

      ▼                             ▼

Chunking              Similarity Search

      │                             │

      ▼                             ▼

Embeddings                Pinecone DB

      │                             │

      └──────────────┬──────────────┘

                     ▼

              LLM Response

                     ▼

              Medical Answer
```

---

# 🚀 Project Flow

```text
Upload PDF
↓

Extract Text

↓

Chunk Documents

↓

Generate Embeddings

↓

Store in Pinecone

↓

Ask Question

↓

Retrieve Relevant Context

↓

Generate AI Response

↓

Show Answer
```

---

# 🧰 Tech Stack

| Layer     | Technology  |
| --------- | ----------- |
| Frontend  | Streamlit   |
| Backend   | FastAPI     |
| Embedding | HuggingFace |
| Vector DB | Pinecone    |
| LLM       | Groq        |
| RAG       | LangChain   |

---

# 📂 Folder Structure

```bash
RAG/

├── client/
│   ├── app.py
│   ├── components/
│   ├── utils/
│
├── server/
│   ├── routes/
│   ├── modules/
│   ├── middlewares/
│   ├── uploaded_docs/
│
├── README.md
├── requirements.txt
```

---

# ⚙ Installation

## Clone

```bash
git clone https://github.com/shristy-shahi/RAG_Based_Medical_Chatbot.git
```

## Backend

```bash
cd server

pip install -r requirements.txt

python -m uvicorn main:app --reload
```

---

## Frontend

```bash
cd client

streamlit run app.py
```

---

# 🔑 Environment Variables

Create:

```bash
server/.env
```

Add:

```env
PINECONE_API_KEY=

PINECONE_INDEX_NAME=

GROQ_API_KEY=
```

---

# 🧪 Example Questions

```text
What is diabetes?

Explain symptoms of hypertension

How is heart disease diagnosed?

What are risk factors?
```

---

# 📈 Future Improvements

☐ Voice Assistant
☐ Authentication
☐ Cloud Deployment
☐ Multi User Support
☐ Live Medical Search

---

# 👩‍💻 Author

**Shristy Shahi**

Built with ❤️ using RAG + FastAPI + Streamlit
