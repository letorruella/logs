# logs
 
A basic program that asnwers threee questions based on a provided data


## This project requires certain dependencies such as:

PostgreSQL
Psycopg2 API
Python 
Vagrant ("bento/ubuntu-16.04-i386")
Virtual box



## To run it got to the log directory and run it:
The data was provided by my school and was manipulated in an virtual machine(vagarant) wih postgresql 

After that I follow this steps.

1.Import the data into the script with Psycopg2
2.Create the below VIEWS
3.Run the script(you know how to run a script. Right?)



# Make sure you create the following VIEWS:


## path_ok: counts the all paths where the status is '200 OK'
 
            CREATE OR REPLACE VIEW path_ok AS select log.path, substring
            (path from 10 for 30), COUNT(*) AS VIEWS FROM log WHERE status
            LIKE '200 OK' GROUP BY  log.path; 


## pop_articles: wich is combined with path ok giving us a total of all articles

            CREATE OR REPLACE VIEW pop_articles AS SELECT views, substring,
            slug, title,id, author FROM path_ok, articles WHERE slug =
            path_ok.substring ORDER BY views DESC;


## total_status: gets all the logs regardless its status code
            
            CREAT OR REPLACE VIEW total_status AS SELECT  
            date(time) AS date, COUNT(status) AS count
            FROM log  GROUP BY date;


## err_status: gets logs with status(404)

            CREATE OR REPLACE VIEW  err_status AS SELECT to_char
            (time) AS date, COUNT(status) AS errors FROM log
            WHERE status = '404 NOT FOUND' GROUP BY date;





__WARNING: Data not provided since it's to big :-(__
