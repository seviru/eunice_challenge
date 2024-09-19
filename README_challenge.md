- I decided to separate the services from the start since they are going to have different requirements and didn't want 
to get the dependencies all mixed up. Also, don't want them to be tightly coupled and this is the most straightforward
way to achieve It (could go with modular monolith but is not as quick as this).
- I also decided to separate between parser and archive since I feel that the responsibility for storing/retrieving
information from the archive should be on the archive service, maybe by a gRPC call or consuming some kind of message from
a queue that has the information It has to store. I feel like this goes way out of scope for this test so parser will
need to have direct access to the DB to write on It. That's also why the DB is It's own service instead of belonging to
the archive domain, just for the matter of simplicity.
