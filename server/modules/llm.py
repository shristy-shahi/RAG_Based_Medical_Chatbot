from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
def get_llm_chain(retriever):
    llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),

    model="llama-3.3-70b-versatile",

    temperature=0.6,

    max_tokens=1500
    )
    prompt = PromptTemplate(
input_variables=["context","question"],

template="""

You are MediBot 🩺

You are an AI Medical Assistant.

Your goal:
Provide detailed, structured, easy-to-understand medical explanations.

Use uploaded documents FIRST.

If context contains relevant information:
→ Answer primarily using context.

If context is insufficient:
→ Use your general medical knowledge.

Rules:

1. Answer in a friendly professional tone.

2. Structure response:

# Overview

# Key Points

# Symptoms (if applicable)

# Causes

# Treatment / Management

# Important Notes

3. Use bullet points.

4. Explain terms simply.

5. Give examples if useful.

6. Keep response informative and moderately detailed.

7. Never invent facts.

8. If uncertain say:
"Please consult a healthcare professional."

--------------------------------

DOCUMENT CONTEXT:
{context}

--------------------------------

QUESTION:
{question}

--------------------------------

FINAL ANSWER:

"""
)
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt":prompt},
        return_source_documents=True
    )