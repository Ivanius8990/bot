import re

from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Numeric, delete, insert


### удаляет ненужные символы и слова(такие как 'esport') из названия команды
def repl(team):
    team_lst = list(team)
    for i in range(len(team_lst) - 2):
        team_lst[i] = re.sub(r'[?!.@\'\" ]', '', team_lst[i])
        team_lst[i] = re.sub(r'esport', '', team_lst[i]).strip()
    return tuple(team_lst)


### возвращает совпавшие команды с правильным порядком коэффициентов
def match_finder(team1,team2):
    team1,team2=team1[1:],team2[1:]
    team1,team2=repl(team1),repl(team2)
    res=[(team1,team2) for s in team1[0:2] for i in team2[0:2] if s.find(i)!=-1 or i.find(s)!=-1]
    if len(res)==2:
        # print(res[0])
        xx = {
            'first_team': res[0][0][0],
            'second_team': res[0][0][1],
            'kef1-1': res[0][0][2],
            'kef1-2': res[0][0][3],
       }

        if res[0][0][0].find(res[0][1][0])==-1 and res[0][1][0].find(res[0][0][0])==-1:
            # print('обратный порядок')
            xx['kef2-1']= res[0][1][3],
            xx['kef2-2']= res[0][1][2],
        else:
            # print('прямой порядок')
            xx['kef2-1'] = res[0][1][2],
            xx['kef2-2'] = res[0][1][3],
        return xx

# x=('0','Atlantic esport', 'Fla"mes Ascent', 2.00000, 2.00000,)
# y=('1','Atlantic', 'Flames Ascent',  1.93000, 1.87000,)

engine = create_engine("postgresql+psycopg2://postgres:1234567@localhost/stavki")

conn = engine.connect()
x=conn.execute('SELECT * FROM marafon;').fetchall()
y=conn.execute('SELECT * FROM fonbet;').fetchall()

table=[]
no_match_table=[]
for i in x:
    for j in y:
        if match_finder(i,j):
            elem=match_finder(i,j)
            elem['teams']=elem['first_team']+" - "+elem['second_team']
            elem.pop("first_team")
            elem.pop("second_team")
            table.append(elem)
            print(match_finder(i,j).values())
        else:
            ### список без совпадений
            no_match=list(i[1:3])+list(j[1:3])
            no_match_table.append(no_match)

engine = create_engine("postgresql+psycopg2://postgres:1234567@localhost/stavki")
metadata = MetaData()
matches = Table('matches', metadata,
                Column('id', Integer(), primary_key=True),
                Column('teams', String(100), nullable=False),
                Column('kef1-1', Numeric(8, 5), nullable=False),
                Column('kef1-2', Numeric(8, 5), nullable=False),
                Column('kef2-1', Numeric(8, 5), nullable=False),
                Column('kef2-2', Numeric(8, 5), nullable=False)
                )


metadata.create_all(engine)
conn = engine.connect()
conn.execute('TRUNCATE TABLE matches RESTART IDENTITY;')
r = conn.execute(insert(matches), table)

print(f'Всего найдено {r.rowcount} матчей')
# print(len(no_match_table))



