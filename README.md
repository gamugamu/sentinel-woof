#conf waf
#docker image
docker run --rm -it -p 5000:8080 -d cryptodraco/sentinel-dev:v0.0.6

docker pull redis
# port redis par defaut 6379
docker run --name waf-redis -p 6379:6379 -d redis

docker pull mongo
# port mongo par defaut 27017
docker run --name waf-MongoDB -p 27017:27017 -d mongo

docker pull postgres
# port 5432
docker run -d -p 5432:5432 --name waf-postgres -e POSTGRES_PASSWORD=secretpassword postgres
docker exec -it waf-postgres bash
/# psql -U postgres
/# CREATE DATABASE woof;
/# \q
en local psql -h localhost -p 5432 -U postgres -W  devrait marcher
-> deja fait python manage.py db init
python manage.py db migrate
python manage.py db upgrade

#migration remote:
## export
pg_dump -C -h localhost  -U postgres woof | xz > woof-backup.xz
## copy
scp -r woof-backup.xz root@wannanosuurus.com:~
# remote terminal
docker cp woof-backup.xz waf-postgres:/woof-backup.xz

#Utiliser docker-compose:
docker-compose -f stack.yml up

#minio
docker pull minio/minio
docker run -e "MINIO_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE" -e "MINIO_SECRET_KEY=SECRETSECRET" -p 9000:9000 minio/minio server /data

K3tNre9SVrgTue88eG36w642BRwiF5
# GET
curl -i -H "Authorization: Bearer 2mSaNSBmNBUYgRImGKraCDei5t89gC" -H "Content-Type: application/json" http://127.0.0.1:8000/me
# MUTATE
curl -k -H "Authorization: Bearer NRmbkgxtrV60wQhoqnErd5qdLUSMot" -H "Content-Type: application/json" -X PUT -d '{"mail":"dsjjl@djsl.com"}' http://127.0.0.1:8000/me
# DELETE
curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:8000/me

curl -k -H "Authorization: Bearer tmBC6jSx973do1kVRgFlaQF5njLHJ8" -H "Content-Type: application/json" https://woof.wannanosuurus.com/me/pets

curl -i -H "Authorization: Bearer KL5Gbi2uXcVKAWscyBEXBUvD2MSjbL" http://localhost:5001/pets/feeds/luke -X POST -F "image=@/Users/abadiel/Desktop/D2.jpg"

# rajout feed
curl -i -H "Authorization: Bearer 6fY6Bjiex79emxkr7J4qmld718B801" http://0.0.0.0:5002/pets/feeds/kikoo -X POST -F "image=@/Users/lionel/Desktop/home-dog-running.jpg"

# liste feed d'un pets en particulier
curl -i -H "Authorization: Bearer 6fY6Bjiex79emxkr7J4qmld718B801" http://0.0.0.0:5002/pets/feeds/kikoo/1

# modification feed
curl -i -H "Authorization: Bearer 6fY6Bjiex79emxkr7J4qmld718B801" http://0.0.0.0:5002/pets/feeds/423bd68e433a48a8a75142ccf6378d89 -H "Content-Type: multipart/form-data" "-X PUT -F "image=@/Users/lionel/Desktop/home-dog-running.jpg" -F "comment= me me me MOX MOX"

# liste ami
curl -i -H "Content-Type: application/json" -i -H "Authorization: Bearer lKD7KdZPXzNjA7ORY7eDOwz0HKMR6W" http://localhost:5002/friends

# rajout ami
curl -i -H "Content-Type: application/json" -i -H "Authorization: Bearer 9gOxnZU9EJS6uEOfaBGBpC7t1I1oz2" http://localhost:5002/friends/big-donkey -X POST
