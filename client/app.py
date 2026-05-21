# import streamlit as st

# st.set_page_config(
#     page_title="AI Medical Assistant",
#     layout="wide"
# )

# st.title("🩺 Medical Assistant Chatbot")

# st.write("Streamlit is working successfully!")

# question = st.text_input("Ask your medical question")

# if st.button("Submit"):
#     st.success(f"You asked: {question}")
# import streamlit as st
# from components.upload import render_uploader
# from components.history_download import render_history_download
# from components.chatUI import render_chat


# st.set_page_config(page_title="AI Medical Assistant",layout="wide")
# st.title(" 🩺 Medical Assistant Chatbot")


# render_uploader()
# render_chat()
# render_history_download()
import streamlit as st
import requests

# -------------------------
# PAGE
# -------------------------

st.set_page_config(
    page_title="🩺 Medical Assistant",
    layout="wide"
)

# -------------------------
# UI STYLE
# -------------------------

st.markdown("""
<style>

.stApp{
background:
linear-gradient(
135deg,
#071019,
#0B1220,
#111827
);

color:white;
}

.main-title{
font-size:52px;
font-weight:700;
text-align:center;
}

.subtitle{
text-align:center;
color:#9CA3AF;
margin-bottom:30px;
}

[data-testid="stSidebar"]{
background:#0F172A;
}

.stButton button{

width:100%;

height:50px;

background:
linear-gradient(
90deg,
#6366F1,
#06B6D4
);

border:none;

color:white;

font-size:18px;

border-radius:14px;

}

.answer-card{

padding:25px;

background:#0B1220;

border-radius:18px;

border:1px solid #24324d;

line-height:1.8;

font-size:18px;

}

</style>
""",
unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------

st.markdown("""
<div class='main-title'>
🩺 Medical Assistant
</div>

<div class='subtitle'>
Upload PDFs • Ask Questions • AI Answers
</div>
""",
unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------

with st.sidebar:

    st.header("📄 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Upload Medical PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("🚀 Upload Documents"):

        if uploaded_files:

            files=[]

            for f in uploaded_files:

                files.append(
                    (
                        "files",
                        (
                            f.name,
                            f.getvalue(),
                            "application/pdf"
                        )
                    )
                )

            try:

                with st.spinner(
                    "Uploading..."
                ):

                    response=requests.post(
                        "http://127.0.0.1:8000/upload_pdfs/",
                        files=files
                    )

                if response.status_code==200:

                    st.success(
                        "PDF Uploaded Successfully"
                    )

                else:

                    st.error(
                        response.text
                    )

            except Exception as e:

                st.error(
                    str(e)
                )

# -------------------------
# CHAT
# -------------------------

st.markdown(
"## 💬 Chat"
)

question=st.text_input(
"Ask your medical question"
)

if st.button(
"Ask AI"
):

    if question:

        try:

            with st.spinner(
                "Thinking..."
            ):

                response=requests.post(

                    "http://127.0.0.1:8000/ask/",

                    data={
                        "question":
                        question
                    }
                )

                result=response.json()

                answer=result.get(
                    "response",
                    "No response"
                )

                mode=result.get(
                    "mode",
                    ""
                )

                st.markdown(
f"### {mode}"
)

                st.markdown(
f"""
<div class='answer-card'>
{answer}
</div>
""",
unsafe_allow_html=True
)

                if result.get(
                    "sources"
                ):

                    st.markdown(
                        "### 📚 Sources"
                    )

                    for i,src in enumerate(
                        result["sources"],
                        1
                    ):

                        with st.expander(
                            f"Source {i}"
                        ):

                            st.write(
                                src
                            )

        except Exception as e:

            st.error(
                str(e)
            )