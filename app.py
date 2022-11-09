import os
import shutil
import time
import json
from consts import DIRECTORY_PATH, ARCHIVE_PATH, SELECT_DAILY_VIEWS
from sqlite_handler import SQLiteHandler

sql_conn = SQLiteHandler()
with sql_conn:
    sql_conn.create_tables_and_views()


def get_json_data(records):
    vehicles_recs = []
    table_name = list(records.keys())[0]
    values = list(records.values())[0]
    for obj in values:
        vehicles_recs.append([str(obj) for obj in obj.values()])
    return table_name, vehicles_recs


def main():
    before = []
    while True:
        time.sleep(1)
        after = [dir for dir in os.listdir(DIRECTORY_PATH)]
        jsons = [dir for dir in after if not dir in before]
        if jsons:
            print("INFO: " + str(len(jsons)) + " JSONS detected ")
            data_to_insert = []
            for json_file in jsons:
                with open(os.path.join(DIRECTORY_PATH, json_file)) as f:
                    data = json.load(f)
                table_name, records = get_json_data(data)
                data_to_insert.append((table_name, records))

            with sql_conn:
                print("INFO: Connection to db established successfully")
                for data in data_to_insert:
                    sql_conn.insert_to_db(data[0], data[1])
                sql_conn.export_select_to_csv(SELECT_DAILY_VIEWS, 'daily_summarized.csv')

            for file in jsons:
                src_path = os.path.join(DIRECTORY_PATH, file)
                dst_path = os.path.join(ARCHIVE_PATH, file)
                shutil.move(src_path, dst_path)
            print("INFO: " + str(len(jsons)) + " JSONS moved to archive ")
        before = after


if __name__ == '__main__':
    main()
