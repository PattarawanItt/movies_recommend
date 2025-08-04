import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# โหลดข้อมูล
movies = pd.read_csv('tmdb_5000_movies.csv')
movies = movies[['title', 'cast']].dropna()

# Vectorize
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['cast'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
title_to_index = pd.Series(movies.index, index=movies['title'])

def recommend_movie(title, num=5):
    idx = title_to_index.get(title)
    if idx is None:
        return ["ไม่พบหนังที่คุณป้อน", "未找到您输入的电影"]
        # return ["未找到您输入的电影"]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices].tolist()
