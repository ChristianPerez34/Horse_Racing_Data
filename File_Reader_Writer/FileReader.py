import os

import xlsxwriter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/Data/'


class FileReader:

    def __init__(self, file_name):
        self.file = open(BASE_DIR + file_name, 'r')
        self.horse_workbook = xlsxwriter.Workbook(file_name.split('.')[0] + '_horse.xlsx')
        self.race_workbook = xlsxwriter.Workbook(file_name.split('.')[0] + '_race.xlsx')
        self.horse_worksheet = self.horse_workbook.add_worksheet()
        self.race_worksheet = self.race_workbook.add_worksheet()
        self.race_header = ['track', 'race_date', 'race_no', 'track_rating', 'race_distance', 'track_surface',
                            'purse', 'race_rating', 'WF_1', 'WF_2', 'WF_3', 'WF_4', 'WF_5', 'WF_6', 'WF_7',
                            'WF_8']
        self.race_data_list = []

    def read_file(self):
        print('***********************')
        print(self.race_worksheet.header)
        print('***********************')
        for line in self.file:
            line = line.strip('\n')
            if line:
                if 'QuickHorse' in line or 'Custom Method' in line:
                    continue
                self.gather_race_data(line)
                if 'PGM' in line:
                    self.parse_race_data()
            # print(line)

    def gather_race_data(self, line):
        self.race_data_list += line.split(' ')
        self.race_data_list = list(filter(None, self.race_data_list))

    def parse_race_data(self):
        if not self.race_worksheet.header:
            col = 0
            for header in self.race_header:
                self.race_worksheet.write(0, col, header)
                col += 1
            self.race_workbook.close()
        print(self.race_data_list)
        self.race_data_list.clear()
