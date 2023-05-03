# AI-Powered Knowledge Base

[Demo](https://user-images.githubusercontent.com/19983429/235894528-9ad791a8-f2f0-4ad8-a2fc-69f4ed0aa8d8.mp4)

This repository contains an AI-powered knowledge base that utilizes the LLMs model to answer questions based on a given website's content and **provide sources as links** to the relevant pages. 

The system:
1. Loads the website's content using a **sitemap**
2. Split each web page into **chunks**
4. **Embed** each chunk using a LLM (for now OpenAI) and store them in the **Chroma vector database
5. Then it embeds the user query and run a similarity search using the Chroma database
5. Finally it loads the similarity search results as context for a LLM (for now ChatGPT) to find relevant answers and citing the sources

It also provides a Streamlit-based web interface for an easy-to-use experience.

## Files

- `knowledge_base.py`: The main module that creates the KnowledgeBase class. This class is responsible for loading and processing the website content, creating the document index, and querying the LLM model for answers.
- `app.py`: A Streamlit web application that provides a user interface for querying the AI-powered knowledge base.

## Installation

1. Clone the repository:

```
git clone git@github.com:bitswired/website-to-knowledge-base.git
```

2. Instal the project with poetry:

```
poetry install
```

## Usage

### Knowledge Base

To use the KnowledgeBase class, follow these steps:

1. Import the KnowledgeBase class:

```python
from knowledge_base import KnowledgeBase
```

2. Instantiate the KnowledgeBase with the appropriate sitemap URL and pattern (optional):

```python
kb = KnowledgeBase(
    sitemap_url="https://nextjs.org/sitemap.xml",
    pattern="docs/api-refe",
    chunk_size=8000,
    chunk_overlap=3000,
)
```

3. Ask a question:

```python
result = kb.ask("How do I deploy my Next.js app?")
print(result)
```

### Web Application

To run the Streamlit web application, execute the following command in your terminal:

```
streamlit run app.py
```

The web app will open in your default browser. Enter the URL to the website's sitemap, an optional filter pattern for the URLs, and your question. The AI-powered knowledge base will return an answer based on the content of the website.

## Requirements

- An API key for OpenAI's GPT-4 (see [OpenAI's API documentation](https://beta.openai.com/docs/) for details)

## License

This project is licensed under the MIT License.
