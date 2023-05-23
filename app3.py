import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'b4aea1034c35e785a7b9f20eccbe0ecf'
tmdb.language = 'ko-KR'

# 추천 함수
def get_recommendation(title, cosine_sim2):
    # title을 변수로 받아 idx 호출하기
    idx = movies[movies['title'] == title].index[0] # 인덱스가 배열 형태로 넘어온다고?

    #idx를 변수로 인덱스, 코사인유사도를 리스트로 만들기
    sim2_scores = list(enumerate(cosine_sim2[idx])) # 인덱스, 유사도 형태로 넘어옴.

    #코사인유사도를 기준으로 내림차순 정렬하기
    sim2_scores = sorted(sim2_scores, key=lambda x : x[1], reverse=True) # x[1]은 유사도를 기준으로 정렬
    # 자기 자신을 제외한 20개만 남기기
    sim2_scores = sim2_scores[1:11]
    # 20개의 인덱스만 뽑기
    movie2_indices = [i[0] for i in sim2_scores]
    # 인덱스로 영화 제목 불러오기
    images = []
    titles = []
    for i in movie2_indices : 
        id = movies['id'].iloc[i]
        details = movie.details(id) # tmdb에서 자료가져오기. api사용

        image_path = details['poster_path']
        if image_path : 
            image_path = 'https://image.tmdb.org/t/p/w500/'+ image_path
        else:
            image_path = 'no_image.jpg'

        images.append(image_path)
        titles.append(details['title']) # tmdb에서 한국어로 정보를 받을수 잇음.
    return images, titles

#파일 로드하기
movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim2 = pickle.load(open('cosine_similarity2.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_similarity.pickle', 'rb'))

#사이트 기본 세팅
st.set_page_config(layout='wide')
st.title("Avaaroong's Homeflix")
st.header("Don't waste any more time choosing a movie.")
st.subheader("I'll figure it out!")

movie_list = movies['title'].values
title= st.selectbox('Choose a movie you enjoyed watching.', movie_list)

# 요소 추천 만들기
if st.button('Recommendation by Jenre, Actor, Director, etc'):
    with st.spinner('Searching...'):
        images, titles = get_recommendation(title, cosine_sim2) #
        idx =  0
        for i in range(0, 2) : 
            cols = st.columns(5)
            for col in cols:
                link_text = "Find Info"
                link_url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={titles[idx]} 영화"
                col.image(images[idx]) 
                col.write(titles[idx])
                col.write(f'<a href="{link_url}">{link_text}</a>', unsafe_allow_html=True)
                idx += 1

# 줄거리 추천 만들기
if st.button('Recommendation by Overview'):
    with st.spinner('Searching...'):
        images, titles = get_recommendation(title, cosine_sim) #
        idx =  0
        for i in range(0, 2) : 
            cols = st.columns(5)
            for col in cols:
                link_text = "Find Info"
                link_url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={titles[idx]} 영화"
                col.image(images[idx]) 
                col.write(titles[idx])
                col.write(f'<a href="{link_url}">{link_text}</a>', unsafe_allow_html=True)
                idx += 1