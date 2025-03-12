import streamlit as st
import pickle
import pandas as pd
import requests

# TMDb API Key
API_KEY = "292a14387472ea59790d17fbd8bfc895"
BASE_URL = "https://api.themoviedb.org/3"

# Load movie data
movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['original_title'].values
new_data = pd.DataFrame(movies)

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_title):
    """Fetch movie poster URL using TMDb API."""
    search_url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": movie_title}
    
    response = requests.get(search_url, params=params)
    data = response.json()
    
    if "results" in data and len(data["results"]) > 0:
        poster_path = data["results"][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None  # Return None if no poster is found

def recommend_(movie):
    """Get recommended movies and their posters."""
    movie_index = new_data[new_data['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommend_movies = []
    recommend_posters = []
    
    for i in movie_list:
        movie_title = new_data.iloc[i[0]].original_title
        recommend_movies.append(movie_title)
        recommend_posters.append(fetch_poster(movie_title))
    
    return recommend_movies, recommend_posters

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox("Select a movie:", movies_list)

if st.button('Recommend'):
    recommendations, posters = recommend_(selected_movie_name)
    
    cols = st.columns(5)  # Create 5 columns for displaying movies & posters
    for i in range(len(recommendations)):
        with cols[i]:
            st.text(recommendations[i])  # Movie Title
            if posters[i]:  # Show poster if available
                st.image(posters[i], use_container_width=True)  # ✅ FIXED!
            else:
                st.text("No Image Available")
