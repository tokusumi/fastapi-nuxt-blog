docker-compose run --rm fastapi pytest --cov=app/blogs --disable-warnings --cov-report=term-missing
docker-compose run --rm fastapi rm -f test_temp.db