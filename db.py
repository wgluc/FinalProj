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
            'Position' TEXT,
            'Peak Position' TEXT,
            'Previous Position' TEXT,
            'Weeks Charting' TEXT,
            'Artist' TEXT,
            'Song' TEXT,
        );
    '''

    cur.execute(statement)
    conn.commit()
    conn.close()

def populate_db():
    conn = sqlite3.connect('spotifybillboard.db')
    cur = conn.cursor()

    populate_dict = get_billboard()

    for c in populate_dict.keys():
        Position = c
        Peak_Position = populate_dict.keys[c][2]
        Previous_Position = populate_dict.keys[c][4]
        Weeks_Charting = populate_dict.keys[c][3]
        Artist = populate_dict.keys[c][1]
        Song = populate_dict.keys[c][0]

        insertion = (Position, Peak_Position, Previous_Position, Weeks_Charting,
        Artist,Song)
        statement = 'INSERT INTO "CHART_DATA" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()

    f = open(MUSICJSON, 'r')
    fcontents = f.read()
    music_data = json.loads(fcontents)

    for x in music_data.keys:
        Artist = x
        Best_Song = get_top_tracks(x)[0]
        Followers = music_data[x]['artists']['items'][0]['followers']['total']
        Genres = ''.join(music_data[x][]['artists']['items'][0]['genres'])
        Popularity = music_data[x]['artists']['items'][0]['popularity']
        Type = music_data[x]['artists']['items'][0]['type']
        uri = music_data[x]['artists']['items'][0]['uri']

        insertion = (None, Artist, Best_Song, Followers, Genres, Popularity,
        Type, uri)
        statement = 'INSERT INTO "Artist_Data" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

init_db()
populate_db()
