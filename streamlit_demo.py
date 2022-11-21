import streamlit as st
from PIL import Image
from docarray import DocumentArray, Document
import json
import requests
from jina import Client
import os

os.environ['JINA_AUTH_TOKEN'] = '31454a8d0823445012c6de5623aed215'

# openimage dataset
# client = Client(host='grpcs://1f51c9f5b1.wolf.jina.ai')

# laion400m
# client = Client(host='grpcs://2e037a5082.wolf.jina.ai')

# trademark dataset
client = Client(host='grpcs://gentle-asp-671ced508f.wolf.jina.ai')

st.title('CLIP Search demo')



def display_results(results):
    st.write('Search results:')
    cols = st.columns(2)

    for k, m in enumerate(results):
        image_id = m.id
        # print(image_id)

        col_id = 0 if k % 2 == 0 else 1

        with cols[col_id]:
            score = m.scores['cosine'].value
            similarity = 1 - score
            st.markdown(f'Top: [{k+1}], similarity: {similarity}')
            cols[col_id].image(st.session_state.tm_data[image_id].blob)


def search(query_da):
    res = client.post('/search', query_da)

    result = DocumentArray(
                        sorted(
                            res, key=lambda m: m.scores['COSINE'].value
                        )
                    )
    display_results(result[0].matches)
    #display_results(res[0].matches)


menu = ['Text', 'Image']
choice = st.sidebar.selectbox('Select The Input Modality: ',menu)

if 'tm_data' not in st.session_state:
    with st.spinner('Preparing data...'):
        st.session_state.tm_data = DocumentArray.pull(name='tm_designs')

if choice == 'Image':
    st.subheader('Image-Image Search')
    image_file = st.file_uploader('Upload Query Image', type=["png", "jpg", "jpeg"])

    if image_file is not None:
        img = image_file.getvalue()
        st.image(Image.open(image_file), width=250)

        query_da = DocumentArray([Document(text='query_img', blob=img)])

elif choice == 'Text':
    st.subheader('Text-Image Search')
    query = st.text_input('Text Query', placeholder='Type your query here...')

    query_da = DocumentArray([Document(text=query)])


if st.button('search'):
    message = 'Wait for it...'

    with st.spinner(message):
        search(query_da)
    
