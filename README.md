# guane-intern-fastapi

## Database

The database was created in a docker container, to create your own instance follow these steps:

**Note:** You need to have docker installed on your pc.

1. Open a terminal and copy `$docker` pull postgres
to download the official postgres image from dockerhub. 
2. Create a directory to save the postgres data on your machine so that the container is kept either stopped or deleted.
I created this path `/home/daniel/postgresVolumes/postgres12`.
3. To create a new docker container run: `$docker run -p 5432:5432 --name postgres12 -v /home/daniel/postgresVolumes/postgres12:/var/lib/postgresql/data -e   POSTGRES_USER=daniel -e POSTGRES_PASSWORD=root -d postgres`. You can change the user and the password but you have to change it in the environment variables config of the project too.
4. To enter the container run: `$docker exec -it postgres12 psql -U daniel`. Remember to change the user for the one you have chosen.
5. To create the database run: `#CREATE DATABASE db_tutorial_fastapi;`. In the same way, you can put any name, you just have to change it in the environment variables of the project.

That is all :)

