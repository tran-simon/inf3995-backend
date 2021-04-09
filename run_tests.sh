sudo docker kill back
sudo docker rm back
sudo docker build . -t backend
sudo docker run -d --name back backend
sudo docker exec back /bin/sh -c "cd ./src/tests;pytest --cov-report term-missing --cov"
