add src/docker/docker-flask-app-1/app/static/jquery-3.4.1.js 
sudo docker build -t mydockerflask .
sudo docker run --name name-mydockerflask-name -p 8123:8123 mydockerflask
sudo docker stop name-mydockerflask-name
sudo docker ps -a
sudo docker rm name-mydockerflask-name
sudo docker rm containerid

docker builder prune 
WARNING! This will remove all dangling build cache. Are you sure you want to continue? [y/N] y

docker images
REPOSITORY              TAG                 IMAGE ID            CREATED              SIZE
docker_express_server   latest              imageid             About a minute ago   nMB

docker rmi docker_express_server
// removes all images of it

docker rmi docker_express_server:version // remove specific version

docker rmi imageid

