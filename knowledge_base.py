from typing import Optional

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain

import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def extract_urls_from_sitemap(sitemap):
    """
    Extract all URLs from a sitemap XML string.

    Args:
        sitemap_string (str): The sitemap XML string.

    Returns:
        A list of URLs extracted from the sitemap.
    """
    # Parse the XML from the string
    root = ET.fromstring(sitemap)

    # Define the namespace for the sitemap XML
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    # Find all <loc> elements under the <url> elements
    urls = [
        url.find("ns:loc", namespace).text for url in root.findall("ns:url", namespace)
    ]

    # Return the list of URLs
    return urls


class KnowledgeBase:
    def __init__(
        self,
        sitemap_url: str,
        chunk_size: int,
        chunk_overlap: int,
        pattern: Optional[str] = None,
    ):
        logger.info("Building the knowledge base ...")

        logger.info("Loading sitemap from {sitemap_url} ...", sitemap_url=sitemap_url)
        sitemap = requests.get(sitemap_url).text
        urls = extract_urls_from_sitemap(sitemap)

        if pattern:
            logger.info("Filtering URLs with pattern {pattern} ...", pattern=pattern)
            urls = [x for x in urls if pattern in x]
        logger.info("{n} URLs extracted", n=len(urls))

        logger.info("Loading URLs content ...")
        loader = UnstructuredURLLoader(urls)
        data = loader.load()

        logger.info("Splitting documents in chunks ...")
        doc_splitter = CharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        docs = doc_splitter.split_documents(data)
        logger.info("{n} chunks created", n=len(docs))

        logger.info("Building the vector database ...")
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(docs, embeddings)

        logger.info("Building the retrieval chain ...")
        self.chain = RetrievalQAWithSourcesChain.from_chain_type(
            ChatOpenAI(),
            chain_type="map_reduce",
            retriever=docsearch.as_retriever(),
        )

        logger.info("Knowledge base created!")

    def ask(self, query: str):
        return self.chain({"question": query}, return_only_outputs=True)


if __name__ == "__main__":
    # Build the knowledge base
    kb = KnowledgeBase(
        sitemap_url="https://nextjs.org/sitemap.xml",
        pattern="docs/api-refe",
        chunk_size=8000,
        chunk_overlap=3000,
    )

    # Ask a question
    res = kb.ask("How do I deploy my Next.js app?")
