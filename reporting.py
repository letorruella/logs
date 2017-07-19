import psycopg2 #import library2


#Fetching tables from database and combine
db = psycopg2.connect('dbname=news')
c = db.cursor() 
query = "select articles.title, count(*) as views  from articles join log on articles.slug \
         = (regexp_split_to_array(path, '/article/'))[2] where path !='/' group by  \
        (regexp_split_to_array(path, '/article/'))[2], articles.title order  by views desc limit 3;"

c.execute(query)
rows=c.fetchall()
print ("The Top three articles are:")
print(rows)
db.close()





