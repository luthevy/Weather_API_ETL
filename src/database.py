"""
	This source is used for processing database relevant operations
"""
from asyncio.windows_events import NULL
from datetime import datetime, timedelta
import json
import sqlite3
from utilities import progress


def json_preprocessing(file_name):
    """
    Transform value of json object into suitable type
    :param: str file_name : name of json file
    :return: transformed data
    """
    with open(file_name, 'r+') as json_file:
        data = json.load(json_file)
        data["d"] = datetime.utcfromtimestamp(
            data["d"]).strftime('%d/%m/%Y, %H:%M:%S')
        data['imzon'] = str(timedelta(seconds=data['imzon']))
        data['y']['unri'] = datetime.utcfromtimestamp(
            data['y']['unri']).strftime('%d/%m/%Y, %H:%M:%S')
        data['y']['un'] = datetime.utcfromtimestamp(
            data['y']['un']).strftime('%d/%m/%Y, %H:%M:%S')
        data['y']['id'] = str(data['y']['id'])
        data['y']['yp'] = str(data['y']['yp'])
        data['id'] = str(data['id'])
        data['cod'] = str(data['cod'])
        data['wahr']['id'] = str(data['wahr']['id'])
        json_file.seek(0)
        json.dump(data, json_file)
        json_file.truncate()


def load_data(col, tag, file_name):
    """
    Return json object value at given position
    :param: str file_name : name of json file
                    str col : name of nested object
                    str tag : name of object inside that nested object
    :return: str/integer object
    """
    try:
        with open(file_name) as json_file:
            data = json.load(json_file)
        return data[col][tag]
    except:
        try:
            with open(file_name) as json_file:
                data = json.load(json_file)
            return data[tag]
        except:
            return NULL


