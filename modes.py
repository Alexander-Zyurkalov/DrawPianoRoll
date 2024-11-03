import csv
from csv import DictReader
from typing import Dict

# Define the CSV file path
csv_file_path = 'modes.txt'


def read_file() -> Dict[str, Dict[str,str]]:
   main_dictionary: Dict[str, Dict[str,str]] = {}
   with open(csv_file_path, mode='r') as csvfile:
      csvreader = csv.DictReader(csvfile, delimiter='\t',
                                 fieldnames=['ModeAndDirection', 'KeyboardPicture', 'SongToPractice', 'Syllables',
                                             'KeyboardPictureNoColours']
                                 )
      for row in csvreader:
         main_dictionary[row['ModeAndDirection']] = row

   return main_dictionary
