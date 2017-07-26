import psycopg2

# Fetching tables from database and combine
# ====Top three article fetch===
db = psycopg2.connect('dbname=news')
c = db.cursor()
query = """select articles.title, count(*) as views  from articles join log on
        articles.slug = (regexp_split_to_array(path, '/article/'))[2] where
        path!='/' group by(regexp_split_to_array(path, '/article/'))[2],
        articles.title order  by views desc limit 3;"""
c.execute(query)
rows = c.fetchall()
print ("The Top three articles are:")
print
# looping the object

for row in rows:
    print row[0], row[1], "- views"


db.close()

# =====Most popular authors====


db = psycopg2.connect('dbname=news')
c = db.cursor()
query = """select authors.name, count(log.path) as views from authors left join
            articles on authors.id = articles.author left join log on log.path
            like concat('%', articles.slug) group by authors.name order by
            views desc;"""

c.execute(query)
rows = c.fetchall()
print
print ("The Top Most Popular authors:")
print

for row in rows:
    print row[0], row[1]

print
print

db = psycopg2.connect('dbname=news')
c = db.cursor()

# create an error table
query = """create or replace view error AS
            select to_char(time, 'Month DD, YYYY') as date,
            count(status) as err, status
            from log where status = '404 NOT FOUND'
            group by date, status
            order by date ASC;
            create view"""

# create a date table
query = """create or replace total AS
          select to_char(time, 'Month DD, YYYY') as date,
          count(status) as total
         from log group by date order by date asc;
        """

query = "select date, err_val*100 from rate"
c.execute(query)
rows = c.fetchall()

for row in rows:
    res = row[0], round(row[1])
    if res[1] > 1.5:
        print
        print '%s, %i percent Errors '  % res 

