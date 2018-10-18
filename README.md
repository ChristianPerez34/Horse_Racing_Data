# Horse_Racing_Data
Parsing of one poorly structured text file into two structured files. The content of files is Horse Racing data which includes facts about races and each horse. 

Instructions:
 Some suggested delimiters in the source file:

1.) Track code and date – taken from source file name i.e. BEL20181008APRCJ.txt

2.) “QuickHorse” – in the source file marks beginning of each race data block.

3.) “Method Success” marks the end of each block of race data

4.) You can easily find other delimiters which consistently appear in the source file which can be used as breakpoints.

Example of the two structured output file is attached as BEL20181008_race.xls and BEL20181008_horse.xls

The finished product will be a Python script that parses a source file trackcode_dateAPRCJ.txt file into trackcode_date_race.xls and trackcode_date_horse.xls files.