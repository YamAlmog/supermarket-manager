



## How to run tests in docker?
```
docker-compose up -d --build  # Start your FastAPI app
docker-compose exec fastapi_app pytest  # Run pytest inside the container
```
