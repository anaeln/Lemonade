import sqlite3
import pandas as pd
from consts import (DB_NAME, CREATE_VEHICLES_STATUS, INSERT_VEHICLES_STATUS, CREATE_VEHICLES_EVENTS,
                    INSERT_VEHICLES_EVENTS, CREATE_DAILY_SUMMARIZED)


class SQLiteHandler(object):
    def __init__(self):
        self.db = DB_NAME
        self.conn = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db)
            self.cur = self.conn.cursor()
        except Exception as e:
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def create_tables_and_views(self):
        try:
            with self.conn:
                self.cur.execute(CREATE_VEHICLES_STATUS)
                self.cur.execute(CREATE_VEHICLES_EVENTS)
                self.cur.execute(CREATE_DAILY_SUMMARIZED)
        except Exception as e:
            raise e

    def insert_to_db(self, table_name, records_lst):
        try:
            with self.conn:
                if table_name == 'vehicle_status':
                    self.cur.executemany(INSERT_VEHICLES_STATUS, records_lst)
                elif table_name == 'vehicles_events':
                    self.cur.executemany(INSERT_VEHICLES_EVENTS, records_lst)
                self.conn.commit()
                print("INFO: Successfully inserted to database")
        except Exception as e:
            raise e

    def export_select_to_csv(self, select_query, csv_name):
        try:
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(select_query)
                query = pd.read_sql(select_query, self.conn)
                query.to_csv(csv_name, index=False)
                print("CSV file with query output was created")
        except Exception as e:
            raise e
