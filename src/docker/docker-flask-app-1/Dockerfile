FROM python:3.6
COPY ./requirements.txt /var/www/requirements.txt
RUN pip3 install -r /var/www/requirements.txt
WORKDIR /
COPY . /
EXPOSE 8123
ENTRYPOINT [ "python3" ]
CMD [ "app/test_flask_endpoints.py" ]
