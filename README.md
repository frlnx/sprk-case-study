# SPRK Coding Challenge
Thank you for the challenge, it was fun.

As I am coming to the end of the timebox I allowed myself, I will make some final remarks here.

Known issues:
 - 
 - I assumed duplicates could only come in the form of entries with different amount of leading zeros. I notice 
now that this is not the case. I still think my implementation will prove interesting. This mistake can be rectified
relatively easily.
 - The docker files should be built in a two step build process, to make them smaller.

Pattern used
-
I have used a Service-Provider pattern as a base for my application. I prefer this pattern because of the ability to
layer tests, which comes in handy when working with docker specifically. This pattern is way too heavy for such a small
project, but I wanted to show off.

Data models
-
I chose to keep the database and models lightweight. Normalising data is something I used to be very fond of, but
it often leads to pre-optimization and cumbersome database migrations.
The methodology I use keeps the original data, and applies on-the-fly migrations of data as data is fetched from the
repository.
The advantages of this being
 - Flexibility, The database backends cannot just be switched to which ever your ORM supports, but any key value store
is supported.
 - With no schema, there are no database migrations that can fail, leading to downtime.
 - With no schema, there is no need to duplicate the production database to ensure compatibility with old data
after a migration.
 - With on the fly migrations, the data can be kept pristine and immutable. This brings the advantage of the data being
cacheable and available in a distributed form without concurrency issues.

Tests
-
There are three layers of tests
 - Unit ie. tests/test_service.py
 - Integration ie. tests/test_integration.py
 - Acceptance ie. acceptance_tests/test_acceptance.py

All part of the different scopes, none of them 100% covering but it shows the principle of layering tests.

Final words
-
I know I made this challenge in a different way than described. I hope it will provide interesting discussions and
mutually beneficial exchanges in all directions.