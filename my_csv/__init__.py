import csv
from csv import DictReader
from typing import Dict

# Define the CSV file path
csv_file_path = 'data.txt'


def read_file() -> Dict[str, Dict[str,str]]:
   main_dictionary: Dict[str, Dict[str,str]] = {}
   with open(csv_file_path, mode='r') as csvfile:
      csvreader = csv.DictReader(csvfile, delimiter='\t',
                                 fieldnames=['Syllables', 'Mnemonic', 'Keyboard', 'Pianoroll',
                                             'TypeAndQuality', 'KeyboardColoured', 'PianorollColoured']
                                 )
      for row in csvreader:
         main_dictionary[row['Syllables']] = row

   return main_dictionary
