

import streamlit as st
import streamlit.components.v1 as components
API_KEY_ASSEMBLYAI = "33b0c6db31c3413d95d47337eec86052"
API_KEY_LISTENNOTES = "defab91db9fe4748972e6e003d676c1a"

import requests
import time
import pprint
from transformers import pipeline
summarizer = pipeline('summarization')


transcribe_endpoint = "https://api.assemblyai.com/v2/transcript"
#headers is for authentication
assemblyai_headers = {"authorization":API_KEY_ASSEMBLYAI}


listennotes_episode_endpoint = "https://listen-api.listennotes.com/api/v2/episodes"
listennotes_headers = {"X-ListenAPI-Key":API_KEY_LISTENNOTES}


def get_episode_audio_url(episode_id):
    url = listennotes_episode_endpoint + "/" + episode_id
    response =  requests.request('GET', url,headers = listennotes_headers)
    data = response.json()
    #pprint.pprint(data)

    audio_url = data['audio']
    episode_thumbnail = data['thumbnail']
    podcast_title = data['podcast']['title']
    episode_title = data['title']
    return audio_url,episode_thumbnail,podcast_title,episode_title,podcast_title


#transcribe
def transcribe(audio_url):

    transcript_request = { "audio_url": audio_url }
    transcript_response = requests.post(transcribe_endpoint, json=transcript_request, headers=assemblyai_headers)
    job_id = transcript_response.json()['id']
    return job_id

#poll
def poll(transcript_id):
    polling_endpoint = transcribe_endpoint+ '/' +transcript_id
    polling_response = requests.get(polling_endpoint,headers = assemblyai_headers)
    return polling_response.json()

def get_transcription_url(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == "error":
            return data, "error"
        print("Waiting 30 seconds....")
        time.sleep(30)

#save
def save_transcript(episode_id):
    audio_url,episode_thumbnail,podcast_title,episode_title,podcast_title = get_episode_audio_url(episode_id)
    data,error = get_transcription_url(audio_url)
    audio = []
    if data:
        audio = data['text']
        return audio
    elif error:
        print("Error!!",error)

#summarize 
def summarize(text_data):
    sentences = text_data.split('.')
    max_chunk = 500
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
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])

    res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)
    text = ' '.join([summ['summary_text'] for summ in res])
    return text
st.title("Audio Summarizer")
input_  = st.text_input("please input a episode id")
if st.button("SUMMARIZE"):
    text_data = save_transcript(input_)
    result = summarize(text_data)
    st.write(result)

