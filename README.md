# cloudrun

docker build .
docker run --env-file .env <image>

docker run -it --entrypoint /bin/bash --env-file .env <image>
