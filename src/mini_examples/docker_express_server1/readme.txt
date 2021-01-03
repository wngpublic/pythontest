vim Dockerfile
docker build -t docker_express_server .         
// -t is tagname repository when doing  docker images
docker run --name docker_express_server -p 3030:3000 docker_express_server
docker images
docker run --name appname -p 80:3000 -d dockerusername/imagename
docker run --name docker_express_server -p 3030:3000 docker_express_server
docker run -t -i -d --name docker_express_server -p 3030:3000 docker_express_server // terminal, interactive, daemon, allows for CTRL-C
docker ps -a
docker rm containerid
docker stop containerid  // on another terminal. CTRL-C doesnt work on the docker run term

docker image
docker image inspect docker_express_server:latest
docker rmi imageid
docker rmi repositoryname
docker rmi repositoryname:tag
docker system prune -a      // prune all with prompt

optional with docker-compose
docker-compose build
docker-compose up
docker-compose up -d
docker-compose stop
docker-compose start

