* instructions on express to docker, and docker to ec2
- mkdir nodeapp
  npm init
  create express app
- create docker file Dockerfile
  docker build -t [dockerusername/]nodeapp
  docker build -t nodeapp .
  docker run --name nodeapp -p 80:8000 -d dockerusername/nodeapp  
  docker images
- submit to docker repository
  docker login -u username -p pass
  docker push dockerusername/nodeapp
- docker ps
  docker stop PID
- docker pull dockerusername/nodeapp
- ec2 launch (from amazonecs docker-basics)
  sudo yum update -y
  sudo yum install docker
  sudo usermode -a -G docker ec2-user
  docker info
  aws ecr create-repository --repository-name myrepo --region <region>
  docker tag nodeapp aws_account_id.dkr.ecr.<region>.amazonaws.com/myrepo
  aws ecr get-login-password | docker login --username AWS --password-stdin awsaccountid.dkr.ecr.<region>.amazonaws.com
  docker push <awsaccountid>.dkr.ecr.region.amazonaws.com/myrepo
