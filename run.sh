docker-compose rm -f

cd /home/dylan/volkswagon/flask-app

# Build the Docker image
docker build . -t flaskapp:test 

cd ../

# Run the Docker container
docker-compose up --force-recreate