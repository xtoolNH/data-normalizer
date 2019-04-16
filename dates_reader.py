import csv
import datetime
import threading
import logging


class DatesReader(threading.Thread):
    """
        To Read Dates from `Records.csv` file which is created by RPA program
        This will give us Recording Start Date and Recording End Date
        Usage: Initialize an Object for class using: Obj = DatesReader()
    """
    def __init__(self, name, filename):
        threading.Thread.__init__(self)
        self.name = name
        self.filename = filename
        self.reader = None
        self.flag_start = None
        self.flag_end = None
        logging.basicConfig(filename='logs/' + self.filename + '.log', level=logging.DEBUG)

    def read_dates(self):
        """
            To Read Dates from `Records.csv` file which is created by RPA program
            This will give us Recording Start Date and Recording End Date
        """
        # Open csv file for reading dates
        with open('../../Reports/Records.csv', newline='') as date_reader:
            self.reader = csv.reader(date_reader, delimiter=',')
            for row in self.reader:
                if 'Recording Start Time' not in row[0]:
                    # Skip first row as it is Header
                    self.flag_start = datetime.datetime.strptime('2019-04-15 11:27:12', '%Y-%m-%d %H:%M:%S')
                    self.flag_end = datetime.datetime.strptime('2019-04-15 11:27:41', '%Y-%m-%d %H:%M:%S')
                    # self.flag_start = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                    # self.flag_end = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            print(self.flag_start)
            print(self.flag_end)
            logging.info('Start Date of Video Recording is:\t' + str(self.flag_start))
            logging.info('End Date of Video Recording is:\t' + str(self.flag_end))
        # Close csv file
        date_reader.close()
        return [str(self.flag_start), str(self.flag_end)]

    def __del__(self):
        self.reader = None
        self.flag_start = None
        self.flag_end = None
