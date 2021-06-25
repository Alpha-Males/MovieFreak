MovieFreak

https://moviefreak-flask-new.herokuapp.com/


installation

install postgresql for your machine

start the service using

service postgresql start
    
    sudo -u postgres psql

then create a database  using
    
    CREATE DATABASE ratings;
    then import the sql file
    sudo -u postgres -i psql ratings < ratings.sql

run `python app.py`

## IMPORTANT CSV AND JSON FILES
Some of the csv files are previously created to give recommendations using communities.
  1. user-com.csv - In this csv file we store the community id  of each user id which was previosly calculated using Neo4j by applying Louvain algorithm on the User graph.
  2. small-movies-similarity.csv - In this csv file we have movie id and in the sim_movieId there is the id of the movie which it is similar to calculated based on tags, genre and rating relevance.
  3. community-movies.json - In this json file the key is the community id and value is a string of movie ids that have been watched by the users belonging to that particular community.The movie ids in the string are separated by commas.
