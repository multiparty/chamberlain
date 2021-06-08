# chamberlain
Accepts requests from an analyst in order to orchestrate computations between cardinal (and then congregation) servers.
Maintains a database of mappings between dataset IDs and IPs of cardinal servers that own shares of those datasets.

To run with the database add a .env file to the root of the directory with the following format
```
    MYSQL_HOST= "localhost"
    MYSQL_PORT= 3306
    MYSQL_USER= "root"
    MYSQL_PASSWORD= "********"
    MYSQL_DB= "chamberlain"
```