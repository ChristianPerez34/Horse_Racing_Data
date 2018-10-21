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
        self.race_row = 0
        self.race_col = 0
        self.race_date = ''
        self.race_no = ''

    def read_file(self):
        lines = self.file.readlines()
        lines = list(map(lambda line: line.strip(), lines))  # Removes new line characters from list
        lines = list(filter(None, lines))  # Removes empty strings from list
        self.gather_relevant_data(lines)
        for line in self.file:
            line = line.strip('\n')
            if line:
                if 'Website: http://quickreckoning.com/horses.htm' in line:
                    ignore_race_data_lines = 1
                    continue
                if ignore_race_data_lines != 0:
                    ignore_race_data_lines -= 1
                    continue
                else:
                    self.gather_race_data(line)
                    if 'PGM Name' in line:
                        self.parse_race_data()
            # print(line)

    def gather_race_data(self, line):
        self.race_data_list += line.split(' ')
        self.race_data_list = list(filter(None, self.race_data_list))

    def parse_race_data(self):
        track = self.race_data_list[0][:3]
        extracted_date = self.race_data_list[2].split('-')
        self.race_date = extracted_date[2] + extracted_date[0] + extracted_date[1]
        self.race_no = self.race_data_list[4]
        track_rating = self.race_data_list[10]
        race_distance = self.race_data_list[12][:3]
        track_surface = self.race_data_list[13]
        purse = self.race_data_list[34][1:]
        race_rating = self.race_data_list[38]
        wf_1 = self.race_data_list[41]
        wf_2 = self.race_data_list[42]
        wf_3 = self.race_data_list[43]
        wf_4 = self.race_data_list[44]
        wf_5 = self.race_data_list[45]
        wf_6 = self.race_data_list[46]
        wf_7 = self.race_data_list[47]
        wf_8 = self.race_data_list[48]
        data = [track, self.race_date, self.race_no, track_rating, race_distance, track_surface, purse, race_rating,
                wf_1, wf_2, wf_3, wf_4, wf_5, wf_6, wf_7, wf_8]
        self.write_to_excel(self.race_worksheet, data)

    def write_to_excel(self, worksheet, data):
        if not worksheet.header:
            for header in self.race_header:
                self.race_worksheet.write(self.race_row, self.race_col, header)
                self.race_col += 1
            self.race_col = 0
            self.race_row += 1
        for item in data:
            worksheet.write(self.race_row, self.race_col, item)
            self.race_col += 1
        self.race_row += 1
        self.race_data_list.clear()
        # self.race_workbook.close()

    def gather_relevant_data(self, lines):
        ignore_race_data_lines = 0
        for line in lines:
            if 'Website: http://quickreckoning.com/horses.htm' in line:
                ignore_race_data_lines = 1
                continue
            elif ignore_race_data_lines != 0:
                ignore_race_data_lines -= 1
                gather_race_data = 4
                continue
            else:
                if gather_race_data != 0:
                    self.race_data_list.append(line)
                    gather_race_data -= 1
