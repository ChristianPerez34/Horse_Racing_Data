import os
import re

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
        self.horse_header = ['race_date', 'race_no', 'PGM', 'Name', 'A1FRR', 'A2FRR', 'A3FRR', 'AEPR', 'AAPR', 'ASPR',
                             'CLASS', 'JRATE', 'SCORE']
        self.race_data_list = []
        self.horse_data_list = []
        self.race_row = 0
        self.race_col = 0
        self.race_date = ''
        self.race_no = ''

    def read_file(self):
        lines = self.file.readlines()
        lines = list(map(lambda line: line.strip(), lines))  # Removes new line characters from list
        lines = list(filter(None, lines))  # Removes empty strings from list
        self.write_excel_headers()
        self.gather_relevant_data(lines)

    def gather_race_data(self, line):
        self.race_data_list += line.split(' ')
        self.race_data_list = list(filter(None, self.race_data_list))

    def parse_race_data(self):
        for race_data in self.race_data_list:
            for i in range(0, int(len(race_data) / 4), 4):
                data = race_data[i].split()
                extracted_date = data[2].split('-')
                track = data[0][:3]
                self.race_date = extracted_date[2] + extracted_date[0] + extracted_date[1]
                self.race_no = data[4]
                track_rating = data[10]
                data = race_data[i + 1].split()
                race_distance = data[0].split('f')[0]
                track_surface = data[1]
                data = race_data[i + 2].split()
                purse = data[4][1:]
                race_rating = data[-1]
                data = race_data[i + 3].split()
                wf_1, wf_2, wf_3, wf_4 = data[2], data[3], data[4], data[5]
                wf_5, wf_6, wf_7, wf_8 = data[6], data[7], data[8], data[9]
                data = [track, self.race_date, self.race_no, track_rating, race_distance, track_surface, purse,
                        race_rating,
                        wf_1, wf_2, wf_3, wf_4, wf_5, wf_6, wf_7, wf_8]
                self.write_to_race_excel(data)
        self.race_data_list.clear()

    def write_to_race_excel(self, data):
        for item in data:
            self.race_worksheet.write(self.race_row, self.race_col, item)
            self.race_col += 1
        self.race_row += 1
        self.race_col = 0

    def write_to_horse_excel(self, worksheet, data, headers):
        self.race_col = 0
        if not worksheet.header:
            for header in headers:
                self.race_worksheet.write(self.race_row, self.race_col, header)
                self.race_col += 1
            self.race_col = 0
            self.race_row += 1
        for item in data:
            worksheet.write(self.race_row, self.race_col, item)
            self.race_col += 1
        self.race_row += 1

    def gather_relevant_data(self, lines):
        ignore_race_data_lines = 0
        gather_race_data = 0
        gather_horse_data = 0
        race_data_list = []
        horse_data_list = []
        for line in lines:
            if 'Website: http://quickreckoning.com/horses.htm' in line:
                ignore_race_data_lines = 1
                gather_race_data = 4
                gather_horse_data = 7
                continue
            elif ignore_race_data_lines != 0:
                ignore_race_data_lines -= 1
                continue
            else:
                if gather_race_data != 0:
                    race_data_list.append(line)
                    gather_race_data -= 1
                else:
                    if gather_horse_data != 0:
                        horse_data_list.append(line)
                        gather_horse_data -= 1
                    else:
                        if 'Method Success' in line:
                            self.race_data_list.append(race_data_list)
                            self.horse_data_list.append(horse_data_list)
        self.parse_race_data()
        # self.parse_horse_data()
        self.race_workbook.close()
        # self.horse_workbook.close()

    def parse_horse_data(self):
        for horse_data in self.horse_data_list:
            for data in horse_data:
                data_list = data.split()
                if data_list == self.horse_data_list[2:]:
                    continue
                pgm = data[0]
                name = ''
                for string in data:
                    if re.search('[a-zA-Z]', string):
                        name += string + ' '
                a1frr = data[data.index(name.split()[-1]) + 1].replace('*', '')
                a2frr = data[data.index(name.split()[-1]) + 2].replace('*', '')
                a3frr = data[data.index(name.split()[-1]) + 3].replace('*', '')
                aepr = data[data.index(name.split()[-1]) + 4].replace('*', '')
                aapr = data[data.index(name.split()[-1]) + 5].replace('*', '')
                aspr = data[data.index(name.split()[-1]) + 6].replace('*', '')
                class_ = data[data.index(name.split()[-1]) + 7].replace('*', '')
                jrate = data[data.index(name.split()[-1]) + 8].replace('*', '')
                score = data[-1].replace('*', '')
                data = [self.race_date, self.race_no, pgm, name, a1frr, a2frr, a3frr, aepr, aapr, aspr, class_, jrate,
                        score]
                self.write_to_excel(self.horse_worksheet, data, self.horse_header)
        self.horse_data_list.clear()

    def write_race_excel_header(self):
        for header in self.race_header:
            self.race_worksheet.write(self.race_row, self.race_col, header)
            self.race_col += 1
        self.race_header.clear()
        self.race_col = 0
        self.race_row += 1

    # def write_horse_excel_header(self):

    def write_excel_headers(self):
        self.write_race_excel_header()
