import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from docarray import DocumentArray, Document


from jina import Client

client = Client(host='grpcs://e275ad649f.wolf.jina.ai')
st.title('Retrieval in CLIP-as-service demo')


def display_results(results):
    st.write('Search results:')
    cols = st.columns(2)

    for k, m in enumerate(results):
        image_id = m.id
        image_url = 'https://open-images-dataset.s3.amazonaws.com/' + image_id

        col_id = 0 if k % 2 == 0 else 1

        with cols[col_id]:
            score = m.scores['cosine'].value
            similarity = 1 - score
            st.markdown(f'Top: [{k+1}] Similarity: ({similarity:.3f}) {image_id}')
            cols[col_id].image(image_url)

    # data = [[r.text, st.image(), r.scores['cosine'].value] for r in results]
    # df = pd.DataFrame(
    # data,
    # columns=('caption', 'uri', 'score'))

    # st.table(df)


def search(query_da):
    res = client.post('/search', query_da)

    result = res[0].matches[:10]
    display_results(result)


menu = ['Text', 'Image']
choice = st.sidebar.selectbox('Select The Input Modality: ',menu)

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
    
