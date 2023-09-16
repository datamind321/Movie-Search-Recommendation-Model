import streamlit as st
import pandas as pd
import pickle 

from sklearn.metrics.pairwise import cosine_similarity

import requests
from sklearn.feature_extraction.text import CountVectorizer




movies_dict = pickle.load(open('movies.pkl','rb'))


movies = pd.DataFrame(movies_dict)  

new_df = pd.read_csv('moviezz.csv')


# RECOMMEND SECTION FUNCTION
def fetch_link(movie_id):
	link_url = f"https://www.themoviedb.org/movie/{movie_id}" 
	
	return link_url



base_url="https://image.tmdb.org/t/p/w500/" 


def fetch_poster(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=45c587635e813dbf6f99b3d8ccfb7d32&language=en-US".format(movie_id))
	data = response.json()  
	# print(data)  
	img = "https://image.tmdb.org/t/p/w500/" + data['poster_path'] 
	return  img    

def fetch_credits(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}/credits?api_key=45c587635e813dbf6f99b3d8ccfb7d32&language=en-US".format(movie_id)) 
	dr = response.json()
	cast = dr['cast'] 
	name = cast[0:6]
	return name  

def get_videos(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}/videos?api_key=45c587635e813dbf6f99b3d8ccfb7d32&language=en-US".format(movie_id))
	data = response.json()
	vid = data['results']
	return vid 

def watch_now(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}/watch/providers?api_key=45c587635e813dbf6f99b3d8ccfb7d32".format(movie_id))
	data = response.json()
	watch = data['results'] 
	# print(watch)
	return watch 
	
def fetch_details(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=45c587635e813dbf6f99b3d8ccfb7d32&language=en-US".format(movie_id))
	return response.json()   

def fetch_reviews(movie_id):
	for i in range(0,20):
		response=requests.get("https://api.themoviedb.org/3/movie/{}/reviews?api_key=45c587635e813dbf6f99b3d8ccfb7d32&language=en-US&page=1".format(movie_id))
		data = response.json()
		review = data['results']
		return review
def star_cast(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}/credits?api_key=45c587635e813dbf6f99b3d8ccfb7d32&language=en-US".format(movie_id)) 
	dr = response.json()
	cast = dr['cast']   

	return cast 


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
activity = ['Search','Recommendation','About'] 
choices = st.sidebar.selectbox("Select Activity",activity) 

if choices=='Search':
	st.title("Movie Search App") 

	title = st.text_input("Type and Hit Enter....") 

	url = f"https://api.themoviedb.org/3/search/movie?api_key=45c587635e813dbf6f99b3d8ccfb7d32&query={title}" 
	url2 = f"https://api.themoviedb.org/3/search/movie?api_key=45c587635e813dbf6f99b3d8ccfb7d32&query=append_to_response=videos"
	video=requests.get(url2)
	file=video.json()


	base_url = "https://image.tmdb.org/t/p/w500/"
	data = requests.get(url)
	m = data.json()
	movie = m['results'] 
	if title:
		try:
			col1,col2=st.columns(2) 
			movie_id = movie[0]['id'] 
		   
			stars = star_cast(movie_id)

			link_url = f"https://www.themoviedb.org/movie/{movie_id}"
			with col1:
				st.image(base_url+movie[0]['poster_path'])
			with col2:
				st.header(f"[{movie[0]['original_title']}]({link_url})")
				st.write("Relesase Date :", movie[0]['release_date']) 
				st.write(movie[0]['overview']) 
				st.write("Popularity : ",movie[0]['popularity'])
				st.write("Vote Avg : ",movie[0]['vote_average'])
				st.write("Vote Counts : ",movie[0]['vote_count']) 
		
			st.markdown("<center><h1>StarCast<h1></center>",unsafe_allow_html=True)
			col1,col2,col3,col4=st.columns(4)
			slink = f"https://www.themoviedb.org/person/{stars[0]['id']}"
			slink1 = f"https://www.themoviedb.org/person/{stars[1]['id']}"
			slink2 = f"https://www.themoviedb.org/person/{stars[2]['id']}"
			slink3 = f"https://www.themoviedb.org/person/{stars[3]['id']}"
			slink4 = f"https://www.themoviedb.org/person/{stars[4]['id']}"

			
			
			try:
				with col1:
					st.image(base_url+stars[0]['profile_path'])
					st.subheader(f"[{stars[0]['original_name']}]({slink})")
				with col2:
					st.image(base_url+stars[1]['profile_path'])
					st.subheader(f"[{stars[1]['original_name']}]({slink1})")
				with col3:
					st.image(base_url+stars[2]['profile_path'])
					st.subheader(f"[{stars[2]['original_name']}]({slink2})")
				with col4:
					st.image(base_url+stars[3]['profile_path'])
					st.subheader(f"[{stars[3]['original_name']}]({slink3})")
			except:
				st.error("NO Starcast Available !!") 

			

			st.header("More Like This.......")
			col1,col2,col3,col4,col5=st.columns(5)
			link1 = f"https://www.themoviedb.org/movie/{movie[1]['id']}"
			link2 = f"https://www.themoviedb.org/movie/{movie[2]['id']}"
			link3 = f"https://www.themoviedb.org/movie/{movie[3]['id']}"
			link4 = f"https://www.themoviedb.org/movie/{movie[4]['id']}"
			link5 = f"https://www.themoviedb.org/movie/{movie[5]['id']}"
			try:
				with col1:
					st.image(base_url+movie[1]['poster_path'])
					st.write(f"[{movie[1]['original_title']}]({link1})")
	
	
				with col2:
					st.image(base_url+movie[2]['poster_path'])
					st.write(f"[{movie[2]['original_title']}]({link2})")
		
	
				with col3:
					st.image(base_url+movie[3]['poster_path'])
					st.write(f"[{movie[3]['original_title']}]({link3})")
		
	
				with col4:
					st.image(base_url+movie[4]['poster_path'])
					st.write(f"[{movie[4]['original_title']}]({link4})")
		
		
				with col5:
					st.image(base_url+movie[5]['poster_path'])
					st.write(f"[{movie[5]['original_title']}]({link5})")  
			except:
				st.succ("Similar Movies Found !!!")
		except:
			st.error("No Movie Found !!!")


	

if choices=='Recommendation':
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
			img = base_url+details['poster_path']
	
		
			try:
				with col1:
					st.write(f"[{names[3]}]({link[3]})")
				
					st.image(posters[0])
			
		
				with col2:
					st.write(f"[{names[4]}]({link[4]})")
					st.image(posters[1])

				with col3:
					st.write(f"[{names[5]}]({link[5]})")
					st.image(posters[2])
			except:
				st.error('No Recommendation Found !!')
			
				 
	
	
		
	
			col1,col2,col3=st.columns(3) 
			try:
				with col1:
					st.write(f"[{names[3]}]({link[3]})")
					st.image(posters[3])
		
				with col2:
					st.write(f"[{names[4]}]({link[4]})")
					st.image(posters[4])

				with col3:
					st.write(f"[{names[5]}]({link[5]})")
					st.image(posters[5])
			except:
					st.error("No Recommendation Found !!!")

if choices=="About":
	st.title("Movie Search & Recommendation Engine V-2.0")
	st.markdown("This Engine Developed by <a href='https://github.com/datamind321'>DataMind Platform</a>",unsafe_allow_html=True)
	st.subheader("if you have any query Contact us on : bme19rahul.r@invertisuniversity.ac.in") 
	st.markdown("More on : ")
	
	
	st.markdown("[![Linkedin](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/rahul-rathour-402408231/)",unsafe_allow_html=True)
	

	st.markdown("[![Instagram](https://img.icons8.com/color/1x/instagram-new.png)](https://instagram.com/_technical__mind?igshid=YmMyMTA2M2Y=)")

				







		
	

  
  

	

	


	
	




   
	



	
		
	
	

	
   

	

  
   
		
		
		

		
		

	   
	
	  
		
	


