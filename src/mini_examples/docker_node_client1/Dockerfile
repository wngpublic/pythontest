FROM node:15-alpine
ENV NODE_ENV production
ARG DIR1=/tmp/node/client1/
ARG DIR=./clientapp1
#RUN mkdir -p $DIR
WORKDIR $DIR
# not dst to $DIR!
COPY package*.json ./
COPY *.js ./
RUN npm install
RUN echo "NODE Version:" && node --version
RUN echo "NPM Version:" && npm --version
CMD [ "node", "simple_client_to_simple_server.js" ]

