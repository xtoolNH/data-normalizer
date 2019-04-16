import csv
import datetime
import threading
import logging


def set_flag(date_to_be_verified, start_date, end_date):
    """
        set_flag() function to verify if a date is:
        1. Equal to Recording Start Date
        2. In between Recording Start Date and Recording End Date
        3. Equal to End Date
    """
    if ((date_to_be_verified == start_date) or (date_to_be_verified > start_date)) \
            and ((date_to_be_verified < end_date) or (date_to_be_verified == end_date)):
        # Return 1 if date is in between or equal to Start Date and End Date
        return 1
    else:
        return 0


class DataNormalizer(threading.Thread):
    """
        class `DataNormalizer` to Normalize EEG and Facial Expressions Data CSV
        Usage: Initialize an Object for class using: Obj = DataNormalizer()
    """

    def __init__(self, name, filename, raw_folder, final_folder, flag_start, flag_end):
        threading.Thread.__init__(self)
        self.name = name
        self.prev_date = None
        self.filler_date = None
        self.current_date = None
        self.prev_data = []
        self.filler_row = []
        self.flag = 1
        self.total_row_count = 0
        self.filename = filename
        self.raw_folder = raw_folder
        self.final_folder = final_folder
        self.reader = None
        self.writer = None
        self.in_csv = None
        self.out_csv = None
        self.flag_start = datetime.datetime.strptime(flag_start, '%Y-%m-%d %H:%M:%S')
        self.flag_end = datetime.datetime.strptime(flag_end, '%Y-%m-%d %H:%M:%S')
        logging.basicConfig(filename='logs/' + self.filename + '.log', level=logging.DEBUG)

    def count_total_rows(self):
        """
            To count total number of rows in csv file
        """
        # Open csv file for counting number of rows
        with open(self.raw_folder + self.filename + '.csv', newline='') as in_csv:
            reader = csv.reader(in_csv, delimiter=',')
            self.total_row_count = sum(1 for row in reader)
            print('Total number of rows:\t' + str(self.total_row_count))
            logging.info('Total number of rows:\t' + str(self.total_row_count))
        # Close csv file
        in_csv.close()

    def normalize_data(self):
        """
            Normalization of Data
        """
        # Open Raw CSV to read data rows
        with open(self.raw_folder + self.filename + '.csv', newline='') as self.in_csv:
            # Open Final CSV to write data rows
            with open(self.final_folder + self.filename + '.csv', 'w', newline='') as self.out_csv:
                row_count = 1
                self.reader = csv.reader(self.in_csv, delimiter=',')
                self.writer = csv.writer(self.out_csv)
                for row in self.reader:
                    if self.flag == 0:
                        # First Row
                        print('FIRST ROW -->')
                        print(row)
                        print(len(row))
                        logging.info('FIRST ROW -->')
                        logging.info(row)
                        print('\n')
                        self.prev_data = row
                        self.flag = 1
                    if row[0] == 'DATETIME':
                        # Header Row
                        print('HEADER -->')
                        print(row)
                        logging.info('HEADER -->')
                        row.append('Flag')
                        logging.info(row)
                        print('\n')
                        self.writer.writerow(row)
                        self.flag = 0
                    print('Previous Row -->')
                    print(self.prev_data)
                    print('Actual Row -->')
                    print(row)
                    logging.info('Previous Row -->')
                    logging.info(self.prev_data)
                    logging.info('Actual Row -->')
                    logging.info(row)
                    if self.prev_data:
                        self.current_date = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                        self.prev_date = datetime.datetime.strptime(self.prev_data[0], '%Y-%m-%d %H:%M:%S')
                        diff = self.current_date - self.prev_date
                        print('diff is:\t' + str(diff))
                        logging.info('diff is:\t' + str(diff))
                        if diff == datetime.timedelta(seconds=1):
                            # One Second Difference
                            print('1 second difference -->')
                            print(self.prev_data)
                            logging.info('1 second difference -->')
                            logging.info(self.prev_data)
                            # Set Flag as 0 or 1 in Last Column
                            temp = set_flag(self.prev_date, self.flag_start, self.flag_end)
                            self.prev_data.append(temp)
                            # Write to CSV
                            self.writer.writerow(self.prev_data)
                            print('###########################################')
                            print(row[1])
                            if row[1] == '0':
                                print('current row has 0s')
                                temp = self.prev_data
                                self.prev_data = []
                                self.prev_data.append(row[0])
                                for j in range(1, len(row)):
                                    self.prev_data.append(temp[j])
                                print('current row changed to ->')
                                print(self.prev_data)
                            else:
                                print('###########################################')
                                print('leaving as is...')
                                self.prev_data = row
                        if diff < datetime.timedelta(seconds=1):
                            # Same Datetime Values
                            # print('Same DateTime Values -->')
                            if row[1] > self.prev_data[1]:
                                # print(row)
                                blink = self.prev_data[12]
                                self.prev_data = row
                                self.prev_data[12] = blink
                            else:
                                # print(prev_data)
                                self.prev_data = self.prev_data
                        if diff > datetime.timedelta(seconds=1):
                            # If rows have difference > 1 seconds
                            print('Diff between Datetime > 1')
                            print(self.prev_data)
                            logging.info('Diff between Datetime > 1')
                            logging.info(self.prev_data)
                            # Set Flag as 0 or 1 in Last Column
                            temp = set_flag(self.prev_date, self.flag_start, self.flag_end)
                            self.prev_data.append(temp)
                            # Write to CSV
                            self.writer.writerow(self.prev_data)
                            for i in range(1, int(diff.seconds)):
                                # Traverse and fill total number of rows that were lost
                                filler_date = self.prev_date + datetime.timedelta(seconds=1)
                                filler_date = datetime.datetime.strptime(str(filler_date), '%Y-%m-%d %H:%M:%S')
                                self.filler_row.append(str(filler_date))
                                for j in range(1, len(row)):
                                    self.filler_row.append(self.prev_data[j])
                                # Set Flag as 0 or 1 in Last Column
                                temp = set_flag(filler_date, self.flag_start, self.flag_end)
                                self.filler_row.append(temp)
                                print(self.filler_row)
                                # Write to CSV
                                self.writer.writerow(self.filler_row)
                                self.prev_data = self.filler_row
                                self.prev_date = datetime.datetime.strptime(str(filler_date), '%Y-%m-%d %H:%M:%S')
                                self.filler_row = []
                            self.prev_data = row
                        print('\n')
                        row_count = row_count + 1
                    if row_count == self.total_row_count:
                        print('Last Row -->')
                        self.prev_date = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                        # Set Flag as 0 or 1 in Last Column
                        temp = set_flag(self.prev_date, self.flag_start, self.flag_end)
                        self.prev_data.append(temp)
                        print(self.prev_data)
                        logging.info('Last Row -->')
                        logging.info(self.prev_data)
                        # Write to CSV
                        self.writer.writerow(self.prev_data)
                        print('\n')

    def __del__(self):
        self.out_csv.close()
        self.in_csv.close()
        self.prev_date = None
        self.filler_date = None
        self.current_date = None
        self.prev_data = []
        self.filler_row = []
        self.flag = 1
        self.total_row_count = 0
        self.reader = None
        self.writer = None
        self.in_csv = None
        self.out_csv = None
        self.flag_start = None
        self.flag_end = None
