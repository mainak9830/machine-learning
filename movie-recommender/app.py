import streamlit as st
import pickle
import pandas as pd
import requests

movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')

selected_movie_name = st.sidebar.selectbox(
    'How would you like to be watch?',
    movies_list['title'].values
)
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7f0d0bb6f3fb0b5e4a244c5d102b43f2&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    new_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in new_list:
        movie_id = movies_list.iloc[i[0]].movie_id
        #Fetch poster from TMDB API
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies_list.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.beta_columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])