import os
import sqlite3


def LOAD_DB_TO_DICT(db):
    con = sqlite3.connect(db)
    cur = con.cursor()

    LIBS_IDS = cur.execute('SELECT LIB_ID FROM LIBRARIES').fetchall()
    LIBS = cur.execute('SELECT LIB FROM LIBRARIES').fetchall()
    DESCRIPTIONS = cur.execute('SELECT DESCRIPTION FROM LIBRARIES').fetchall()
    LINKS = cur.execute('SELECT LINK FROM LIBRARIES').fetchall()

    libsData = dict()

    for i in range(len(LIBS)):
        libsData[LIBS_IDS[i][0]] = {
            'Name': LIBS[i][0],
            'Description': DESCRIPTIONS[i][0],
            'Link': LINKS[i][0],
            'Templates': None
        }

    for i in LIBS_IDS:
        names = cur.execute(f'SELECT NAME FROM TEMPLATES WHERE LIB_ID = {i[0]}').fetchall()
        contents = cur.execute(f'SELECT CONTENT FROM TEMPLATES WHERE LIB_ID = {i[0]}').fetchall()
        templates = dict()
        for j in range(len(names)):
            templates = dict()
            templates[names[j][0]] = contents[j][0]
        libsData[i[0]]['Templates'] = templates

    return libsData


def GET_DATA_FROM_DICT(dictt):
    LIBS_IDS = []
    for idd in dictt.keys():
        LIBS_IDS.append(idd)
    LIBS = []
    DESCRIPTIONS = []
    LINKS = []
    for i in range(len(LIBS_IDS)):
        LIBS.append(dictt[LIBS_IDS[i]]['Name'])
        DESCRIPTIONS.append(dictt[LIBS_IDS[i]]['Description'])
        LINKS.append(dictt[LIBS_IDS[i]]['Link'])

    T_NAMES = []
    T_CONTENTS = []
    for i in range(len(LIBS_IDS)):
        T_NAMES.append(list(dictt[LIBS_IDS[i]]['Templates'].keys()))
        T_CONTENTS.append(list(dictt[LIBS_IDS[i]]['Templates'].values()))

    return ([LIBS_IDS, LIBS, DESCRIPTIONS, LINKS], [T_NAMES, T_CONTENTS])


def DUMP_FROM_DICT_TO_DB(dictt):
    db = os.path.abspath('compilation-of-python-libs-docs/DATA.db').replace('\\', '/')
    db = db[:-len('compilation-of-python-libs-docs/DATA.db')] + 'DATA.db'
    dbb = db + '_backup'
    if os.path.isfile(dbb):
        os.remove(dbb)
    os.rename(db, dbb)
    # os.remove(db)

    ([LIBS_IDS, LIBS, DESCRIPTIONS, LINKS], [T_NAMES, T_CONTENTS]) = GET_DATA_FROM_DICT(dictt)
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('VACUUM')

    cur.execute('PRAGMA foreign_keys = off')
    cur.execute('BEGIN TRANSACTION')
    cur.execute(
        'CREATE TABLE LIBRARIES (LIB_ID INTEGER, LIB STRING, DESCRIPTION TEXT, LINK STRING)')

    for i in range(len(LIBS_IDS)):
        cur.execute(
            f"INSERT INTO LIBRARIES (LIB_ID, LIB, DESCRIPTION, LINK) VALUES ('{LIBS_IDS[i]}', '{LIBS[i]}', '{DESCRIPTIONS[i]}', '{LINKS[i]}')")

    cur.execute('CREATE TABLE TEMPLATES (LIB_ID INTEGER, NAME STRING, CONTENT TEXT)')

    for i in range(len(LIBS_IDS)):
        for j in range(len(T_NAMES[i])):
            cur.execute(
                f"INSERT INTO TEMPLATES (LIB_ID, NAME, CONTENT) VALUES ('{LIBS_IDS[i]}', '{T_NAMES[i][j]}', '{T_CONTENTS[i][j]}')")
    cur.execute('COMMIT TRANSACTION')
    cur.execute('PRAGMA foreign_keys = on')
    con.close()
