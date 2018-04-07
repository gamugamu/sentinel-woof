#conf waf
#docker image
docker run --rm -it -p 5000:8080 -d cryptodraco/sentinel-dev:v0.0.1

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
/# \q;
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



curl -i -H "Authorization: Bearer NRmbkgxtrV60wQhoqnErd5qdLUSMot" -H "Content-Type: application/json" http://127.0.0.1:8000/me/profil
curl -k -H "Authorization: Bearer NRmbkgxtrV60wQhoqnErd5qdLUSMot" -H "Content-Type: application/json" -X PUT -d '{"mail":"dsjjl@djsl.com"}' http://127.0.0.1:8000/mecurl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:8000/me/profil
