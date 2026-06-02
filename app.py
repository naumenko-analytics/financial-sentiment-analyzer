import streamlit as st
from components.news_fetcher import fetch_news
from components.rag_pipeline import build_vectorstore, analyze_sentiment
from utils.helpers import format_date, truncate_text, validate_company_input

# Streamlit page configuration
st.set_page_config(page_title="Financial Sentiment Analyzer", layout='wide')

# Header
st.title('Financial News Sentiment Analyzer')
st.markdown('*Powered by RAG, LangChain, and OpenAI GPT*')
st.divider()

# Sidebar
with st.sidebar:
    st.header('Settings')
    num_articles = st.slider("Number of articles to analyze", 5, 20, 10)
    st.divider()
    st.markdown('**How it works:**')
    st.markdown('1. Fetches recent news via NewsAPI')
    st.markdown('2. Builds a FAISS vector database')
    st.markdown('3. Uses RAG to find relevant context')
    st.markdown('4. GPT analyzes sentiment and returns insights')

# Main input
company = st.text_input("Enter a company name", placeholder="Apple, Tesla, Microsoft, ...")
analyze_button = st.button("Analyze Sentiment", type='primary')

# Analysis
if analyze_button:
    is_valid, error_msg = validate_company_input(company)

    if not is_valid:
        st.error(error_msg)
    else:
        with st.spinner(f'Fetching latest news about {company}...'):
            articles = fetch_news(company, num_articles)

        if not articles:
            st.warning(f"No articles found for '{company}'. Try a different company name.")
        
        else:
            with st.spinner('Building knowledge base and analyzing sentiment ...'):
                vectorstore = build_vectorstore(articles)
                result = analyze_sentiment(vectorstore, company)

            # Results
            st.success(f'Analysis complete - {len(articles)} articles analyzed')
            st.divider()

            col1, col2 = st.columns([2,1])

            with col1:
                st.subheader('Sentiment Analysis')
                st.markdown(result)

            with col2:
                st.subheader('Articles Analyzed')
                for article in articles:
                    st.markdown(f'**{truncate_text(article['title'], 80)}**')
                    st.caption(f'{article['source']} - {format_date(article['publishedAt'])}')
                    st.markdown(f'[Read more]({article['url']})')
                    st.divider()