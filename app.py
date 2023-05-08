import streamlit as st
import pandas as pd
import pickle 
import json 
from sklearn.metrics.pairwise import cosine_similarity
import webbrowser
import requests
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup  
import nltk 
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()  

movies_dict = pickle.load(open('movies.pkl','rb'))


movies = pd.DataFrame(movies_dict)  

new_df = pd.read_csv('moviezz.csv')


# RECOMMEND SECTION FUNCTION
def fetch_link(movie_id):
	link_url = f"https://www.themoviedb.org/movie/{movie_id}" 
	
	return link_url



base_url="https://image.tmdb.org/t/p/w500/" 


def fetch_poster(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=150a2108231c511927660bbee0ce71b1&language=en-US".format(movie_id))
	data = response.json()  
	# print(data)  
	img = "https://image.tmdb.org/t/p/w500/"+data['poster_path'] 
	return  img    

def fetch_credits(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}/credits?api_key=150a2108231c511927660bbee0ce71b1&language=en-US".format(movie_id)) 
	dr = response.json()
	cast = dr['cast'] 
	name = cast[0:6]
	return name  

def get_videos(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}/videos?api_key=150a2108231c511927660bbee0ce71b1&language=en-US".format(movie_id))
	data = response.json()
	vid = data['results']
	return vid 

def watch_now(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}/watch/providers?api_key=150a2108231c511927660bbee0ce71b1".format(movie_id))
	data = response.json()
	watch = data['results'] 
	# print(watch)
	return watch 
	
def fetch_details(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=150a2108231c511927660bbee0ce71b1&language=en-US".format(movie_id))
	return response.json()   

def fetch_reviews(movie_id):
	for i in range(0,20):
		response=requests.get("https://api.themoviedb.org/3/movie/{}/reviews?api_key=150a2108231c511927660bbee0ce71b1&language=en-US&page=1".format(movie_id))
		data = response.json()
		review = data['results']
		return review
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

def recommend(movie):

	cv = CountVectorizer(max_features=5000,stop_words="english")
	vectors = cv.fit_transform(new_df['tags']).toarray()
	
	similarity=cosine_similarity(vectors) 
	movie_index = movies[movies['title']==movie].index[0]
	
	distances = similarity[movie_index]
	movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:7] 

	
	# print(movie_list)
	
	recommend_movies = []
	recommend_poster = []
	recommend_link = []  
	
	for i in movie_list:
		movie_id = movies.iloc[i[0]].movie_id 
		
		
		
	  
		recommend_movies.append(movies.iloc[i[0]].title)
		recommend_link.append(fetch_link(movie_id)) 
		
		recommend_poster.append(fetch_poster(movie_id))
		
	# print(recommend_link)
		

	return recommend_movies , recommend_poster , recommend_link 

st.title('Movie Recommender System') 
option = st.selectbox(
	'How would you like to be contacted?',
	(movies['title']))  
st.write('You selected:', option)  
base_url="https://image.tmdb.org/t/p/w500/" 
mid = movies[movies['title']==option] ['movie_id'].values[0]
details = fetch_details(mid)
credit = fetch_credits(mid) 
reviews = fetch_reviews(mid)   
	
	
videos = get_videos(mid)
now=watch_now(mid) 
if st.button('Recommend'):
	col1,col2=st.columns(2)
	with col1:
		st.image(base_url+details['poster_path']) 
		try:
			with col2:
				st.header(f"[{details['title']}]({now['AR']['link']})")
				st.caption(details['tagline'])
				st.write(details['overview'])
				st.markdown("**Released in {}**".format(details['release_date']))
				st.write('Runtime: {} mins'.format(details['runtime']))
				st.write('Avg. Rating: {} :star:            Votes: {} :thumbsup:'.format(details['vote_average'], details['vote_count'])) 
				
		except:
			st.error("some details not found !!!")
			
	st.markdown("<h1 style='text-align: center; color: red;'>Star Cast</h1>", unsafe_allow_html=True)
	   
		 
	col1,col2,col3,col4=st.columns(4) 
	slink = f"https://www.themoviedb.org/person/{credit[0]['id']}"
	slink1 = f"https://www.themoviedb.org/person/{credit[1]['id']}"
	slink2 = f"https://www.themoviedb.org/person/{credit[2]['id']}"
	slink3 = f"https://www.themoviedb.org/person/{credit[3]['id']}"
	slink4 = f"https://www.themoviedb.org/person/{credit[4]['id']}"
	try:
		with col1:
				st.image(base_url+credit[0]['profile_path'],width=100)
				st.write(f"[{credit[0]['name']}]({slink})")
		
		with col2:
				st.image(base_url+credit[1]['profile_path'],width=100)
				st.write(f"[{credit[1]['name']}]({slink1})")
		
		with col3:
				st.image(base_url+credit[2]['profile_path'],width=100)
				st.write(f"[{credit[2]['name']}]({slink2})")
		
		with col4:
				st.image(base_url+credit[3]['profile_path'],width=100)
				st.write(f"[{credit[3]['name']}]({slink3})") 
	except:
			st.error("some cast are not available !!!")  

	st.markdown("<h1 style='text-align: center; color: red;'>Trailer</h1>", unsafe_allow_html=True)
   
   
	try:
			vids = "https://www.youtube.com/watch?v="+videos[0]['key']
			st.video(vids)
	except:
			st.error("Trailler Not Found")  


   


	

	


	st.markdown("<h1 style='color:red'><center>Recommend For You</center></h1>",unsafe_allow_html=True)
	
	names,posters,link = recommend(option) 
	
	col1,col2,col3=st.columns(3) 

	
		
	with col1:
		try:
				st.subheader(f"[{names[0]}]({link[0]})")
		except:
				st.subheader(names[0]) 
			
		st.image(posters[0])
	with col2:
		try:
				st.subheader(f"[{names[1]}]({link[1]})")
		except:
				st.subheader(names[1])
			
		st.image(posters[1])

	with col3:
		try:
				st.subheader(f"[{names[2]}]({link[2]})")
		except:
				st.subheader(names[2])
			
		st.image(posters[2]) 
		

		col4,col5,col6=st.columns(3) 
		with col1:
			try:
				st.subheader(f"[{names[3]}]({link[3]})")
			except:
				 st.subheader(names[3]) 
			
			st.image(posters[3])
		with col2:
			try:
				st.subheader(f"[{names[4]}]({link[4]})")
			except:
				st.subheader(names[4])
			
			st.image(posters[4])

		with col3:
			try:
				st.subheader(f"[{names[5]}]({link[5]})")
			except:
				st.subheader(names[5])
			
			st.image(posters[5]) 
		




		
	

  
  

	

	


	
	




   
	



	
		
	
	

	
   

	

  
   
		
		
		

		
		

	   
	
	  
		
	


