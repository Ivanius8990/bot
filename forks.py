from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Numeric, delete, insert



engine = create_engine("postgresql+psycopg2://postgres:1234567@localhost/stavki")

conn = engine.connect()
x=conn.execute('SELECT * FROM matches;').fetchall()

for i in x:
    max_kef1=max(i[3],i[5])
    max_kef2=max(i[4],i[6])
    fork=1/max_kef1+1/max_kef2
    print(i[0:3],round(fork,3))
    if float(fork) < 1:
        print(i,'fork',round(fork,3))
