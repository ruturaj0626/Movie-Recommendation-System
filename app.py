import pandas as pd
import streamlit as st
import requests
import pickle

# Function to fetch movie poster URL using TMDb API
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8a7ef013ebcdaadac09d3cb5cde295e1&language=en-US'.format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to recommend movies based on selected movie
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_names = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_names.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies_names, recommended_movies_posters

# Load data and similarity matrices from pickle files
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Streamlit app starts here
st.title('Movie Recommender System')

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    'Choose Your Movie',
    movies['title'].values)

# Button to trigger recommendation
if st.button('Recommend'):
    recommended_names, recommended_posters = recommend(selected_movie_name)
    st.write("Here's what we recommend:\n\n")

    # Display recommended movies and posters in columns
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.text(recommended_names[i])
        col.image(recommended_posters[i])
