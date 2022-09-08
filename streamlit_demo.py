import streamlit as st
from PIL import Image
from docarray import DocumentArray, Document
import json
import requests
from jina import Client

# import extra_streamlit_components as stx
# from streamlit.scriptrunner import add_script_run_ctx
# from streamlit.server.server import Server
# from tornado.httputil import parse_cookie

# from urllib.parse import quote, unquote


client = Client(host='grpcs://a9682347c4.wolf.jina.ai')
st.title('Retrieval in CLIP-as-service demo')


# JWT_COOKIE = 'JinaNOW_Jwt'
# AVATAR_COOKIE = 'AvatarUrl'
# TOKEN_COOKIE = 'JinaNOW_Token'


# @st.cache(allow_output_mutation=True, suppress_st_warning=True)
# def get_cookie_manager():
#     return stx.CookieManager()


# cookie_manager = get_cookie_manager()


# def _get_all_cookies() -> dict:
#     session_id = add_script_run_ctx().streamlit_script_run_ctx.session_id
#     session_info = Server.get_current()._get_session_info(session_id)
#     header = session_info.ws.request.headers
#     cookie_strings = [header_str for k, header_str in header.get_all() if k == 'Cookie']
#     parsed_cookies = {k: v for c in cookie_strings for k, v in parse_cookie(c).items()}

#     return parsed_cookies


# def get_cookie_value(cookie_name):
#     all_cookies = _get_all_cookies()
#     for k, v in all_cookies.items():
#         if k == cookie_name:
#             return


# def setup_session_state():
#     if 'matches' not in st.session_state:
#         st.session_state.matches = None

#     if 'min_confidence' not in st.session_state:
#         st.session_state.min_confidence = 0.0

#     if 'im' not in st.session_state:
#         st.session_state.im = None

#     if 'snap' not in st.session_state:
#         st.session_state.snap = None

#     if 'search_count' not in st.session_state:
#         st.session_state.search_count = 0

#     if 'jwt_val' not in st.session_state:
#         st.session_state.jwt_val = None

#     if 'avatar_val' not in st.session_state:
#         st.session_state.avatar_val = None

#     if 'token_val' not in st.session_state:
#         st.session_state.token_val = None

#     if 'login' not in st.session_state:
#         st.session_state.login = False

#     if 'error_msg' not in st.session_state:
#         st.session_state.error_msg = None

#     if 'page_number' not in st.session_state:
#         st.session_state.page_number = 0

#     if 'disable_next' not in st.session_state:
#         st.session_state.disable_next = True

#     if 'disable_prev' not in st.session_state:
#         st.session_state.disable_prev = True


# def _do_login(params):
#     code = params.code
#     state = params.state
#     if code and state:
#         # Whether it is fail or success, clear the query param
#         # query_params_var = {
#         #     'host': unquote(params.host),
#         #     'input_modality': params.input_modality,
#         #     'output_modality': params.output_modality,
#         #     'data': params.data,
#         # }
#         # if params.secured:
#         #     query_params_var['secured'] = params.secured
#         # st.experimental_set_query_params(**query_params_var)

#         resp_jwt = requests.get(
#             url=f'https://api.hubble.jina.ai/v2/rpc/user.identity.grant.auto'
#             f'?code={code}&state={state}'
#         ).json()
#         if resp_jwt and resp_jwt['code'] == 200:
#             st.session_state.jwt_val = resp_jwt['data']
#             st.session_state.token_val = resp_jwt['data']['token']
#             st.session_state.avatar_val = resp_jwt['data']['user']['avatarUrl']
#             st.session_state.login = False
#             cookie_manager.set(
#                 cookie=JWT_COOKIE, val=st.session_state.jwt_val, key=JWT_COOKIE
#             )
#             return
#         else:
#             st.session_state.login = True
#             params.code = None
#             params.state = None

#     st.session_state.login = True
#     redirect_uri = (
#         f'https://nowrun.jina.ai/?host={params.host}&input_modality={params.input_modality}'
#         f'&output_modality={params.output_modality}&data={params.data}'
#         + f'&secured={params.secured}'
#         if params.secured
#         else ''
#     )
#     redirect_uri = quote(redirect_uri)
#     rsp = requests.get(
#         url=f'https://api.hubble.jina.ai/v2/rpc/user.identity.authorize'
#         f'?provider=jina-login&response_mode=query&redirect_uri={redirect_uri}&scope=email%20profile%20openid'
#     ).json()
#     redirect_to = rsp['data']['redirectTo']
#     return redirect_to


# def _do_logout():
#     st.session_state.jwt_val = None
#     st.session_state.avatar_val = None
#     st.session_state.token_val = None
#     st.session_state.login = True
#     cookie_manager.delete(cookie=JWT_COOKIE, key=JWT_COOKIE)


# def render_auth_components(params):
#     if params.secured.lower() == 'true':
#         jwt_val = get_cookie_value(cookie_name=JWT_COOKIE)
#         if jwt_val and not st.session_state.login:
#             jwt_val = json.loads(unquote(jwt_val))
#             if not st.session_state.jwt_val:
#                 st.session_state.jwt_val = jwt_val
#             if not st.session_state.avatar_val:
#                 st.session_state.avatar_val = jwt_val['user']['avatarUrl']
#             if not st.session_state.token_val:
#                 st.session_state.token_val = jwt_val['token']
#         redirect_to = None
#         if not st.session_state.jwt_val:
#             redirect_to = _do_login(params)
#         _, logout, avatar = st.columns([0.7, 0.12, 0.12])
#         if not st.session_state.login:
#             with avatar:
#                 if st.session_state.avatar_val:
#                     st.image(st.session_state.avatar_val, width=30)
#             with logout:
#                 st.button('Logout', on_click=_do_logout)
#         return redirect_to
#     else:
#         return None


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
    for item in res[0].matches:
        print(item.id, item.uri)
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
    
