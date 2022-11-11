from json import dumps
from sqlalchemy.dialects import postgresql
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Numeric

#
a=[{'marafon': '1.0'}, {'fonbet': '1.5', }]
b=[{'marafon': '1.1'}, {'fonbet': '1.3', }]

a=dumps(a)
b=dumps(b)
#
table = {
            'teams': 'team spirit - amblud',
            'kef1': a,
            'kef2': b
       }


engine = create_engine("postgresql+psycopg2://postgres:1234567@localhost/stavki")
metadata = MetaData()
marafon = Table('ffff', metadata,
                Column('id', Integer(), primary_key=True),
                Column('teams', String(100), nullable=False, unique=True),
                Column('kef1', String(200)),
                Column('kef2', String(200))
                )

metadata.create_all(engine)
conn = engine.connect()


# conn.execute('TRUNCATE TABLE ffff RESTART IDENTITY;')

x=conn.execute('SELECT * FROM ffff;').fetchone()
insert_stmt = postgresql.insert(marafon).values(table)
update_columns = {col.name: col for col in insert_stmt.excluded if col.name not in ('id','teams')}

update_stmt = insert_stmt.on_conflict_do_update(
    index_elements=['teams'],
    set_=update_columns
)

conn.execute(update_stmt)
print(x[2])