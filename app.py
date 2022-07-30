!pip install IMDbPY
import streamlit as st
import pickle
import pandas as pd
from tmdbv3api import TMDb
import json
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tmdb = TMDb()
tmdb.api_key = '552927457b085828308d3b468f6bea5f'
from tmdbv3api import Movie
tmdb_movie = Movie()
movies_dict = pickle.load(open(r'C:\Users\HP\OneDrive\Desktop\mini-project\modular\recommendation_system\movie_dict.pkl','rb'))

movie = pd.DataFrame(movies_dict)

def create_similarity():
    
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(movie['comb'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return similarity
def get_poster(x):
    
    result = tmdb_movie.search(x)
    movie_id = result[0].id
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    data_json = response.json()
    
    return "https://image.tmdb.org/t/p/w500/" + data_json["poster_path"]
def get_info(x):
    
    result = tmdb_movie.search(x)
    movie_id = result[0].id
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    data_json = response.json()
    r_m_homepage=data_json["homepage"]
    r_m_release_date=data_json["release_date"]
    r_m_overview=data_json["overview"]
    r_m_popularity=data_json["popularity"]


    
    return r_m_homepage,r_m_release_date,r_m_overview,r_m_popularity



def recommend(m):
    m = m.lower()
    try:
        
        similarity.shape
    except:
        similarity = create_similarity()
    
    if m not in movie['movie_title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = movie.loc[movie['movie_title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:6] # excluding first item since it is the requested movie itself
        l = []
        recommended_movies_poster=[]
        recommended_movies_info=[]
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(movie['movie_title'][a])
            recommended_movies_poster.append(get_poster(movie['movie_title'][a]))
            recommended_movies_info.append(get_info(movie['movie_title'][a]))

        return l,recommended_movies_poster,recommended_movies_info

     
movie = pd.DataFrame(movies_dict)
#st.set_page_config(layout="wide")
header=st.container()



with header:
    c1, c2, c3,c4,c5,c6,c7 = st.columns(7)
       
        
    with c1:

        st.write('')
    with c2:
        st.write('')
    with c3:    
        st.write('')  
    with c4:
        st.write('')
    with c5:
        st.write('')
    with c6:
        st.write('')
    with c7:
        st.write('[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)') 
        
    #st.write('[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)')
    #st.write("[![Star](<https://img.shields.io/github/stars/><Prikshit7766>/<recommendation_system>.svg?logo=github&style=social)](<https://gitHub.com/><Prikshit7766>/<recommendation_system>)")
    co1, co2, co3 = st.columns(3)
       
        
    with co1:

        st.write('')
    with co2:
        st.image('https://images.creativemarket.com/0.1.0/ps/7414066/1820/1214/m1/fpnw/wm1/logo-design-for-movie-production-company-01-.jpg?1575502358&s=c37b3e6a8863b415070b669f6c8a457c')
    with co3:    
        st.write('')    
   
    #st.image("https://images.creativemarket.com/0.1.0/ps/7414066/1820/1214/m1/fpnw/wm1/logo-design-for-movie-production-company-01-.jpg?1575502358&s=c37b3e6a8863b415070b669f6c8a457c", width=200)
    st.markdown(""" <style> .title{
font-size:50px; text-align:center; border:1px solid #ccc; border-radius:12px;} s
</style> """, unsafe_allow_html=True)
    st.markdown('<p class="title">Movie Recommendation System</p>',unsafe_allow_html=True)
    selected_movie_name = st.selectbox('How would you like to be contacted?',movie["movie_title"].values)

if st.button('Recommend'):

    names,posters,info=recommend(selected_movie_name)
    #homepage,release_date,overview,popularity = info.split(',')
    st.markdown(""" <style> .font {
font-size:50px ; font-family: 'Cooper Black'; color: #FF9633;} 
</style> """, unsafe_allow_html=True)

    
    st.markdown('<p class="font">Recommended Movies</p>', unsafe_allow_html=True)
    st.write(' ')
    
    for i in range(len(names)):
        col1, col2, col3, col4, col5 = st.columns(5)
        st.write(' ')
        
        with col1:

            st.image(posters[i])
        with col2:
            st.write('Title  :   ',names[i].title())
        with col3:    
            st.write('Homepage link : ',info[i][0])
        with col4:    
            st.write('Release Date : ',info[i][1])
            
        st.text_area('Overview : ',info[i][2])
        st.write(' ')
        st.write(' ')
        with col5:     
            st.write('Popularity : ',info[i][3])
       
        
        #st.text(homepage[i])
        #st.text(release_date[i])
        #st.text(overview[i])
        #st.text(popularity[i])
        st.write(' ')
        


 


