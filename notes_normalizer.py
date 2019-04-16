import csv
import logging


class NormalizeNotes:
    """
        class `NormalizeNotes` to Normalize Notes Data CSV
        Usage: Initialize an Object for class using: Obj = NormalizeNotes()
    """
    def __init__(self, name, filename, raw_folder, final_folder, datetime_difference):
        self.name = name
        self.filename = filename
        self.raw_folder = raw_folder
        self.final_folder = final_folder
        self.limit = datetime_difference  # This is the Datetime Difference received from main file
        self.in_csv = None
        self.out_csv = None
        self.reader = None
        self.writer = None
        logging.basicConfig(filename='logs/' + self.filename + '.log', level=logging.DEBUG)

    def normalize(self):
        # Open Raw CSV to read data rows
        with open(self.raw_folder + self.filename + '.csv', newline='') as self.in_csv:
            # Open Final CSV to write data rows
            logging.info('Normalizing Notes file as:\t' + self.final_folder + self.filename + '.csv')
            with open(self.final_folder + self.filename + '.csv', 'w', newline='') as self.out_csv:
                self.reader = csv.reader(self.in_csv, delimiter=',')
                self.writer = csv.writer(self.out_csv)
                i = 0
                for row in self.reader:
                    if 'DATETIME' in row[0]:
                        print('HEADER -->')
                        print(row)
                        logging.info('HEADER --> ')
                        logging.info(row)
                        self.writer.writerow(row)
                        i += 1
                    else:
                        if i <= self.limit + 1:
                            print('ROW -->')
                            print(row)
                            logging.info('ROW -->')
                            logging.info(row)
                            self.writer.writerow(row)
                            i += 1

    def __del__(self):
        self.name = None
        self.filename = None
        self.raw_folder = None
        self.final_folder = None
        self.limit = None
        self.in_csv = None
        self.out_csv = None
        self.reader = None
        self.writer = None
