docker-compose rm -f

cd ./flask-app

# Build the Docker image
docker build . -t flaskapp:test 

cd ../

# Run the Docker container
docker-compose up --force-recreate