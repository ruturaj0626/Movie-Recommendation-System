import pandas as pd
import streamlit as st
import pandas
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8a7ef013ebcdaadac09d3cb5cde295e1&language=en-US'.format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']





def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_names = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_names.append(movies.iloc[i[0]].title)
        # For posters
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies_names,recommended_movies_posters



movies_dict = pickle.load(open('movies_dict.pkl','rb'))

similarity = pickle.load(open('similarity.pkl','rb'))

movies = pd.DataFrame(movies_dict)

st.title('Movie Recommander System')


selected_movie_name = st.selectbox(
    'Choose Your Movie',
    movies['title'].values)

if st.button('Recommend'):
    name,posters = recommend(selected_movie_name)
    st.write("Here's what we recommand,\n\n")

    col1, col2, col3,col4, col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(posters[0])

    with col2:
        st.text(name[1])
        st.image(posters[1])

    with col3:
        st.text(name[2])
        st.image(posters[2])

    with col4:
        st.text(name[3])
        st.image(posters[3])

    with col5:
        st.text(name[4])
        st.image(posters[4])