start-dev:
	docker-compose up
	
stop-dev:
	docker-compose down

start-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up