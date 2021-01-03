FROM node:15-alpine
ENV NODE_ENV production
ARG DIR1=/tmp/node/app1/
ARG DIR=./app1/
#RUN mkdir -p $DIR
WORKDIR $DIR
COPY package*.json ./
COPY *.js ./
RUN npm install
RUN echo "NODE Version:" && node --version
RUN echo "NPM Version:" && npm --version
COPY . ./
EXPOSE 3000
CMD [ "node", "simple_server.js" ]
