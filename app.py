
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="DocuChat Lite", page_icon="📄")

st.title("📄 DocuChat Lite")
st.caption("Ask questions about a document using AI.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "OpenAI API key",
        type="password",
        help="Your key is used for this session only."
    )

document = st.text_area(
    "Paste your document here",
    height=250,
    placeholder="Paste a report, article, or other text..."
)

question = st.text_input(
    "What would you like to know?",
    placeholder="Summarize the main points..."
)

if st.button("Ask AI", type="primary"):
    if not api_key:
        st.error("Enter your OpenAI API key in the sidebar.")
    elif not document.strip() or not question.strip():
        st.error("Enter both a document and a question.")
    else:
        try:
            client = OpenAI(api_key=api_key)

            with st.spinner("Reading your document..."):
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    instructions=(
                        "Answer using only the supplied document. "
                        "If the answer is not present, say so. "
                        "Briefly quote the supporting text when possible."
                    ),
                    input=(
                        f"DOCUMENT:\n{document}\n\n"
                        f"QUESTION:\n{question}"
                    )
                )

            st.subheader("Answer")
            st.write(response.output_text)

        except Exception as e:
            st.error(
                "The request failed. Check your API key, "
                "API access, available credits, and try again."
            )
            st.caption(str(e))
