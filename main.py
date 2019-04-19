from normalizer import DataNormalizer
import os
import sys
import logging
import datetime
from shutil import copyfile
from pathlib import Path
from dates_reader import DatesReader
from eeg_writer import EEGCSV
from emotions_writer import FEACSV
# from notes_writer import NotesCSV
# from notes_normalizer import NormalizeNotes

"""
    This is the Main Script to Start Data Normalization Process
    Process: 
    1.	Read Command Line Arguments
    2.	Setup Logging
    3.	Setup raw/ and final/ folder paths
    4.	Create new directory final/    

    5.	If Video file exists:
                Copy Video file to final/
            else:
                log alert

    6.	If EEG file exists:
            Normalize EEG
        else:
            Create New EEG

    7.	If Facial file exists:
            Normalize Facial
        else:
            Create New Facial

    8.	If Notes file exists:
            Normalize Notes
        else:
            Create New Notes

    Usage: `python main.py UserName_DateTime`
"""

# Read Commandline Arguments
fullCmdArguments = sys.argv
# Skip first Argument i.e. `program_name.py`
argumentList = fullCmdArguments[1:]
# Read Further Arguments
incoming_variable = argumentList[0]

# Define Folder Paths for Read - Write Operations
logging.basicConfig(filename='logs/' + incoming_variable + '.log', level=logging.DEBUG)
raw_data_folder_path = '../../Reports/' + incoming_variable + '/raw/'
final_folder_path = '../../Reports/' + incoming_variable + '/final/'
logging.info('Raw Folder Path:\t' + raw_data_folder_path)
logging.info('Final Folder Path:\t' + final_folder_path)

try:
    # Make a New Directory to Store final Data files i.e. `final/`
    if not os.path.exists(final_folder_path):
        os.mkdir(final_folder_path)
        print('Directory ', final_folder_path, ' Created ')
        logging.info('Directory ' + str(final_folder_path) + ' Created ')
    else:
        print('Directory ', final_folder_path, ' already exists')
        logging.info('Directory ' + str(final_folder_path) + ' already exists ')

    # Copy Raw Video File from Src to Destination
    video_file = Path(raw_data_folder_path + incoming_variable + '_Video.mp4')
    if video_file.is_file():
        # file exists
        copyfile(raw_data_folder_path + incoming_variable + '_Video.mp4',
                 final_folder_path + incoming_variable + '_Video.mp4')
        logging.info('Copying Video file from:\t' + raw_data_folder_path + incoming_variable + '_Video.mp4' +
                     '\nto' + final_folder_path + incoming_variable + '_Video.mp4')
    else:
        print(raw_data_folder_path + incoming_variable + '_Video.mp4 does not exists!')
        logging.info(raw_data_folder_path + incoming_variable + '_Video.mp4 does not exists!')

    # Read End and Start Date from `Reports.csv` file
    d = DatesReader('DateReader', incoming_variable)
    dates = d.read_dates()
    start_date = datetime.datetime.strptime(dates[0], '%Y-%m-%d %H:%M:%S')
    end_date = datetime.datetime.strptime(dates[1], '%Y-%m-%d %H:%M:%S')
    diff = end_date - start_date
    print('Difference between two dates is:\t' + str(diff))

    # Normalize EEG Data file
    eeg_file = Path(raw_data_folder_path + incoming_variable + '_EEG.csv')
    if eeg_file.is_file():
        # file exists. Normalize EEG
        # Initialize object of class DataNormalizer() to normalize raw data
        logging.info('Starting EEG data normalization')
        e = DataNormalizer(
            'EEG',
            incoming_variable + '_EEG',
            raw_data_folder_path,
            final_folder_path,
            dates[0],
            dates[1])
        e.start()
        e.count_total_rows()
        e.normalize_data()
        logging.info('End of EEG data normalization')
    else:
        # file does not exist. Create new EEG file
        print(raw_data_folder_path + incoming_variable + '_EEG.csv does not exists!')
        logging.info(raw_data_folder_path + incoming_variable + '_EEG.csv does not exists!')
        eeg_writer = EEGCSV('EEG_Writer', incoming_variable + '_EEG', final_folder_path, dates[0], dates[1])
        # Start EEGCSV Object
        eeg_writer.start()
        # Write EEG data
        eeg_writer.write_data()
        logging.debug('End of EEGCSV program...')

    # Normalize Facial Expressions File
    fea_file = Path(raw_data_folder_path + incoming_variable + '_Facial.csv')
    if fea_file.is_file():
        # file exists. Normalize Facial
        logging.info('Starting Facial Expression data normalization')
        f = DataNormalizer(
            'Facial',
            incoming_variable + '_Facial',
            raw_data_folder_path,
            final_folder_path,
            dates[0],
            dates[1])
        f.start()
        f.count_total_rows()
        f.normalize_data()
        logging.info('End of Facial Expression data normalization')
    else:
        # file does not exist. Create new EEG
        print(raw_data_folder_path + incoming_variable + '_Facial.csv does not exists!')
        logging.info(raw_data_folder_path + incoming_variable + '_Facial.csv does not exists!')
        fea_writer = FEACSV('EEG_Writer', incoming_variable + '_Facial', final_folder_path, dates[0], dates[1])
        # Start FacialCSV Object
        fea_writer.start()
        # Write Facial data
        fea_writer.write_data()
        logging.debug('End of FEACSV program...')

    # Normalize Notes File
    # notes_file = Path(raw_data_folder_path + incoming_variable + '_Notes.csv')
    # if notes_file.is_file():
    #     # file exists. Normalize Notes
    #     print(raw_data_folder_path + incoming_variable + '_Notes.csv exists!')
    #     logging.info(raw_data_folder_path + incoming_variable + '_Notes.csv exists!')
    #     logging.debug('Normalizing existing Notes file and Copying to ' + final_folder_path + '/ folder')
    #     # Create Normalize_Notes Object
    #     n = NormalizeNotes(
    #         'Normalize_Notes',
    #         incoming_variable + '_Notes',
    #         raw_data_folder_path,
    #         final_folder_path,
    #         diff.seconds
    #     )
    #     # Normalize Existing Notes file
    #     n.normalize()
    #     logging.debug('End of NormalizeNotes program...')
    # else:
    #     # file does not exist. Create new Notes
    #     print(raw_data_folder_path + incoming_variable + '_Notes.csv does not exists!')
    #     # Create NotesCSV Object to Write Notes file as CSV
    #     logging.debug('Running NotesCSV program now...')
    #     # Create NotesCSV Object
    #     notes_writer = NotesCSV('Notes', incoming_variable + '_Notes', final_folder_path, dates[0], dates[1])
    #     notes_writer.start()
    #     # Write Notes
    #     notes_writer.write_data()
    #     logging.debug('End of NotesCSV program...')

except (OSError, ModuleNotFoundError, FileNotFoundError, EOFError, IOError) as ose:
    logging.debug(ose)
    print(ose)
    sys.exit()
except NameError as ne:
    logging.debug(ne)
    print(ne)
    sys.exit()
except ValueError as ve:
    logging.debug(ve)
    print(ve)
    sys.exit()
