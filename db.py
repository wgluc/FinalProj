# Create database
DBNAME = 'spotifybillboard.db'
CHARTJSON = 'cached_chart.json'
MUSICJSON = 'cached_music.json'

def init_db():
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Artist_Data';
    '''

    cur.execute(statement)
    conn.commit()

    statement = '''
        DROP TABLE IF EXISTS 'Chart_Data';
    '''

    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Artist_Data' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Artist' TEXT,
            'Best Song' TEXT,
            'Followers' TEXT,
            'Genres' TEXT,
            'Popularity' INTEGER,
            'Type' TEXT,
            'uri' TEXT,
        );
    '''

    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Chart_Data' (
            'Position' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Peak Position' INTEGER,
            'Previous Position' INTEGER,
            'Weeks Charting' INTEGER,
            'Artist' TEXT,
            'Song' TEXT,
        );
    '''

    cur.execute(statement)
    conn.commit()
    conn.close()

def populate_chart():
    conn = sqlite3.connect('spotifybillboard.db')
    cur = conn.cursor()

    populate_dict = get_billboard()
    chart_dict = {}
    count = 1

    for c in populate_dict.keys():
        Position = c
        Peak_Position = populate_dict.keys[c][2]
        Previous_Position = populate_dict.keys[c][4]
        Weeks_Charting = populate_dict.keys[c][3]
        Artist = populate_dict.keys[c][1]
        Song = populate_dict.keys[c][0]

        insertion = (None, Position, Previous_Position, Weeks_Charting, Artist,
        Song)
        statement = 'INSERT INTO "CHART_DATA" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()

    f = open(MUSICJSON, 'r')
    fcontents = f.read()
    music_data = json.loads(fcontents)
    music_dict = {}
    counter = 1



        insertion = (None, line[0], line[1], line[2], line[3], line[4][:-1],
        line[5], locId, line[6], line[7], line[8], beanid)
        statement = 'INSERT INTO "Bars" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()
