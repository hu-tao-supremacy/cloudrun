# cloudrun

docker build .
docker run --env-file .env <image>
docker run --env-file .env -p 8080:8080 <image>

docker run -it --entrypoint /bin/bash --env-file .env <image>
psql -U username -h localhost -p 5432 dbname
