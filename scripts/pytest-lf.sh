docker-compose run --rm fastapi pytest --lf --disable-warnings
docker-compose run --rm fastapi rm -f test_temp.db