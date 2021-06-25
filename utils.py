import pandas as pd
import json 
import csv

def get_community_info():
    community={}
    df=pd.read_csv('communities.csv')
    res=df.values
    com_mem={}
    for i in res:
        print(i)
        val=i[0].split(' ')   
        members=val[1].split('|')
        com_mem[val[0]]=members
        for j in members:
            community[j]=val[0]
    return community,com_mem    

def get_movie_for_comm(id):
    """
    it will take community id and return top 10 highest rated movies of the community
    """
    l=json.loads(open('community-movies.json').read())
    return l[id].split(',')[:10]

def get_similar_movie(movId):
    a_file = open("small-movies-similarity.csv", "r")
    dict_reader = csv.DictReader(a_file)
    l=list(dict_reader)
    sim_movie=[]
    for i in l:
        if i['movieId'] == str(movId):
            sim_movie.append(i['sim_movieId'])

    return sim_movie[:5] if len(sim_movie) > 10 else sim_movie
