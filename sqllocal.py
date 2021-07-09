import sqlite3

con = sqlite3.connect(r"E:/sqlite3/test.db")
cur = con.cursor()


def create():
    cre = r'create table test (ID integer primary key  autoincrement,Sheet int not null default(0),R int not null,' \
         r'C int not null,old char(50),new char(50));'
    crea = r'create table version (S int not null default(0),R int not null,C int not null,old char(50),' \
           r'new char(50), murder char (50),primary key(S,R,C));'
    cur.execute(crea)
    con.commit()


def init():
    dict = []
    query = r'select * from version;'
    res = cur.execute(query)
    for i in res:
        dict.append(i)
        # print(i)
    return dict


def select_all():
    sel = r'select * from version;'
    res = cur.execute(sel)
    for i in res:
        print(i)


def select(s, r, c):
    sel = r'select new from version where S={0} and R={1} and C = {2};'
    res = cur.execute(sel.format(s, r, c))
    for i in res:
        return i

# create()
# init()
if select(100,1000,100) == None:
    print(1)
# init()
# cur.close()