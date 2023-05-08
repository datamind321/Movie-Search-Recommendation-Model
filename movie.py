import streamlit as st 
import requests 

st.title("Movie Search App") 


def star_cast(movie_id):
	response = requests.get("https://api.themoviedb.org/3/movie/{}/credits?api_key=150a2108231c511927660bbee0ce71b1&language=en-US".format(movie_id)) 
	dr = response.json()
	cast = dr['cast']   

	return cast    





title = st.text_input("Type and Hit Enter....") 

url = f"https://api.themoviedb.org/3/search/movie?api_key=150a2108231c511927660bbee0ce71b1&query={title}" 

	
base_url = "https://image.tmdb.org/t/p/w500/"
data = requests.get(url)
print(data)
m = data.json()
movie = m['results'] 
	# print(movie)
stars = star_cast(movie[0]['id'])
movie_id = movie[0]['id'] 
link_url = f"https://www.themoviedb.org/movie/{movie_id}" 
	# print(link_url)
# print(stars) 
if title:
	try:
		col1,col2=st.columns(2) 
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
			st.error("Similar Movies Not Found !!!")
	except:
		  st.error("No Movie Found !!!") 



			
   

