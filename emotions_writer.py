import csv
import datetime
import threading
import logging


class FEACSV(threading.Thread):
    """
        class `FEACSV` to Normalize EEG and Facial Expressions Data CSV
        Usage: Initialize an Object for class using: Obj = FEACSV()
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
            Write Data in _Facial.csv
        """
        # Open Notes CSV to write data rows
        logging.info('Generating EEG file as:\t' + self.final_folder + self.filename + '.csv')
        with open(self.final_folder + self.filename + '.csv', 'w', newline='') as self.out_csv:
            # Define Headers which are needed in CSV
            logging.info('Writing Headers in Facial.csv as ->')
            fieldnames = [
                'DATETIME',
                'Angry',
                'Disgusted',
                'Fearful',
                'Happy',
                'Sad',
                'Surprised',
                'Neutral',
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
                    'Angry': 0,
                    'Disgusted': 0,
                    'Fearful': 0,
                    'Happy': 0,
                    'Sad': 0,
                    'Surprised': 0,
                    'Neutral': 0,
                    'Flag': 1
                }
                print(write_row)
                logging.info(write_row)
                self.writer.writerow(write_row)
                self.start_date = self.start_date + datetime.timedelta(seconds=1)
        logging.info('end of Facial.csv file')
        self.out_csv.close()

    def __del__(self):
        self.date = None
        self.writer = None
        self.out_csv = None
        self.flag = 1
        self.total_row_count = 0
