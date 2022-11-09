DIRECTORY_PATH = r'C:\Users\hanae\Documents\Lemonade'
ARCHIVE_PATH = r'C:\Users\hanae\Documents\Lemonade_archive'


DB_NAME = 'lemonade.db'

CREATE_VEHICLES_EVENTS = """CREATE TABLE IF NOT EXISTS vehicles_events(
                    VEHICLE_ID TEXT,
                    EVENT_TIME TEXT,
                    EVENT_SOURCE TEXT,
                    EVENT_TYPE TEXT,
                    EVENT_VALUE TEXT,
                    EVENT_EXTRA_DATA TEXT
               )"""

CREATE_VEHICLES_STATUS = """CREATE TABLE IF NOT EXISTS vehicle_status(
                    VEHICLE_ID TEXT,
                    REPORT_TIME TEXT,
                    STATUS_SOURCE TEXT,
                    STATUS TEXT
               )"""

CREATE_DAILY_SUMMARIZED = """CREATE VIEW IF NOT EXISTS daily_summarized as
                                select 
                                    VEHICLE_ID,
                                       case cast (strftime('%w', EVENT_TIME) as integer)
                                           when 0 then 'Sunday'
                                           when 1 then 'Monday'
                                           when 2 then 'Tuesday'
                                           when 3 then 'Wednesday'
                                           when 4 then 'Thursday'
                                           when 5 then 'Friday'
                                           else 'Saturday'
                                        end as DAY,
                                    max(EVENT_TIME) as LAST_EVENT_TIME, 
                                    EVENT_TYPE as LAST_EVENT_TYPE 
                                from 
                                    vehicles_events
                                group by 
                                    VEHICLE_ID"""

INSERT_VEHICLES_EVENTS = """INSERT INTO vehicles_events(
                    VEHICLE_ID,
                    EVENT_TIME, 
                    EVENT_SOURCE, 
                    EVENT_TYPE, 
                    EVENT_VALUE, 
                    EVENT_EXTRA_DATA 
               )
               VALUES (
                    ?,?,?,?,?,?
               );
               """

INSERT_VEHICLES_STATUS = """INSERT INTO vehicle_status(
                    VEHICLE_ID,
                    REPORT_TIME,
                    STATUS_SOURCE,
                    STATUS
               )
               VALUES (
                    ?,?,?,?
               );
               """

SELECT_DAILY_VIEWS = """SELECT * FROM DAILY_SUMMARIZED;"""