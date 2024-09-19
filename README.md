
# Python Software Engineer Take Home Exercise


## Deliverables

- A Git Repository. Please do *NOT* use Github public repo.
  You can choose to make a Github private repository and invite us as an external collaborator to view your work;
- Complete the tasks outlined [below](#tasks)
- A [README](#readme) with instructions on both running the application and on design choices made


**Note:** We will discuss some of your design decisions and implementation in the technical interview

## Tasks

You are tasked with creating a program to scrape coindesk.com for the latest news articles and expose the data via API endpoints.

### Part 1: Backend Sourcing Program

1. Create a program that scrapes the most recent 20 news articles from coindesk.com.
2. Ignore any articles that are from `markets`, `learn`, `consensus-magazine` section. E.g. 
   `https://www.coindesk.com/markets/2024/07/27/bitcoin-prices-see-wild-trading-as-trump-plans-to-establish-btc-as-us-strategic-asset/`
   or 
   `https://www.coindesk.com/consensus-magazine/2024/07/08/what-hamster-kombat-did-how-telegram-built-a-web3-gaming-juggernaut/`
   should be ignored.
3. Store the scraped articles in PostgreSQL database. The database should have a table named `articles` with the following columns:
   - `id`: a unique identifier for the article
   - `title`: title of the article
   - `author`: author of the article
   - `published_at`: published timestamp of the article in UTC timezone
   - `content`: the content of the article
   - `url`: the url of the article
   - `tags`: a list of tags associated with the article. This should have already be privided in the article page.
5. The program must be able to be run from the command line and do not duplicate articles in the database.


### Part 2: API
1. Create an API that exposes the articles stored in the database.
2. The API should have the following endpoints:
   - `/articles`: returns a list of articles. Each article should have the following fields:
     - `title`
     - `published_at`
     - `snippet` (the first 150 characters of the content)
     - `url`
   - `/articles/<article_id>`: returns a single article with the same fields as above.

## README

- It should describe steps required for building and running locally.
- It should describe how to run tests locally.
- It should discuss any design decisions you made in building your application.

## Guidance

* Use python to accomplish this task.

* In the interest of time, we don't mind if you use a library like scrapy or beautifulsoup to help you acheive this task. 
  However, we will judge you on the **quality**, **readability** and **maintainability** of any code you provide us with. 
  Please try to keep the solution as simple as possible.

* We have provided you a docker-compose file to spin up a database to support
you in this task. For the script/api you author, don't worry about including any
docker commands, we can assume the database is already running prior to the
invocation of the script/api you provide.

### Starting a postgres database using the provided docker-compose.yaml

Ensure you have docker installed and then run the following command from the
root of this project
```
docker-compose up -d
```
Then to log into the database use the following credentials:

* user: eunice
* password eunice
* host: localhost
* port: 5433 -- note this isn't the standard port to avoid clashing with any locally running postgres db

To stop the database and clean-up run:
```
docker-compose down -v --rmi all
```
