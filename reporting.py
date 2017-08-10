#!/usr/bin/env python


import psycopg2

# Fetching tables from database and combine
# ====Top three article fetch===


db = psycopg2.connect('dbname=news')
c = db.cursor()


# Create a view named "path_ok" counts the all paths where the status is
# '200 OK'
query = """ create or replace view path_ok as select log.path, substring
            (path from 10 for 30), COUNT(*) AS VIEWS FROM log where status
            like '200 OK' GROUP BY  log.path; """

# create a view named "pop_articles" wich is combined with path_ok giving
# us a total of all articles
query = """create or replace view pop_articles as select views, substring,
            slug, title,id, author from path_ok, articles where slug =
            path_ok.substring order by views desc;"""



# Create a view "totals" total of dates with status
query = """create or replace view total_status as select  
            date(time) as date, count(status) as count
            from log  group by date;"""

# Create a view with status errors
query = """CREATE OR REPLACE VIEW  err_status AS SELECT to_char
            (time, 'Month DD, YYYY') as date, COUNT(status) as errors from log
            WHERE status = '404 NOT FOUND' GROUP BY date;"""

c.execute(query)
db.commit()
c.close()
db.close()


db = psycopg2.connect('dbname=news')
c = db.cursor()

query = "select title, views from pop_articles order  by views desc limit 3;"


c.execute(query)


rows = c.fetchall()


print
print "============================="
print "The top articles are:"
print
for row in rows:
    print
    print row[0], row[1], "-views"

# Top authors
query = """ select authors.name, pop_articles.views from pop_articles,
            authors where authors.id = pop_articles.author order by 
            views desc limit 3;"""


c.execute(query)
rows = c.fetchall()
print
print "============================="
print "The top authors are:"
print
for row in rows:
    print
    print row[0], row[1], "-views"


# Divide Errros fromm "err_status" by count from total_status
query = """select round((errors/count::decimal)*100, 2) results, err_status.date
    from err_status, total_status where err_status. date= total_status.date;"""


c.execute(query)
rows = c.fetchall()
print
print
print "============================="
print "Errror beyond 1% on:"
print

for row in rows:
    if row[0] > 1:
        print
        print row[1], "   ", row[0], "%"

db.commit()
db.close()
