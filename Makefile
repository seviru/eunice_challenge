AMOUNT ?= 20
EXCLUDE ?= "markets,learn,consensus-magazine"

db:
	docker-compose -f docker-compose.yaml -f services/db/docker-compose-db.yaml up -d
parser:
	docker-compose -f docker-compose.yaml -f services/db/docker-compose-db.yaml -f services/parser/docker-compose-parser.yaml up -d
archive:
	docker-compose -f docker-compose.yaml -f services/db/docker-compose-db.yaml -f services/archive/docker-compose-archive.yaml up -d
up:
	docker-compose -f docker-compose.yaml -f services/db/docker-compose-db.yaml -f services/parser/docker-compose-parser.yaml -f services/archive/docker-compose-archive.yaml up -d
down:
	docker-compose -f docker-compose.yaml -f services/db/docker-compose-db.yaml -f services/parser/docker-compose-parser.yaml -f services/archive/docker-compose-archive.yaml down
full_down:
	docker-compose -f docker-compose.yaml -f services/db/docker-compose-db.yaml -f services/parser/docker-compose-parser.yaml -f services/archive/docker-compose-archive.yaml down --rmi all
scrape: up
	docker exec -it eunice_challenge_parser python commands/parse_coindesk_latest_news.py --amount $(AMOUNT) --exclude $(EXCLUDE)

#################### DON'T USE THIS COMMAND. ONLY FOR DEVELOPMENT DESPERATE MEASURES ####################
raze: down
	docker system prune --all -f
#########################################################################################################