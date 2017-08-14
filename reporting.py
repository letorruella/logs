#!/usr/bin/env python


import psycopg2

def top_articles():
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

    db.commit()
    db.close()
print(top_articles)    



# Top authors
def top_authors():
    
    db = psycopg2.connect('dbname=news')
    c = db.cursor()

    query = """ select name, sum(views) as views from pop_authors group by
                name order by views  desc limit 3;"""


    c.execute(query)
    rows = c.fetchall()
    print
    print "============================="
    print "The top authors are:"
    print
    for row in rows:
        print
        print row[0], row[1], "-views"

print top_authors()


def percent():
    db = psycopg2.connect('dbname=news')
    c = db.cursor()


    query = """select round((errors/count::decimal)*100, 2) results, err_status.date
        from err_status, total_status where err_status.date = total_status.date;"""


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

print percent()
