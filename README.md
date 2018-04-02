#conf waf
#docker image
docker run --rm -it -p 5000:8080 -d cryptodraco/sentinel-dev:v0.0.1

docker pull redis
# port redis par defaut 6379
docker run --name waf-redis -p 6379:6379 -d redis

docker pull mongo
# port mongo par defaut 27017
docker run --name waf-MongoDB -p 27017:27017 -d mongo
