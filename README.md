# chamberlain
Accepts requests from an analyst in order to orchestrate computations between [cardinal](https://github.com/multiparty/cardinal) servers.
Maintains a database of locations of cardinal servers, available workflows to run, and available datasets to work with.

To run with the database add a .env file to the root of the directory with the following format
```
    MYSQL_HOST= "localhost"
    MYSQL_PORT= 3306
    MYSQL_USER= "root"
    MYSQL_PASSWORD= "********"
    MYSQL_DB= "chamberlain"
```

Please check the wiki of this repo for detailed instructions for setting up the cardinal-chamberlain system. 
