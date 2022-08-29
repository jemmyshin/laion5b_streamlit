import numpy as np
import pandas as pd
import streamlit as st
from docarray import DocumentArray, Document


# from clip_client import Client
from jina import Client

client = Client(host='grpcs://35aeb2a685.wolf.jina.ai')
st.title('Laion400M retrieval')


def display_results(results):
    st.write('Search results for:', query)
    cols = st.columns(2)

    for k, m in enumerate(results):
        image = m.uri
        col_id = 0 if k % 2 == 0 else 1

        with cols[col_id]:
            caption = m.text
            score = m.scores['cosine'].value
            st.markdown(f'#[{k+1}] ({score:.3f}) {caption}')
            cols[col_id].image(image)

    # data = [[r.text, st.image(), r.scores['cosine'].value] for r in results]
    # df = pd.DataFrame(
    # data,
    # columns=('caption', 'uri', 'score'))

    # st.table(df)


def search(query):
    # res = client.search([query])
    da = DocumentArray([Document(text=query)])
    res = client.post('/search', da)


    result = res[0].matches[:10]
    display_results(result)


query = st.text_input('Query', 'Type your query here...')

if st.button('search'):
    message = 'Wait for it...'

    with st.spinner(message):
        search(query)
    