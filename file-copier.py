from normalizer import DataNormalizer
import os
import sys
import logging
from shutil import copyfile

# Usage: `python main.py UserName_DateTime`

# Read Commandline Arguments
fullCmdArguments = sys.argv
# Skip first Argument i.e. `program_name.py`
argumentList = fullCmdArguments[1:]
# Read Further Arguments
incoming_variable = argumentList[0]


# Define Folder Paths for Read - Write Operations
logging.basicConfig(filename='logs/' + incoming_variable + '.log', level=logging.DEBUG)

# Set Raw Data folder path from where file has to be copied
raw_data_folder_path = '../../Reports/Chinmayee_Data/final/'
final_folder_path = '../../Reports/' + incoming_variable + '/raw/'
logging.info('Folder Path to Chinmayee\'s EEG data:\t' + raw_data_folder_path)
logging.info('User Raw Folder Path:\t' + final_folder_path)


# Make a New Directory to Store final Data files
# if not os.path.exists(final_folder_path):
#     os.mkdir(final_folder_path)
#     print('Directory ', final_folder_path, ' Created ')
#     logging.info('Directory ' + str(final_folder_path) + ' Created ')
# else:
#     print('Directory ', final_folder_path, ' already exists')
#     logging.info('Directory ' + str(final_folder_path) + ' already exists ')


try:
    # Copy Raw Video File from Src to Destination
    copyfile(raw_data_folder_path + 'chinmayee_27-03-2019_15-49-PM_EEG.csv',
             final_folder_path + incoming_variable + '_EEG.csv')
    logging.info('Copying EEG file from:\t' + raw_data_folder_path + 'chinmayee_27-03-2019_15-49-PM_EEG.csv' +
                 ' to ' + final_folder_path + incoming_variable + '_EEG.csv')

    # Initialize object of class DataNormalizer() to normalize raw data
    # logging.info('Starting EEG data normalization')
    # e = DataNormalizer('EEG', incoming_variable + '_EEG', raw_data_folder_path, final_folder_path)
    # e.start()
    # e.read_dates()
    # e.count_total_rows()
    # e.normalize_data()
    # logging.info('End of EEG data normalization')
    #
    # logging.info('Starting Facial Expression data normalization')
    # f = DataNormalizer('Facial', incoming_variable + '_Facial', raw_data_folder_path, final_folder_path)
    # f.start()
    # dates = f.read_dates()
    # f.count_total_rows()
    # f.normalize_data()
    # logging.info('End of Facial Expression data normalization')
    #
    # # Create NotesCSV Object to Write Notes file as CSV
    # logging.debug('Running NotesCSV program now...')
    # notes_writer = NotesCSV('Notes', incoming_variable + '_Notes', final_folder_path, dates[0], dates[1])
    # # Start NotesCSV Object
    # notes_writer.start()
    # # Write Notes
    # notes_writer.write_data()
    # logging.debug('End of NotesCSV program...')

except Exception as err:
    print(err)
    logging.warning(err)
    sys.exit()