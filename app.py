# import streamlit as st
# import pickle
# import pandas as pd
# import requests

# # def fetch_poster(movie_id):
# #     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
# #     data = requests.get(url)
# #     data = data.json()
# #     poster_path = data['poster_path']
# #     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
# #     return full_path

# def fetch_poster(movie_id):
#     API_KEY = "a7cb21fee94e0d246ddd913f7e11aaf2"
#     response=requests.get("https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US".format(movie_id))
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    

# def recommend(movie):
#     movie_index=movies[movies['title']==movie].index[0]
#     distances=similarity[movie_index]
#     movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]


#     recommended_movie_names=[]
#     recommended_movie_posters=[]
#     for i in movies_list:
#         movie_id=movies.iloc[i[0]].movie_id
#         recommended_movie_names.append(movies.iloc[i[0]].title)
#         recommended_movie_posters.append(fetch_poster(movie_id))
#     return recommended_movie_names,recommended_movie_posters


# movies_dict=pickle.load(open('movie_dict.pkl','rb'))
# movies=pd.DataFrame(movies_dict)


# similarity=pickle.load(open('similarity.pkl','rb'))

# st.title("Movie Recomendation System")

# selected_movie_name=st.selectbox(
# 'similar to which movie would you like to watch?',
# movies['title'].values
#     )

# if st.button('🔍 Recommend'):
#     recommended_movie_names, recommended_movie_posters=recommend(selected_movie_name)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])

#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])

import streamlit as st
import pickle
import pandas as pd
import requests

# ==============================
# 🔑 Your TMDB API Key
# ==============================
API_KEY = "a7cb21fee94e0d246ddd913f7e11aaf2"

# ==============================
# 🖼️ Fetch Poster Function
# ==============================
def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raise error for bad responses
        data = response.json()

        # Ensure 'poster_path' exists
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.exceptions.RequestException as e:
        st.warning(f"⚠️ Unable to fetch poster for movie ID {movie_id}. Error: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

# ==============================
# 🎬 Recommendation Function
# ==============================
def recommend(movie):
    """Return list of recommended movies and posters."""
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:6]

        recommended_movie_names = []
        recommended_movie_posters = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_posters.append(fetch_poster(movie_id))

        return recommended_movie_names, recommended_movie_posters

    except Exception as e:
        st.error(f"Error during recommendation: {e}")
        return [], []

# ==============================
# 📦 Load Data
# ==============================
try:
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading data files: {e}")
    st.stop()

# ==============================
# 🎥 Streamlit UI
# ==============================
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    '👉 Select a movie you like:',
    movies['title'].values
)

if st.button('🔍 Recommend'):
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    if recommended_movie_names:
        cols = st.columns(5)
        for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
            with col:
                st.text(name)
                st.image(poster)
    else:
        st.warning("No recommendations found.")
