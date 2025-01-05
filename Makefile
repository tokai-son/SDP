compose:
	docker-compose -f deployment/docker-compose.yaml up
compose-build:
	docker-compose -f deployment/docker-compose.yaml up --build
