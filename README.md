# Logs





 
A basic program that analyses a PostgreSQL database of a fictional news website which allowed me to find the aswers to the following questions.



1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer back to this lesson if you want to review the idea of HTTP status codes.)





#The data contains three tables:

The authors table, this table hold three columns the author's name and a basic bio and their respective id.

The articles table, eventhough this tables holds many columns , eg time, body, you can call check them out in psql to see them all, but three colum, (slug, title, id)   help me find the insights in the my program.

The last table is the log, this is the most useful since it contains all the events that happened of the fictional websites. You can always consult the data for more detailed information, I used path, status and time.  	
 


## This project requires certain dependencies which are included in this repo:

PostgreSQL 

Psycopg2 API

Python 

Vagrant ("bento/ubuntu-16.04-i386")

NewsData(https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.z)



## To run it:

Download the data

Make sure your enviroment is prepared (Postgresql and psycopg) you can also use the vagrant file included in this repo.

Connect to the news data in your terminal and create the views below 

Run the script and the insights will be printed out









# VIEWS:


## path_ok: counts the all paths where the status is '200 OK'
 
            CREATE OR REPLACE VIEW path_ok AS select log.path, substring
            (path from 10 for 30), COUNT(*) AS VIEWS FROM log WHERE status
            LIKE '200 OK' GROUP BY  log.path; 


## pop_articles: wich is combined with path ok giving us a total of all articles

            CREATE OR REPLACE VIEW pop_articles AS SELECT views, substring,
            slug, title,id, author FROM path_ok, articles WHERE slug =
            path_ok.substring ORDER BY views DESC;


## pop_authors: wich is combined with path ok giving us a total of all articles

          CREATE OR REPLACE VIEW pop_authors AS SELECT pop_articles.views, pop_articles.author, authors.name, authors.id FROM pop_articles, authors WHERE pop_articles.author = authors.id ORDER by views DESC;

## total_status: gets all the logs regardless its status code
            
            CREATE OR REPLACE VIEW total_status AS SELECT  
            date(time) AS date, COUNT(status) AS count
            FROM log  GROUP BY date;


## err_status: gets logs with status(404)

            CREATE OR REPLACE VIEW  err_status AS SELECT date(time) AS date, COUNT(status) AS errors FROM log
            WHERE status = '404 NOT FOUND' GROUP BY date;




