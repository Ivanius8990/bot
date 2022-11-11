# from sqlalchemy import create_engine
#
#
# engine = create_engine("postgresql+psycopg2://postgres:1234567@localhost/stavki")
#
# conn = engine.connect()
# x=conn.execute('SELECT * FROM marafon;')
# y=conn.execute('SELECT * FROM fonbet;')
#
# print(x.fetchone())
# print(y.fetchone())

x=('Team Secret', 'Tundra Esports', 2.00000, 2.00000,)
y=('Team Secret', 'Tundra Esports',  1.93000, 1.87000,)

def match_finder(team1,team2):
    res=[(team1,team2) for s in team1[0:2] for i in team2[0:2] if s.find(i)!=-1 or i.find(s)!=-1]
    if len(res)==2:
        print(res[0])
        xx = {
            'first_team': res[0][0][0],
            'second_team': res[0][0][1],
            'kef1-1': res[0][0][2],
            'kef1-2': res[0][0][3],
       }
        if res[0][0][0].find(res[0][1][0])!=0:
            print('обратный порядок')
            xx['kef2-1']= res[0][1][3],
            xx['kef2-2']= res[0][1][2],
        else:
            print('прямой порядок')
            xx['kef2-1'] = res[0][1][2],
            xx['kef2-2'] = res[0][1][3],
    return xx

print(match_finder(x,y))