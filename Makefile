up:
	docker-compose -f docker-compose.yaml -f services/db/docker-compose-db.yaml -f services/parser/docker-compose-parser.yaml up -d
down:
	docker-compose -f docker-compose.yaml -f services/db/docker-compose-db.yaml -f services/parser/docker-compose-parser.yaml down
full_down:
	docker-compose -f docker-compose.yaml -f services/db/docker-compose-db.yaml -f services/parser/docker-compose-parser.yaml down --rmi all
