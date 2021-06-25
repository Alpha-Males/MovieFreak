MovieFreak


installation

install postgresql for your machine

start the service using

service postgresql start
    
    sudo -u postgres psql

then create a database  using
    
    CREATE DATABASE ratings;
    then import the sql file
    sudo -u postgres -i psql ratings < ratings.sql

run python3 server.py

