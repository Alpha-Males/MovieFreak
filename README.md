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
  4. ratings.csv - It contains the information of user's rating to a movie and the timestamp of the rating.
  5. users.csv - UserID of all the users in the data set.
  6. users_genres.csv - UserID and their favourite genre . The favourite genre is the most watched genre found using movies-genres.csv file.
  7. users_movies - Extension of ratings.csv . Contains userId and movie they have watched to create a graph between user and movies.
  8. user-user.csv - The columns are user1 and user2 . Each row represents an edge between the users . This was calculated by calculating the Pearson Correlation Coefficient of the users who have watched atleast 10 movies common . The edge is only formed if PCC is greater than 0.75.
  9. movies_genres.csv - Relation between movies and their genre.
  
