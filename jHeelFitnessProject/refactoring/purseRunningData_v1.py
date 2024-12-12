# this file is used to parse the fit file and store the dev_data in the database
""" stelios (c) steliosmacrico "jHeel 2024 creating plugin"""

import sqlite3
import os
import logging
import datetime
from fitparse import FitFile

# Set up logging
now = datetime.datetime.now()
timestamp = now.strftime('%Y%m%d_%H%M%S')
logging.basicConfig(filename=f'c:/SteliosDev/jHeel_Dev/gProjects/Artemis/Plugins/Logs/jheel_parse_DEV{timestamp}.log', 
                   level=logging.INFO)

# Set up logging with debug level
logging.basicConfig(
    filename=f'c:/SteliosDev/jHeel_Dev/gProjects/Artemis/Plugins/Logs/jheel_parse_DEV{timestamp}.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def print_all_fields(fit_file_path):
    """Helper function to print all available fields in a FIT file"""
    fit_file = FitFile(fit_file_path)
    print("Available fields in FIT file:")
    for msg in fit_file.messages:
        if msg.name in ['session', 'record']:
            print(f"\nMessage type: {msg.name}")
            for field in msg.fields:
                print(f"Field name: {field.name}, Value: {field.value}")

logging.info('Starting script...')
print('Starting script...')

def create_table_if_not_exists():
    conn = sqlite3.connect(r'c:/steliosdev/jheel_dev/dev_learn/dbs/artemis.db')
    cursor = conn.cursor()

    # Drop and create ArtemistblV33_dev
    cursor.execute('DROP TABLE IF EXISTS ArtemistblV33_dev')
    logging.info('ArtemistblV33_dev table dropped successfully.')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ArtemistblV33_dev (
            activity_id INT PRIMARY KEY,
            timestamp TEXT,
            distance REAL,
            hrv INT,
            fat INT,
            total_fat INT,  
            carbs INT,
            total_carbs INT,
            VO2maxSmooth INT,
            VO2maxSession INT,
            CardiacDrift INT,    
            CooperTest INT,
            steps INT,     
            field110 TXT,
            stress_hrpa INT,
            HR_RS_Deviation_Index INT,
            hrv_sdrr_f INT,
            hrv_pnn50 INT,                          
            hrv_pnn20 INT,
            rmssd INT,
            lnrmssd INT,
            sdnn INT,
            sdsd INT,
            nn50 INT,
            nn20 INT,
            pnn20 INT,
            Long  INT,
            Short INT,
            Ectopic_S INT,
            hrv_rmssd INT,
            SD2 INT,
            SD1 INT,
            LF INT,
            HF INT,
            VLF INT,
            pNN50 INT, 
            LFnu INT, 
            HFnu INT,
            MeanHR INT, 
            MeanRR INT
        )
    ''')
    
    # Create hrv_records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hrv_records (
            activity_id TEXT,
            record INTEGER,
            timestamp DATETIME,
            hrv_s INTEGER,
            hrv_btb INTEGER,
            hrv_hr INTEGER,
            PRIMARY KEY (activity_id, record),
            FOREIGN KEY (activity_id) REFERENCES activities(activity_id)
        )
    ''')

    # Create hrv_sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hrv_sessions (
            activity_id TEXT PRIMARY KEY,
            timestamp DATETIME,
            min_hr INTEGER,
            hrv_rmssd INTEGER,
            hrv_sdrr_f INTEGER,
            hrv_sdrr_l INTEGER,
            hrv_pnn50 INTEGER,
            hrv_pnn20 INTEGER,
            FOREIGN KEY (activity_id) REFERENCES activities(activity_id)
        )
    ''')
    
    logging.info('All tables created successfully.')
    conn.commit()
    conn.close()

def create_view_if_not_exists():
    conn = sqlite3.connect('c:/steliosdev/jheel_dev/dev_learn/dbs/artemis.db')
    cursor = conn.cursor()

    # Create view for HRV activities
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS hrv_activities_view AS
        SELECT 
            a.activity_id,
            a.name,
            a.description,
            a.start_time,
            a.stop_time,
            a.elapsed_time,
            h.min_hr,
            h.hrv_rmssd,
            h.hrv_sdrr_f,
            h.hrv_sdrr_l,
            h.hrv_pnn50,
            h.hrv_pnn20
        FROM activities a
        JOIN hrv_sessions h ON a.activity_id = h.activity_id
        ORDER BY a.start_time DESC
    ''')

    conn.commit()
    conn.close()
    logging.info('Views created successfully.')

