#conf waf
#docker image

docker pull redis
# port redis par defaut 6379
docker run --name waf-redis -p 6379:6379 -d redis

docker pull mongo
# port mongo par defaut 27017
docker run --name waf-MongoDB -p 27017:27017 -d mongo
