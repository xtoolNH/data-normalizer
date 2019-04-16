import csv
import datetime
import threading
import logging


class EEGCSV(threading.Thread):
    """
        class `EEGCSV` to Normalize EEG and Facial Expressions Data CSV
        Usage: Initialize an Object for class using: Obj = EEGCSV()
    """
    def __init__(self, name, filename, final_folder, start_date, end_date):
        threading.Thread.__init__(self)
        self.name = name
        self.date = None
        self.writer = None
        self.out_csv = None
        self.flag = 1
        self.total_row_count = 0
        self.filename = filename
        self.final_folder = final_folder
        self.start_date = start_date
        self.end_date = end_date
        logging.basicConfig(filename='logs/' + self.filename + '.log', level=logging.DEBUG)

    def write_data(self):
        """
            Write Data in _EEG.csv
        """
        # Open Notes CSV to write data rows
        logging.info('Generating EEG file as:\t' + self.final_folder + self.filename + '.csv')
        with open(self.final_folder + self.filename + '.csv', 'w', newline='') as self.out_csv:
            # Define Headers which are needed in CSV
            logging.info('Writing Headers in EEG.csv as ->')
            fieldnames = [
                'DATETIME',
                'DELTA',
                'THETA',
                'LOW ALPHA',
                'HIGH ALPHA',
                'LOW BETA',
                'HIGH BETA',
                'LOW GAMMA',
                'HIGH GAMMA',
                'ATTENTION',
                'RELAXED',
                'STRESSED',
                'BLINK',
                'Flag']
            logging.info(fieldnames)
            # Create a Writer Object for csv
            self.writer = csv.DictWriter(self.out_csv, fieldnames=fieldnames)
            # Write Header to CSV file
            self.writer.writeheader()
            self.start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')
            self.end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')
            while self.start_date <= self.end_date:
                write_row = {
                    'DATETIME': str(self.start_date),
                    'DELTA': 0,
                    'THETA': 0,
                    'LOW ALPHA': 0,
                    'HIGH ALPHA': 0,
                    'LOW BETA': 0,
                    'HIGH BETA': 0,
                    'LOW GAMMA': 0,
                    'HIGH GAMMA': 0,
                    'ATTENTION': 0,
                    'RELAXED': 0,
                    'STRESSED': 0,
                    'BLINK': 0,
                    'Flag': 1
                }
                print(write_row)
                logging.info(write_row)
                self.writer.writerow(write_row)
                self.start_date = self.start_date + datetime.timedelta(seconds=1)
        logging.info('end of EEG.csv file')
        self.out_csv.close()

    def __del__(self):
        self.date = None
        self.writer = None
        self.out_csv = None
        self.flag = 1
        self.total_row_count = 0
