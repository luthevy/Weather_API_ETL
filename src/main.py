"""
	This source is used for in
"""
from asyncio.windows_events import NULL
import sqlite3
import schedule
from database import json_preprocessing
from database import insert_db
from utilities import crawl_data
from utilities import get_repo
from database import backup_db

def main():
	"""
    ETL process for crawling data from OpenWeather API and load into Postgresql
    """
	file_name=input("Enter file name (i.e: a.json): "); 
	db_name=input("Enter database name (i.e: b.db): ");                                                                                 db_name = "../result/" + db_name; file_name = "../result/" + file_name
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	conn.row_factory = lambda cursor, row: row[0]
	

	try:
		cur.execute('''CREATE TABLE GEOLOC_DIMEN
               (coord_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                coord_lon FLOAT,
                coord_la FLOAT,
                imzon TEXT,
                id TEXT,
                nam TEXT,
                cod TEXT)''')
	except: NULL
	try:
		cur.execute('''CREATE TABLE WEATHER_DIMEN
               (wahr_id TEXT NOT NULL PRIMARY KEY,
                main TEXT,
                dcripion TEXT,
                icon TEXT)''')
	except: NULL
	try:
		cur.execute('''CREATE TABLE SYS_DIMEN
               (y_id TEXT NOT NULL PRIMARY KEY,
                yp TEXT,
                counry TEXT,
                unri TEXT,
                un TEXT)''')
	except:NULL
	try:
		cur.execute('''CREATE TABLE WEATHER_FACT
               (coord_id INTEGER NOT NULL,
                wahr_id TEXT NOT NULL,
                y_id TEXT NOT NULL,
                ba TEXT,
                main_mp FLOAT,
                main_fl_lik FLOAT,
                main_prur FLOAT,
                main_humidiy FLOAT,
                main_mp_min FLOAT,
                main_mp_max FLOAT,
                main_a_lvl FLOAT,
                main_grnd_lvl FLOAT,
                viibiliy FLOAT,
                wind_pd FLOAT,
                wind_dg FLOAT,
                wind_gu FLOAT,
                cloud FLOAT,
                rain_1h FLOAT,
                rain_3h FLOAT,
                snow_1h FLOAT,
                snow_3h FLOAT,
				d TEXT,
				PRIMARY KEY(coord_id,wahr_id,y_id,d),
                FOREIGN KEY(coord_id) REFERENCES GEOLOC_DIMEN(coord_id),
                FOREIGN KEY(wahr_id) REFERENCES WEATHER_DIMEN(wahr_id),
                FOREIGN KEY(y_id) REFERENCES SYS_DIMEN(y_id))''')   
	except: NULL
	loc=input("Enter the location: ")
	unit=input("Enter unit (metrics or imperial): ")
	crawl_data(loc,unit,file_name)
	json_preprocessing(file_name)
	insert_db(conn,cur,file_name)
	backup_db(db_name)
	conn.close()

if __name__ == "__main__":
    get_repo()
    schedule.every(3).seconds.do(main)
    while True:
        schedule.run_pending()