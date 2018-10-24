import os
import re

import xlsxwriter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/Data/'


class TextToExcel:

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
        self.race_data_list, self.horse_data_list = [], []
        self.race_row, self.race_col = 0, 0
        self.horse_row, self.horse_col = 0, 0
        self.race_date, self.race_no = '', ''

    def read_file(self):
        lines = self.file.readlines()
        lines = list(map(lambda line: line.strip(), lines))  # Removes new line characters from list
        lines = list(filter(None, lines))  # Removes empty strings from list
        return lines
        # self.write_excel_headers()
        # self.gather_relevant_data(lines)

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
                track_surface = data[1] if data[1] != 'INR' else data[2]
                data = race_data[i + 2].split()
                purse = race_data[i + 2][race_data[i + 2].find('PURSE') + 8:race_data[i + 2].find('RACE') - 2]
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

    def write_to_horse_excel(self, data):
        for item in data:
            self.horse_worksheet.write(self.horse_row, self.horse_col, item if item != '????' else '0')
            self.horse_col += 1
        self.horse_row += 1
        self.horse_col = 0

    def gather_relevant_data(self, lines):
        ignore_race_data_lines = 0
        gather_race_data = 0
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
                    if 'Method Success' not in line:
                        horse_data_list.append(line)
                    else:
                        self.race_data_list.append(list(race_data_list))
                        self.horse_data_list.append(list(horse_data_list))
                        race_data_list.clear()
                        horse_data_list.clear()
        # self.parse_race_data()
        # self.parse_horse_data()
        # self.race_workbook.close()
        # self.horse_workbook.close()

    def parse_horse_data(self):
        race_no = 1
        relevant_data = []
        for horse_data in self.horse_data_list:
            for data in horse_data:
                if 'The number of past races' in data:
                    relevant_data = horse_data[1:horse_data.index(data)]
                    break
            for data in relevant_data:
                data_list = data.split()
                pgm = data_list[0]
                name = ''
                for string in data_list:
                    if re.search('[a-zA-Z]', string):
                        name += string + ' '
                a1frr = data_list[data_list.index(name.split()[-1]) + 1].replace('*', '')
                a2frr = data_list[data_list.index(name.split()[-1]) + 2].replace('*', '')
                a3frr = data_list[data_list.index(name.split()[-1]) + 3].replace('*', '')
                aepr = data_list[data_list.index(name.split()[-1]) + 4].replace('*', '')
                aapr = data_list[data_list.index(name.split()[-1]) + 5].replace('*', '')
                aspr = data_list[data_list.index(name.split()[-1]) + 6].replace('*', '')
                class_ = data_list[data_list.index(name.split()[-1]) + 7].replace('*', '')
                jrate = data_list[data_list.index(name.split()[-1]) + 8].replace('*', '')
                score = data_list[-1].replace('*', '')
                parsed_data = [self.race_date, race_no, pgm, name, a1frr, a2frr, a3frr, aepr, aapr, aspr, class_, jrate,
                               score]
                self.write_to_horse_excel(parsed_data)
                parsed_data.clear()
            race_no += 1
        self.horse_data_list.clear()

    def write_race_excel_header(self):
        for header in self.race_header:
            self.race_worksheet.write(self.race_row, self.race_col, header)
            self.race_col += 1
        self.race_header.clear()
        self.race_col = 0
        self.race_row += 1

    def write_horse_excel_header(self):
        for header in self.horse_header:
            self.horse_worksheet.write(self.horse_row, self.horse_col, header)
            self.horse_col += 1
        self.horse_header.clear()
        self.horse_col = 0
        self.horse_row += 1

    def write_excel_headers(self):
        self.write_race_excel_header()
        self.write_horse_excel_header()

    def parse_data(self):
        self.parse_race_data()
        self.parse_horse_data()

    def close_excel_files(self):
        self.race_workbook.close()
        self.horse_workbook.close()


file_reader = TextToExcel('BEL20181008APRCJ.TXT')
file_reader.write_excel_headers()
lines = file_reader.read_file()
file_reader.gather_relevant_data(lines)
file_reader.parse_race_data()
