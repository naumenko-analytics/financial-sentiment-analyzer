import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def build_vectorstore(articles):
    """ Function that takes in articles and turns them into a FAISS vector database
    """
    # combine content and title for each article
    texts = []
    for article in articles:
        if not isinstance(article, dict):
            continue
        text = f"Title: {article.get('title', '')}\n\nContent: {article.get('content', '')}\n\nSource: {article.get('source', '')}\nDate: {article.get('publishedAt', '')}"
        texts.append(text)

    # split text into chuncks 
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500,chunk_overlap = 50)
    chunks = splitter.create_documents(texts)

    # create embeddings and store them in FAISS
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    return vectorstore

def analyze_sentiment(vectorstore, company):
    """ Run RAG pipeline to analyze sentiment about a company
    """
    # Define the prompt template
    prompt = ChatPromptTemplate.from_template("""
You are a financial analyst. Using the news articles provided below as context, analyze the overall market sentiment about {company}.

Context:
{context}

Provide:
1. Overall sentiment (Bullish / Bearish / Neutral)
2. Key themes from the news
3. Brief summary (3-5 sentences)
4. Confidence level (Low / Medium / High) based on the quality of articles

Answer:""")
    
    # Build LLM
    llm = ChatOpenAI(openai_api_key = OPENAI_API_KEY, model_name='gpt-3.5-turbo', temperature=0)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Build RAG chain
    chain = (
        {"context": retriever, "company": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(company)