# Writing REST with Django Ninja

Django Ninja is a FastAPI inspired library for turning your Django views into REST API end-points. This webinar will show you how to get started with Django Ninja, how the interface interacts with Django's URL and ORM mechanisms, and how to apply authentication controls to your REST API.

Tutorial from PyCharm JetBrains Channel: [Writing REST With Django and Ninja](https://youtu.be/Gry6rlZYpzw)

## Setup
1. Create a virtual environment and activate it.

    ```bash
      python3 -m venv venv
      source venv/bin/activate
    ```
      OR with pyenv
    ```bash  
      pyenv virtualenv 3.11.2 westeros
      pyenv activate westeros
    ```

2. Inside project folder, install requirements.
    ```bash
      pip install -r requirements.txt
    ```

3. Run the migrations.
    ```bash
      python manage.py migrate
    ```
   
4. Run the server.
    ```bash
      python manage.py runserver
    ```
   
# Endpoints

## Get Home Greeting

### Request

`GET /api/lannister/home`

    curl -i -H 'Accept: application/json' http://localhost:8000/api/lannister/home

### Response

    HTTP/1.1 200 OK
    Date: Thu, 09 Mar 2023 00:55:56 GMT
    Server: WSGIServer/0.2 CPython/3.11.2
    Content-Type: application/json; charset=utf-8
    X-Frame-Options: DENY
    Content-Length: 37
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    "A lannister always pays their debts"

## Get Casterly Rock height

### Request

`GET /api/lannister/rock/650`

    curl -i -H 'Accept: application/json' http://localhost:8000/api/lannister/rock/650`

### Response

    HTTP/1.1 200 OK
    Date: Thu, 09 Mar 2023 01:01:26 GMT
    Server: WSGIServer/0.2 CPython/3.11.2
    Content-Type: application/json; charset=utf-8
    X-Frame-Options: DENY
    Content-Length: 28
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    "Casterly Rock is 651m tall

## Get list of Dragons

### Request

`GET /api/targaryen/dragons`

    curl -i -H 'Accept: application/json' http://localhost:8000/api/targaryen/dragons

### Response

    HTTP/1.1 200 OK
    Date: Thu, 09 Mar 2023 00:07:52 GMT
    Server: WSGIServer/0.2 CPython/3.11.2
    Content-Type: application/json; charset=utf-8
    X-Frame-Options: DENY
    Content-Length: 79
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    [{"name": "Drogon", "birth_year": 300}, {"name": "Rhaegal", "birth_year": 300}]

## Get list of Person

### Request

`GET /api/targaryen/person`

    curl -i -H 'Accept: application/json' http://localhost:8000/api/targaryen/person

### Response

    HTTP/1.1 200 OK
    Date: Thu, 09 Mar 2023 00:49:51 GMT
    Server: WSGIServer/0.2 CPython/3.11.2
    Content-Type: application/json; charset=utf-8
    X-Frame-Options: DENY
    Content-Length: 745
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    [
     {"id": 1, "birth_year": 281, "name": "Daenerys", "title": "Mother of Dragons", "full_name": "Daenerys Mother of Dragons"}, 
     {"id": 2, "birth_year": 81, "name": "Daemon", "title": "Prince of Dragonstone", "full_name": "Daemon Prince of Dragonstone"}
    ]

## Create a new Person

### Request

`POST /api/targaryen/person/`

    curl -i -H 'Content-Type: application/json' \
         -d '{"name": "Daenerys", "birth_year": 281, "title": "Mother of Dragons"}' \
         -X POST \
         http://localhost:8000/api/targaryen/person/


### Response

    HTTP/1.1 200 OK
    Date: Thu, 09 Mar 2023 00:23:13 GMT
    Server: WSGIServer/0.2 CPython/3.11.2
    Content-Type: application/json; charset=utf-8
    X-Frame-Options: DENY
    Content-Length: 79
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    {"id": 18, "name": "Daenerys", "title": "Mother of Dragons", "birth_year": 281}   

## Get a specific Person

### Request

`GET /api/targaryen/person/{id}`

    curl -i -H 'Accept: application/json' http://localhost:8000/api/targaryen/person/1

### Response

    HTTP/1.1 200 OK
    Date: Thu, 09 Mar 2023 00:26:07 GMT
    Server: WSGIServer/0.2 CPython/3.11.2
    Content-Type: application/json; charset=utf-8
    X-Frame-Options: DENY
    Content-Length: 121
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    {"id": 1, "birth_year": 281, "name": "Daenerys", "title": "Mother of Dragons", "full_name": "Daenerys Mother of Dragons"}

