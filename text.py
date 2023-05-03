import streamlit as st
import pickle
#model = pickle.load(open("text_summarizer.pkl","rb"))
from transformers import pipeline
summarizer = pipeline('summarization')
from bs4 import BeautifulSoup
import requests

st.title("Text Summarizer")
URL = st.text_input("Enter the URL of the blog post")

if st.button("SUMMARIZE"):
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all(['h1', 'p'])
    text = [result.text for result in results]
    ARTICLE = ' '.join(text)
    max_chunk = 500
    ARTICLE = ARTICLE.replace('.', '.<eos>')
    ARTICLE = ARTICLE.replace('?', '?<eos>')
    ARTICLE = ARTICLE.replace('!', '!<eos>')
    sentences = ARTICLE.split('<eos>')


    current_chunk = 0 
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            print(current_chunk)
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])

    res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)
    text = ' '.join([summ['summary_text'] for summ in res])
    st.write(text)
