start-dev:
	docker-compose up

start-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

stop-compose:
	docker-compose down

ssh-nginx:
	docker exec -it nginx_server bash