
import streamlit as st
import streamlit.components.v1 as comp
st.title("MUTI MODAL SUMMARIZATION")
st.write("""Welcome to our website! We specialize in text, video, and audio summarization,
        providing our users with the most important and relevant information in a concise and easily digestible format.
        Our cutting-edge technology allows us to analyze large amounts of data and distill it into key points, saving our users time and effort.
          Whether you need to quickly catch up on a news article, a podcast, or a video lecture, our summarization tools are here to help. 
        Explore our website to learn more about our services and how they can benefit you.""")

import os
import nltk
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
nltk.data.path.append(os.path.abspath("nltk_data"))
#import itertools
intents = [
    {
        "tag": "greeting",
        "patterns": ["Hi", "Hello", "Hey", "How are you", "What's up"],
        "responses": ["Hi there", "Hello", "Hey", "I'm fine, thank you", "Nothing much"]
    },
    {
        "tag": "goodbye",
        "patterns": ["Bye", "See you later", "Goodbye", "Take care"],
        "responses": ["Goodbye", "See you later", "Take care"]
    },
    {
        "tag": "thanks",
        "patterns": ["Thank you", "Thanks", "Thanks a lot", "I appreciate it"],
        "responses": ["You're welcome", "No problem", "Glad I could help"]
    },
    {
        "tag": "about",
        "patterns": ["What can you do", "Who are you", "What are you", "What is your purpose"],
        "responses": ["I am a chatbot", "My purpose is to assist you", "I can answer questions and provide assistance"]
    },
    {
        "tag": "help",
        "patterns": ["Help", "I need help", "Can you help me", "What should I do"],
        "responses": ["Sure, what do you need help with?", "I'm here to help. What's the problem?", "How can I assist you?"]
    },
    {
        "tag": "age",
        "patterns": ["How old are you", "What's your age"],
        "responses": ["I don't have an age. I'm a chatbot.", "I was just born in the digital world.", "Age is just a number for me."]
    },
    {
        "tag": "weather",
        "patterns": ["What's the weather like", "How's the weather today"],
        "responses": ["I'm sorry, I cannot provide real-time weather information.", "You can check the weather on a weather app or website."]
    },
    {
        "tag": "Audio summarization",
        "patterns": ["How to do audio summarization"],
        "responses": ["it takes listen notes podcast episode id and gives you text summarization "]
    },
    {
        "tag": "Video summarization",
        "patterns": ["how to do video summarization"],
        "responses": ["Sorry its on the process"]
    },
    {
        "tag": "Text summarization",
        "patterns": ["How to do text summarization"],
        "responses": ["give a blog post link which you want to summarize"]
    }
]
# train a machine learning model
#create the vectorizer and classifier

# Create the vectorizer and classifier
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
tags = []
patterns = []
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

# training the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response

counter = 0
def main():
    global counter
    st.sidebar.title("Chatbot")
    st.sidebar.write("Welcome to the chatbot. Please type a message and press enter to start the conversation")

    counter += 1
    user_input = st.sidebar.text_input("You:",key = f"user_input_{counter}")

    if user_input:
        response = chatbot(user_input)
        st.sidebar.text_area("Chatbot:",value=response,height=100,max_chars =None,key=f"chatbot_response_{counter}")
        if response.lower() in ["goodbye","bye"]:
            st.sidebar.write("Thank you for chatting with me. Have a great day!")
            st.stop()

if __name__ == "__main__":
    main()



