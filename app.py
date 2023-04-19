import streamlit as st
import pandas as pd

from knowledge_base import KnowledgeBase

# Page setup
st.set_page_config(page_title="Website to AI-Powered Knowledge Base", page_icon="🐍")
st.title("AI-Powered Knowledge Base")

# Remove whitespace from the top of the page and sidebar
st.markdown(
    """
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
""",
    unsafe_allow_html=True,
)

st.markdown("## Config")

col1, col2 = st.columns(2)

with col1:
    sitemap_url = st.text_input("URL to the website sitemap", value="")

with col2:
    pattern = st.text_input("URL filter pattern (optional)", value="")


st.markdown("## Ask")


@st.cache_resource
def get_knowledge_base(url, pattern):
    return KnowledgeBase(
        sitemap_url=url,
        pattern=pattern,
        chunk_size=8000,
        chunk_overlap=3000,
    )


@st.cache_resource
def get_answer(url, pattern, query):
    kb = get_knowledge_base(sitemap_url, pattern)
    return kb.ask(query)


if sitemap_url and pattern:
    with st.spinner("Getting the knowledge base ready, this may take a bit ..."):
        kb = get_knowledge_base(sitemap_url, pattern)

    query = st.text_input("Question", value="")

    if query:
        with st.spinner("Getting the answer ..."):
            result = get_answer(sitemap_url, pattern, query)

        st.markdown("### Answer")
        st.markdown(result["answer"])
        st.markdown("### Sources")
        st.markdown("\n ".join([f"- {x}" for x in result["sources"].split("\n")]))