def parse_fit_file(file_path, activity_id):
    fit_file = FitFile(file_path)
    messages = fit_file.messages
    session_data = []
    hrv_records = []
    hrv_sessions = []

    for msg in messages:
        if msg.name == 'session':
            fields = msg.fields
            field_dict = {field.name: field.value for field in fields}
            
            # Create session data with proper field name handling and default None values
            session = {
                'activity_id': activity_id,
                'timestamp': field_dict.get('timestamp', None),
                'distance': field_dict.get('total_distance', None),
                'hrv': field_dict.get('dev_hrv', None),  # Changed from 'HRV' to 'dev_hrv'
                'fat': field_dict.get('dev_fat', None),  # Changed from 'Fat' to 'dev_fat'
                'Total Fat': field_dict.get('dev_total_fat', None),
                'Carbs': field_dict.get('dev_carbs', None),
                'Total Carbs': field_dict.get('dev_total_carbs', None),
                'VO2maxSmooth': field_dict.get('dev_vo2max_smooth', None),
                'VO2maxSession': field_dict.get('dev_vo2max_session', None),
                'CardiacDrift': field_dict.get('dev_cardiac_drift', None),
                'CooperTest': field_dict.get('dev_cooper_test', None),
                'Steps': field_dict.get('total_steps', None),  # Changed to match common FIT field name
                'field110': field_dict.get('dev_field110', None),
                'stress_hrpa': field_dict.get('dev_stress_hrpa', None),
                'HR-RS_Deviation Index': field_dict.get('dev_hr_rs_deviation_index', None),
                'hrv_sdrr_f': field_dict.get('dev_hrv_sdrr_f', None),
                'hrv_pnn50': field_dict.get('dev_hrv_pnn50', None),
                'hrv_pnn20': field_dict.get('dev_hrv_pnn20', None),
                'RMSSD': field_dict.get('dev_rmssd', None),
                'lnRMSSD': field_dict.get('dev_ln_rmssd', None),
                'SDNN': field_dict.get('dev_sdnn', None),
                'SDSD': field_dict.get('dev_sdsd', None),
                'NN50': field_dict.get('dev_nn50', None),
                'NN20': field_dict.get('dev_nn20', None),
                'pnn20': field_dict.get('dev_pnn20', None),
                'Long': field_dict.get('dev_long', None),
                'Short': field_dict.get('dev_short', None),
                'Ectopic_S': field_dict.get('dev_ectopic_s', None),
                'hrv_rmssd': field_dict.get('dev_hrv_rmssd', None),
                'SD2': field_dict.get('dev_sd2', None),
                'SD1': field_dict.get('dev_sd1', None),
                'LF': field_dict.get('dev_lf', None),
                'HF': field_dict.get('dev_hf', None),
                'VLF': field_dict.get('dev_vlf', None),
                'pNN50': field_dict.get('dev_pnn50', None),
                'LFnu': field_dict.get('dev_lfnu', None),
                'HFnu': field_dict.get('dev_hfnu', None),
                'MeanHR': field_dict.get('dev_mean_hr', None),
                'MeanRR': field_dict.get('dev_mean_rr', None)
            }

            # Log available fields for debugging
            logging.debug(f"Available fields in session message: {list(field_dict.keys())}")
            
            session_data.append(session)

            # Create HRV session data
            hrv_session = {
                'activity_id': activity_id,
                'timestamp': field_dict.get('timestamp', None),
                'min_hr': field_dict.get('dev_min_hr', None),
                'hrv_rmssd': field_dict.get('dev_hrv_rmssd', None),
                'hrv_sdrr_f': field_dict.get('dev_hrv_sdrr_f', None),
                'hrv_sdrr_l': field_dict.get('dev_hrv_sdrr_l', None),
                'hrv_pnn50': field_dict.get('dev_hrv_pnn50', None),
                'hrv_pnn20': field_dict.get('dev_hrv_pnn20', None)
            }
            hrv_sessions.append(hrv_session)

        elif msg.name == 'record':
            fields = msg.fields
            field_dict = {field.name: field.value for field in fields}
            
            # Log available fields for debugging
            logging.debug(f"Available fields in record message: {list(field_dict.keys())}")
            
            hrv_record = {
                'activity_id': activity_id,
                'record': len(hrv_records) + 1,
                'timestamp': field_dict.get('timestamp', None),
                'hrv_s': field_dict.get('dev_hrv_s', None),
                'hrv_btb': field_dict.get('dev_hrv_btb', None),
                'hrv_hr': field_dict.get('dev_hrv_hr', None)
            }
            hrv_records.append(hrv_record)

    # Add debug logging for the first session
    if session_data:
        logging.debug(f"First session data: {session_data[0]}")

    logging.info(f'Parsed session data for activity ID {activity_id}.')
    
    
    # At the end of parse_fit_file:
    if session_data or hrv_records or hrv_sessions:
        logging.info(f'Parsed data for activity ID {activity_id}: '
                    f'{len(session_data)} sessions, '
                    f'{len(hrv_records)} records, '
                    f'{len(hrv_sessions)} HRV sessions')
    else:
        logging.warning(f'No data parsed for activity ID {activity_id}')

    return session_data, hrv_records, hrv_sessions