def insert_db(conn, cur, file_name):
    """
    Insert value into sqlite3 database
    :param: conn : sqlite3 connection module
                    cur : sqlite3 cursor module
                    str file_name: name of json file
    """
    # First, check if any records in given database table
    cur.execute(''' SELECT count(coord_id) FROM GEOLOC_DIMEN ''')
    if cur.fetchone() != 0:
        rows = cur.execute(''' SELECT nam FROM GEOLOC_DIMEN ''').fetchall()
        nam = load_data("", "nam", file_name)
        if nam not in rows:
            # If having records, check duplicates
            lon = load_data("coord", "lon", file_name)
            la = load_data("coord", "la", file_name)
            imzon = load_data("", "imzon", file_name)
            id = load_data("", "id", file_name)
            cod = load_data("", "cod", file_name)
            cur.execute('INSERT into GEOLOC_DIMEN(coord_lon,coord_la,imzon,id,nam,cod) VALUES(%f,%f,%s,%s,%s,%s)' % (
                lon, la, "\""+imzon+"\"", "\""+id+"\"", "\""+nam+"\"", "\""+cod+"\""))
    else:
        # If not, insert new record
        nam = load_data("", "nam", file_name)
        lon = load_data("coord", "lon", file_name)
        la = load_data("coord", "la", file_name)
        imzon = load_data("", "imzon", file_name)
        id = load_data("", "id", file_name)
        cod = load_data("", "cod", file_name)
        cur.execute('INSERT into GEOLOC_DIMEN(coord_lon,coord_la,imzon,id,nam,cod) VALUES(%f,%f,%s,%s,%s,%s)' % (
            lon, la, "\""+imzon+"\"", "\""+id+"\"", "\""+nam+"\"", "\""+cod+"\""))

    # Insert records process for WEATHER_DIMEN table
    cur.execute(''' SELECT count(wahr_id) FROM WEATHER_DIMEN ''')
    if cur.fetchone() != 0:
        rows = cur.execute(
            ''' SELECT wahr_id FROM WEATHER_DIMEN ''').fetchall()
        wahr_id = load_data("wahr", "id", file_name)
        if wahr_id in rows:
            main = load_data("wahr", "main", file_name)
            dcripion = load_data("wahr", "dcripion", file_name)
            icon = load_data("wahr", "icon", file_name)
            cur.execute('INSERT into WEATHER_DIMEN VALUES(%s,%s,%s,%s)' % (
                "\""+wahr_id+"\"", "\""+main+"\"", "\""+dcripion+"\"", "\""+icon+"\""))
    else:
        wahr_id = load_data("wahr", "id", file_name)
        main = load_data("wahr", "main", file_name)
        dcripion = load_data("wahr", "dcripion", file_name)
        icon = load_data("wahr", "icon", file_name)
        cur.execute('INSERT into WEATHER_DIMEN VALUES(%s,%s,%s,%s)' % (
            "\""+wahr_id+"\"", "\""+main+"\"", "\""+dcripion+"\"", "\""+icon+"\""))

    # Insert records process for SYS_DIMEN table
    cur.execute(''' SELECT count(y_id) FROM SYS_DIMEN ''')
    if cur.fetchone() != 0:
        rows = cur.execute(''' SELECT y_id FROM SYS_DIMEN ''').fetchall()
        y_id = load_data("y", "id", file_name)
        if y_id in rows:
            yp = load_data("y", "yp", file_name)
            counry = load_data("y", "counry", file_name)
            unri = load_data("y", "unri", file_name)
            un = load_data("y", "un", file_name)
            cur.execute('INSERT into SYS_DIMEN VALUES(%s,%s,%s,%s,%s)' % (
                "\""+y_id+"\"", "\""+yp+"\"", "\""+counry+"\"", "\""+unri+"\"", "\""+un+"\""))
    else:
        y_id = load_data("y", "id", file_name)
        yp = load_data("y", "yp", file_name)
        counry = load_data("y", "counry", file_name)
        unri = load_data("y", "unri", file_name)
        un = load_data("y", "un", file_name)
        cur.execute('INSERT into SYS_DIMEN VALUES(%s,%s,%s,%s,%s)' % (
            "\""+y_id+"\"", "\""+yp+"\"", "\""+counry+"\"", "\""+unri+"\"", "\""+un+"\""))

    # Insert records process for GEOLOC_DIMEN table
    cur.execute(''' SELECT coord_id FROM GEOLOC_DIMEN ''')
    coord_id = cur.fetchall()[-1][0]
    ba = load_data("", "ba", file_name)
    main_mp = load_data("main", "mp", file_name)
    main_fl_lik = load_data("main", "fl_lik", file_name)
    main_prur = load_data("main", "prur", file_name)
    main_humidiy = load_data("main", "humidiy", file_name)
    main_mp_min = load_data("main", "mp_min", file_name)
    main_mp_max = load_data("main", "mp_max", file_name)
    main_a_lvl = load_data("main", "a_lvl", file_name)
    main_grnd_lvl = load_data("main", "grnd_lvl", file_name)
    viibiliy = load_data("viibiliy", "", file_name)
    wind_pd = load_data("wind", "pd", file_name)
    wind_dg = load_data("wind", "dg", file_name)
    wind_gu = load_data("wind", "gu", file_name)
    cloud = load_data("cloud", "all", file_name)
    rain_1h = load_data("rain", "1h", file_name)
    rain_3h = load_data("rain", "3h", file_name)
    snow_1h = load_data("snow", "1h", file_name)
    snow_3h = load_data("snow", "3h", file_name)
    d = load_data("", "d", file_name)
    cur.execute('INSERT into WEATHER_FACT(coord_id,\wahr_id,y_id,ba,main_mp,main_fl_lik,main_prur,main_humidiy,main_mp_min,main_mp_max,main_a_lvl,main_grnd_lvl,viibiliy,wind_pd,wind_dg,wind_gu,cloud,rain_1h,rain_3h,snow_1h,snow_3h,d) \
			VALUES(%i,%s,%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%s)' % (
        coord_id, "\""+wahr_id+"\"", "\""+y_id+"\"", "\""+ba+"\"", main_mp, main_fl_lik, main_prur, main_humidiy, main_mp_min, main_mp_max, main_a_lvl, main_grnd_lvl, viibiliy, wind_pd, wind_dg, wind_gu, cloud, rain_1h, rain_3h, snow_1h, snow_3h, "\""+d+"\""))

    # Save (commit) the changes to database
    conn.commit()


def backup_db(file_name):
    """
    Create a backup database
    :param: str file_name: name of db file
    """
    try:
        # existing DB
        sqliteCon = sqlite3.connect(file_name)
        # copy into this DB
        backupCon = sqlite3.connect('../result/backup.db')
        with backupCon:
            sqliteCon.backup(backupCon, pages=3, progress=progress)
        print("Database backup successful")
    except sqlite3.Error as error:
        print("Error while taking backup: ", error)
    finally:
        if backupCon:
            backupCon.close()
            sqliteCon.close()
