from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Numeric

engine = create_engine("postgresql+psycopg2://mrsmith:Flatron700?@localhost/stavki")
metadata = MetaData()

marafon = Table('marafon', metadata,
    Column('id', Integer(), primary_key=True),
    Column('first_team', String(100), nullable=False),
    Column('second_team', String(100), nullable=False),
    Column('kef1', Numeric(8, 5),  nullable=False),
    Column('kef2', Numeric(8, 5), nullable=False)

)


metadata.create_all(engine)