def insert_data_into_db(data, hrv_records, hrv_sessions):
    conn = sqlite3.connect('c:/steliosdev/jheel_dev/dev_learn/dbs/artemis.db')
    cursor = conn.cursor()

    try:
        # Specify the fields you care about for jHeel component
        specific_fields = ['fat','Total Fat','Carbs','Total Carbs',
                        'VO2maxSmooth',
                        'VO2maxSession',
                        'CardiacDrift',
                        'CooperTest',
                        'Steps',
                        'field110',
                        'stress_hrpa',
                        'HR-RS_Deviation Index',
                        'hrv_sdrr_f',
                        'hrv_pnn50',
                        'hrv_pnn20',
                        'RMSSD',
                        'lnRMSSD',
                        'SDNN',
                        'SDSD',
                        'NN50',
                        'NN20',
                        'pnn20',
                        'Long',
                        'Short', 
                        'Ectopic_S',
                        'hrv_rmssd',
                        'SD2',
                        'SD1',
                        'LF',
                        'HF',
                        'VLF',
                        'pNN50',
                        'LFnu',
                        'HFnu',
                        'MeanHR', 
                        'MeanRR']

        # Insert jHeel session data
        for session in data:
            # Check if all specific fields in the session dictionary are None
            if all(session.get(field) is None for field in specific_fields):
                # If they are, skip this iteration
                continue

            cursor.execute('''
                INSERT OR REPLACE INTO ArtemistblV33_dev (
                    activity_id, distance, hrv, fat, total_fat, carbs, total_carbs,  
                    VO2maxSmooth, steps, field110, stress_hrpa, HR_RS_Deviation_Index,
                    hrv_sdrr_f, hrv_pnn50, hrv_pnn20, rmssd, lnrmssd, sdnn, sdsd, 
                    nn50, nn20, pnn20, Long, Short, Ectopic_S, hrv_rmssd, 
                    VO2maxSession, CardiacDrift, CooperTest, SD2, SD1, HF, LF, VLF, 
                    pNN50, LFnu, HFnu, MeanHR, MeanRR
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session['activity_id'], 
                session['distance'], 
                session['hrv'], 
                session['fat'], 
                session['Total Fat'],
                session['Carbs'], 
                session['Total Carbs'],
                session['VO2maxSmooth'], 
                session['Steps'], 
                session['field110'], 
                session['stress_hrpa'], 
                session['HR-RS_Deviation Index'],
                session['hrv_sdrr_f'], 
                session['hrv_pnn50'], 
                session['hrv_pnn20'], 
                session['RMSSD'], 
                session['lnRMSSD'], 
                session['SDNN'], 
                session['SDSD'], 
                session['NN50'], 
                session['NN20'], 
                session['pnn20'], 
                session['Long'], 
                session['Short'], 
                session['Ectopic_S'], 
                session['hrv_rmssd'], 
                session['VO2maxSession'],
                session['CardiacDrift'], 
                session['CooperTest'], 
                session['SD2'], 
                session['SD1'], 
                session['HF'], 
                session['LF'], 
                session['VLF'], 
                session['pNN50'], 
                session['LFnu'], 
                session['HFnu'],
                session['MeanHR'], 
                session['MeanRR']
            ))

        # Insert HRV records
        if hrv_records:  # Check if there are any records
            for record in hrv_records:
                cursor.execute('''
                    INSERT OR REPLACE INTO hrv_records 
                    (activity_id, record, timestamp, hrv_s, hrv_btb, hrv_hr)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    record['activity_id'], 
                    record['record'], 
                    record['timestamp'],
                    record['hrv_s'], 
                    record['hrv_btb'], 
                    record['hrv_hr']
                ))

        # Insert HRV sessions
        if hrv_sessions:  # Check if there are any sessions
            for session in hrv_sessions:
                if isinstance(session, dict) and all(key in session for key in ['activity_id', 'timestamp', 'min_hr', 'hrv_rmssd', 'hrv_sdrr_f', 'hrv_sdrr_l', 'hrv_pnn50', 'hrv_pnn20']):
                    cursor.execute('''
                        INSERT OR REPLACE INTO hrv_sessions 
                        (activity_id, timestamp, min_hr, hrv_rmssd, hrv_sdrr_f, 
                        hrv_sdrr_l, hrv_pnn50, hrv_pnn20)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        session['activity_id'], 
                        session['timestamp'],
                        session['min_hr'], 
                        session['hrv_rmssd'],
                        session['hrv_sdrr_f'], 
                        session['hrv_sdrr_l'],
                        session['hrv_pnn50'], 
                        session['hrv_pnn20']
                    ))
                else:
                    logging.warning(f"Skipping invalid HRV session data: {session}")

        conn.commit()
        logging.info('Data insertion completed successfully.')

    except Exception as e:
        logging.error(f"Error during data insertion: {str(e)}")
        conn.rollback()
        raise

    finally:
        conn.close()
    
def parse_all_fit_files_in_folder(folder_path):
    all_session_data = []
    all_hrv_records = []
    all_hrv_sessions = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.fit'):
            try:
                fit_file_path = os.path.join(folder_path, filename)
                activity_id = os.path.splitext(filename)[0].split('_')[0]
                
                session_data, hrv_records, hrv_session = parse_fit_file(
                    fit_file_path, activity_id)
                
                all_session_data.extend(session_data)
                all_hrv_records.extend(hrv_records)
                if hrv_session:
                    all_hrv_sessions.append(hrv_session)
                    
            except Exception as e:
                logging.error(f'Error parsing file {filename}: {e}')
                print(f'Error parsing file {filename}: {e}')
                continue
    
    logging.info('All files parsed successfully.')
    print('All files parsed successfully.')
    
    return all_session_data, all_hrv_records, all_hrv_sessions

if __name__ == "__main__":
    try:
        create_table_if_not_exists()
        create_view_if_not_exists()
        
        folder_path = 'c:/users/stma/healthdata/fitfiles/activitiesTEST'
        logging.info(f"Processing files from folder: {folder_path}")
        
        all_session_data, all_hrv_records, all_hrv_sessions = parse_all_fit_files_in_folder(folder_path)
        
        logging.info(f"Parsed data summary:")
        logging.info(f"Sessions: {len(all_session_data)}")
        logging.info(f"HRV Records: {len(all_hrv_records)}")
        logging.info(f"HRV Sessions: {len(all_hrv_sessions)}")
        
        insert_data_into_db(all_session_data, all_hrv_records, all_hrv_sessions)
        
        # Verify the database contents after insertion
        verify_database_contents()
        
        logging.info('Script completed successfully.')
        print('Script completed successfully.')
        
    except Exception as e:
        logging.error(f"Script failed with error: {str(e)}")
        print(f"Script failed with error: {str(e)}")