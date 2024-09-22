# Python Software Engineer Take Home Solution Explanation

## Intro

This is the main deliverable for the challenge described on the [README_CHALLENGE_DESCRIPTION](README_CHALLENGE_DESCRIPTION.md)
file.

## About testing

### Requirements

- To have docker installed on your machine.
- Port 8080 available for the API. Otherwise, you can modify [the docker-compose file](./services/archive/docker-compose-archive.yaml)
to one that you have available.


### Instructions for running the application and the tests

On the same folder of this README there is a [Makefile](./Makefile) with a lot of commands to run for different purposes.

If you just want a single command to run the whole application and execute a test run, being on the directory of
this same README use:
```
make test_integration_manual
```
This command will run the scraping with the default parameters (20 articles, skipping `markets`, `learn` 
and `consensus-magazine` categories), storing those 20 articles on the database and executing an API request to
the archive API to retrieve them (the endpoint for all of them, and a random one from the single article endpoint).

If you want to play with the parameters of the scraping, you can use:
```
make scrape AMOUNT=<INTEGER_NUMBER> EXCLUDE="<CATEGORY_1,CATEGORY_2,CATEGORY_3>"
```
and following, use the command
```
make retrieve_articles
```
to call the archive API and return the last 20 (paginated response) from the articles listing endpoint, and a random
one from the single article endpoint. You can also call the API manually using a program like postman by calling the
`http://localhost:5555/api/articles` and `http://localhost:5555/api/articles/{id}` endpoints.

At any point after running the
```
make scrape (...)
```
command, you can get into your database and check them manually too.

## About the code

There are 3 main services that separate concerns on the application:

- archive: Is the publicly exposed API that we can call to retrieve the data stored in our database related to the articles.
- db: Database where we will store the information related to our articles.
- parser: Is the core program that does the web scrapping and stores the information into the database. Run It from the command line.

### Underlying design choices

Some design choices that go across the three services, without any particular link between them:

- I decided to separate the services from the start since they are going to have different requirements and didn't want 
to get the dependencies all mixed up. Also, don't want them to be tightly coupled and this is the most straightforward
way to achieve It (could go with modular monolith but is not as quick as this).
- I also decided to separate between parser and archive since I feel that the responsibility for storing/retrieving
information from the archive should be on the archive service, maybe by a gRPC call or consuming some kind of message from
a queue that has the information It has to store. I feel like this goes way out of scope for this test so parser will
need to have direct access to the DB from the parser to write on It. That's also why the DB is It's own service instead 
of belonging to the archive service, just for the matter of simplicity.
- Some things like the logger could be a common custom library that all my services use, but again I feel like that is out
of scope for this exercise.
- Currently the logger ob both archive and parser services writes to rotating files in case you want to check It out for 
reviewing this exercise. For a prod environment I would use rotating files, or just plain skip this if we have our logs 
stored by some commercial app like Datadog or so.
- For the given moment, I've decided to skip all concurrency handling with locks and so on, since It adds complexity and
I don't see much of a point for this use case. Also, if I went with my ideal approach which would be throwing jobs in a
queue that happen sequentially I feel like a lot of these issues wouldn't be even a concern.
- I usually would write automated tests for everything, but given the size of the assignment I decided to go this time for
a manual showcase of the system work by using a manual script test.
- Even though I could have used something like SQLAlchemy for handling the database models, and more in depth building
with psycopg2 to make service-wide connector and so on, since I'm only will be having 3 touch points to the database
(write the article, retrieve a particular one and retrieve all) I decided for the sake of simplicity just do It case-based.
- Also, about some vital variables spread around the code like database passwords and so on. I know that those should be on a secret
variable for production, or even be on an environment variables file and then load It as a configuration on the app instead
of having It hardcoded in there. I thought that for a test It's okay to leave It like that, but I would never do It on
code to send to production.

### Archive design choices

It's a basic API where I separated the concerns of presentation layer, business logic layer (even though there is not much)
and data layer. Each of the features of the API should be self contained (except for the features on common).

Some design choices about the archive, without any particular link between them:

- A lot of the things that I've hardcoded on the articles repository like the connection to the database and so on It would
typically go into a different class that all repositories that connect to the postgres database will inherit from, but since
for this case we only have that one I'll roll with It like that.

### Database design choices

There is not much to say here, It's just a database exposed to both services that allows us to store the articles.

Some design choices about the database, without any particular link between them:

- I added the table creation as an init script for the sake of simplicity. If this was a real application looking to scale,
I would use something like alembic to separate between DDLs and DMLs, while also having the database version control by
having the up revisions and down revisions.

### Parser design choices

From the code point of view this may be the most complex one (there is a bit of abstraction to all the elements) on the code.

We have the entrypoint for the parsing on the [parse_coindesk_latest_news.py](./services/parser/commands/parse_coindesk_latest_news.py) file.
You can give to It arguments like the max amount of articles you want to retrieve (default 20) and the categories you want
to skip (default `markets`, `learn` and `consensus-magazine`).

My idea was creating a reusable way of carrying out the web scrapping, hence the [ParserOrchestrator](./services/parser/app/orchestration/parser_orchestrator.py).
This is a class that by inputting a configuration (done through a factory if you want, like on the case of the exercise) that contains
the 3 key components of execution:
- [URL retrievers:](./services/parser/app/url_retriever) Retrieves the URL for news that match a certain criteria
- [Page data extractors](./services/parser/app/extractor): Takes those URLs and fetches the needed information from them
- [Page information storers](./services/parser/app/storer): Takes that information and stores It through a repository.

Note that all of these elements are defined by a given set of interfaces, so If at any point we want to change how each of
each of those steps work (like pushing the information to a queue instead of storing in a database), as long as they respect
the interface we can replace It in our orchestrator without issue. I did It this way so if we want to improve any part of
the code individually, we don't need to change the whole application, just that particular step.

Some design choices about the parser, without any particular link between them:

- On the coindesk pages retriever, I decided to go with the one that retrieves the articles following the current structure
of the page by date, since ensuring the opposite is pretty heavyweight (parse all links and order them). If in the future
this changes, we can just change this part of the code since the retrieval is not coupled with anything else.
- Also, for the sake of simplicity, I decided to only retrieve english articles.
- Also, since I caught the API call to retrieve the news, I think It's more sustainable to crawl the direct API call than
to do the content returned. Sadly, when I want the full information of the new (like the content) I have to acces the HTML
since It is what is returned from the backend (or at least I didn't catch the API call).
- I know doing the whole parsing and then checking if we don't have the article on the database is not very performant,
but It was the low hanging fruit to ensure avoiding duplications. Other way of doing It could be having a URL validation
step on our orchestrator before parsing the page information, but I think that for this case and just for a test this
solution is OK (we are just parsing 20 articles, not 2000!).

## Closing thoughts

All in all, It was an interesting project to work on. Even though with the self-imposed limitations that I wouldn't do for
a production-ready code, I hope you find this code suitable for the standards of this test!

Also a last disclaimer, if you run this code plenty of times the `/logs` folders in both the parser and archive will begin
to increase in size. Remember to remove them when you are done testing!
