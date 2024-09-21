- I decided to separate the services from the start since they are going to have different requirements and didn't want 
to get the dependencies all mixed up. Also, don't want them to be tightly coupled and this is the most straightforward
way to achieve It (could go with modular monolith but is not as quick as this).
- I also decided to separate between parser and archive since I feel that the responsibility for storing/retrieving
information from the archive should be on the archive service, maybe by a gRPC call or consuming some kind of message from
a queue that has the information It has to store. I feel like this goes way out of scope for this test so parser will
need to have direct access to the DB from the parser to write on It. That's also why the DB is It's own service instead 
of belonging to the archive service, just for the matter of simplicity.
- I added the table creation as an init script for the sake of simplicity. If this was a real application looking to scale,
I would use something like alembic to separate between DDLs and DMLs, while also having the database version control by
having the up revisions and down revisions.
- On the coindesk pages retriever, I decided to go with the one that retrieves the articles following the current structure
of the page by date, since ensuring the opposite is pretty heavyweight (parse all links and order them). If in the future
this changes, we can just change this part of the code since the retrieval is not coupled with anything else.
- Also, for the sake of simplicity, I decided to only retrieve english articles.
- Also, since I caught the API call to retrieve the news, I think It's more sustainable to crawl the direct API call than
to do the content returned. Sadly, when I want the full information of the new (like the content) I have to acces the HTML
since It is what is returned from the backend (or at least I didn't catch the API call).
- Even though I could have used something like SQLAlchemy for handling the database models, and more in depth building
with psycopg2 to make service-wide connector and so on, since I'm only will be having 3 touch points to the database
(write the article, retrieve a particular one and retrieve all) I decided for the sake of simplicity just do It case-based.
- For the given moment, I've decided to skip all concurrency handling with locks and so on, since It adds complexity and
I don't see much of a point for this use case. Also, if I went with my ideal approach which would be throwing jobs in a
queue that happen sequentially I feel like a lot of these issues wouldn't be even a concern.
- Currently the logger writes to a file in case you want to check It out for reviewing this exercise. For a prod environment
I would use rotating files, or just plain skip this if we have our logs stored by some commercial app like Datadog or so.
- Some things like the logger could be a common custom library that all my services use, but again I feel like that is out
of scope for this exercise.
- A lot of the things that I've hardcoded on the articles repository like the connection to the database and so on It would
typically go into a different class that all repositories that connect to the postgres database will inherit from, but since
for this case we only have that one I'll roll with It like that.