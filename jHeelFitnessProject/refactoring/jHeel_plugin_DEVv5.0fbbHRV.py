# this file is used to parse the fit file and store the dev_data in the database
""" stelios (c) steliosmacrico "jHeel 2024 creating plugin - integrate fbb_HRV
"""" revision (c) November 2019 - save data to PostgresSQL"
""" purpose of this is to make a more simple plugin to manage hrvData"""
import psycopg2
import os
import logging
import datetime
import fitparse
from fitparse import FitFile

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="garminDB_v2",
        user="postgres",
        password="Penivalia2627"
    )

def create_tables_in_postgres():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Drop existing tables if they exist
    cursor.execute('DROP TABLE IF EXISTS hrv_recordsDEV')
    cursor.execute('DROP TABLE IF EXISTS hrv_sessionsDEV')
    cursor.execute('DROP TABLE IF EXISTS ArtemistblV41dev')

    # Create hrv_records table
    cursor.execute('''
        CREATE TABLE hrv_recordsDEV (
            activity_id TEXT,
            record INTEGER,
            timestamp TEXT,
            hrv_s INTEGER,
            hrv_btb INTEGER,
            hrv_hr INTEGER,
            rrhr INTEGER,
            rawHR INTEGER,
            RRint INTEGER,
            hrv INTEGER,
            rmssd TEXT,
            sdnn INTEGER,
            SaO2_C INTEGER,
            PRIMARY KEY (activity_id, record)
        )
    ''')

    # Create hrv_sessions table
    cursor.execute('''
        CREATE TABLE hrv_sessionsDEV (
            activity_id TEXT PRIMARY KEY,
            timestamp TEXT,
            min_hr INTEGER,
            hrv_rmssd INTEGER,
            hrv_sdrr_f INTEGER,
            hrv_sdrr_l INTEGER,
            hrv_pnn50 INTEGER,
            hrv_pnn20 INTEGER,
            session_hrv INTEGER,
            NN50 INTEGER,
            NN20 INTEGER,
            armssd INTEGER,
            asdnn INTEGER,
            SaO2 INTEGER,
            trnd_hrv INTEGER,
            recovery INTEGER
        )
    ''')

    # Create main ArtemistblV41dev table
    cursor.execute('''
        CREATE TABLE ArtemistblV41dev (
            activity_id TEXT PRIMARY KEY,
            timestamp TEXT,
            distance REAL,
            hrv INTEGER,
            fat INTEGER,
            total_fat INTEGER,  
            carbs INTEGER,
            total_carbs INTEGER,
            VO2maxSmooth INTEGER,
            VO2maxSession INTEGER,
            CardiacDrift INTEGER,    
            CooperTest INTEGER,
            steps INTEGER,     
            field110 TEXT,
            stress_hrpa INTEGER,
            HR_RS_Deviation_Index INTEGER,
            hrv_sdrr_f INTEGER,
            hrv_pnn50 INTEGER,                          
            hrv_pnn20 INTEGER,
            rmssd INTEGER,
            lnrmssd INTEGER,
            sdnn INTEGER,
            sdsd INTEGER,
            nn50 INTEGER,
            nn20 INTEGER,
            pnn20 INTEGER,
            Long INTEGER,
            Short INTEGER,
            Ectopic_S INTEGER,
            hrv_rmssd INTEGER,
            SD2 INTEGER,
            SD1 INTEGER,
            LF INTEGER,
            HF INTEGER,
            VLF INTEGER,
            pNN50 INTEGER, 
            LFnu INTEGER, 
            HFnu INTEGER,
            MeanHR INTEGER, 
            MeanRR INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()
    logging.info('PostgreSQL tables created successfully.')
    
    
    
    # Parse all .fit files in the specified folder (folder_path)
from fitparse import FitFile

def parse_all_fit_files_in_folder(folder_path):
    
       
    all_session_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.fit'):
            try:
                fit_file_path = os.path.join(folder_path, filename)
                activity_id = os.path.splitext(filename)[0]  # Get filename without extension
                activity_id = activity_id.split('_')[0]  # Get everything before '_' character
                session_data = parse_fit_file(fit_file_path, activity_id)
                all_session_data.extend(session_data)
            except Exception as e:
                logging.error(f'Error parsing file {filename}: {e}')
                print(f'Error parsing file {filename}: {e}')
                continue
            
            logging.info('All files parsed successfully.')  
            print('All files parsed successfully.')
            
    return all_session_data



def insert_session_data_into_postgres(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    specific_fields = ['fat','Total Fat','Carbs','Total Carbs',
                    'VO2maxSmooth', 'VO2maxSession', 'CardiacDrift',
                    'CooperTest', 'Steps', 'field110', 'stress_hrpa',
                    'HR-RS_Deviation Index', 'hrv_sdrr_f', 'hrv_pnn50',
                    'hrv_pnn20', 'RMSSD', 'lnRMSSD', 'SDNN', 'SDSD',
                    'NN50', 'NN20', 'pnn20', 'Long', 'Short', 
                    'Ectopic_S', 'hrv_rmssd', 'SD2', 'SD1', 'LF',
                    'HF', 'VLF', 'pNN50', 'LFnu', 'HFnu', 
                    'MeanHR', 'MeanRR']

    for session in data:
        # Skip sessions with all specific fields as None
        if all(session[field] is None for field in specific_fields):
            continue

        # Insert or replace record
        cursor.execute('''
            INSERT INTO ArtemistblV41dev (
                activity_id, distance, hrv, fat, total_fat, carbs, total_carbs,  
                VO2maxSmooth, steps, field110, stress_hrpa, HR_RS_Deviation_Index,
                hrv_sdrr_f, hrv_pnn50, hrv_pnn20, rmssd, lnrmssd, sdnn, sdsd, 
                nn50, nn20, pnn20, Long, Short, Ectopic_S, hrv_rmssd, 
                VO2maxSession, CardiacDrift, CooperTest, SD2, SD1, HF, LF, VLF, 
                pNN50, LFnu, HFnu, MeanRR, MeanHR
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        ''', (
            session['activity_id'], session['distance'], session['hrv'], 
            session['fat'], session['Total Fat'], session['Carbs'], 
            session['Total Carbs'], session['VO2maxSmooth'], session['Steps'], 
            session['field110'], session['stress_hrpa'], 
            session['HR-RS_Deviation Index'], session['hrv_sdrr_f'], 
            session['hrv_pnn50'], session['hrv_pnn20'], session['RMSSD'], 
            session['lnRMSSD'], session['SDNN'], session['SDSD'], 
            session['NN50'], session['NN20'], session['pnn20'], 
            session['Long'], session['Short'], session['Ectopic_S'], 
            session['hrv_rmssd'], session['VO2maxSession'], 
            session['CardiacDrift'], session['CooperTest'], session['SD2'], 
            session['SD1'], session['HF'], session['LF'], session['VLF'], 
            session['pNN50'], session['LFnu'], session['HFnu'], 
            session['MeanRR'], session['MeanHR']
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Set up logging
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d_%H%M%S')
    logging.basicConfig(filename=f'postgres_import_{timestamp}.log', level=logging.INFO)

    try:
        # Create tables in PostgreSQL
        create_tables_in_postgres()

        # Parse and insert data
        all_session_data = parse_all_fit_files_in_folder('c:/users/stma/healthdata/fitfiles/activitiesTEST')
        insert_session_data_into_postgres(all_session_data)
        
        logging.info('All data inserted successfully.')
        print('All data inserted successfully (c)smacrico')
    except Exception as e:
        logging.error(f'Error processing data: {e}')
        print(f'Error processing data: {e}')