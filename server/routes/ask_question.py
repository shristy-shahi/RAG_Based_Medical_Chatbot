from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_core.retrievers import BaseRetriever
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
import os
router = APIRouter()
@router.post("/ask/")
async def ask_question(question: str = Form(...)):

    try:

        logger.info(f"user query: {question}")

        # ------------------------
        # PINECONE
        # ------------------------

        pc = Pinecone(
            api_key=os.environ["PINECONE_API_KEY"]
        )

        index = pc.Index(
            os.environ["PINECONE_INDEX_NAME"]
        )

        embed_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        embedded_query = embed_model.embed_query(
            question
        )

        res = index.query(
            vector=embedded_query,
            top_k=3,
            include_metadata=True
        )

        docs = [

            Document(
                page_content=match["metadata"].get(
                    "text",
                    ""
                ),

                metadata=match["metadata"]

            )

            for match in res["matches"]

        ]

        # ------------------------
        # RETRIEVER
        # ------------------------

        class SimpleRetriever(
            BaseRetriever
        ):

            tags: Optional[
                List[str]
            ] = Field(
                default_factory=list
            )

            metadata: Optional[
                dict
            ] = Field(
                default_factory=dict
            )

            def __init__(
                self,
                documents
            ):

                super().__init__()

                self._docs = documents

            def _get_relevant_documents(
                self,
                query
            ):

                return self._docs


        # ------------------------
        # CASE 1
        # PDF FOUND
        # ------------------------

        if docs and any(
            d.page_content.strip()
            for d in docs
        ):

            retriever = SimpleRetriever(
                docs
            )

            chain = get_llm_chain(
                retriever
            )

            result = query_chain(
                chain,
                question
            )

            return {

                "response":
                result["result"],

                "mode":
                "📄 PDF Knowledge",

                "sources":[

                    d.page_content[:300]

                    for d in docs

                ]
            }


        # ------------------------
        # CASE 2
        # FALLBACK MEDICAL
        # ------------------------

        from langchain_groq import ChatGroq

        llm = ChatGroq(

            groq_api_key=
            os.environ[
                "GROQ_API_KEY"
            ],

            model=
            "llama-3.3-70b-versatile"
        )

        prompt = f"""
You are a medical assistant.

Rules:
- Answer only medical questions.
- If not medical → politely refuse.
- Keep answer concise.

Question:
{question}
"""

        response = llm.invoke(
            prompt
        )

        return {

            "response":
            response.content,

            "mode":
            "🩺 Medical Knowledge",

            "sources":[]
        }


    except Exception as e:

        logger.exception(
            "Error processing question"
        )

        return JSONResponse(

            status_code=500,

            content={

                "error":
                str(e)
            }
        )