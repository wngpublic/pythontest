- example of reverse proxy with 2 flask endpoints
  - start up 2 flask instances first
    - python3 test_flask_endpoints_1.py   # for http://localhost:8124/a* endpoints
    - python3 test_flask_endpoints_2.py   # for http://localhost:8125/b* endpoints
  - start nginx with conf
    - sudo nginx -c $PWD/nginx-rp-1.conf  # reverse proxy for port 8080 to ports 8124 and 8125
  - example:
    http://localhost8080/a/echo/helloa    # routes to localhost:8124/a/*
    http://localhost8080/b/echo/hellob    # routes to localhost:8125/b/*
  - to kill:
    - source sh.kill_nginx_processes.sh


