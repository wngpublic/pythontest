add src/docker/docker-flask-app-1/app/static/jquery-3.4.1.js 
sudo docker build -t mydockerflask .
sudo docker run --name name-mydockerflask-name -p 8123:8123 mydockerflask
sudo docker stop name-mydockerflask-name
sudo docker ps -a
sudo docker rm name-mydockerflask-name
