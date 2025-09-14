.PHONY: init build up down logs clean

init:
	@chmod +x ./bin/setup-project.sh
	@./bin/setup-project.sh

build:
	@cd app && docker-compose build

up:
	@cd app && docker-compose up -d

down:
	@cd app && docker-compose down

logs:
	@cd app && docker-compose logs -f

clean:
	@docker system prune -f
	@docker volume prune -f
