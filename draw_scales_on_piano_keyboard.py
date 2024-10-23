from dataclasses import dataclass
from enum import Enum

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from typing import Dict, List, Optional, Literal

from draw_intervals import draw_keyboard, note_names, keys_per_octave
from modes import read_file

# Define scale intervals for each mode, including intervals below the tonic
scales_intervals = {
   'Ionian': ['-P8', '-m7', '-m6', '-P5', '-P4', '-m3', '-m2', 'P1', 'M2', 'M3', 'P4', 'P5', 'M6', 'M7', 'P8'],
   'Dorian': ['-P8', '-m7', '-M6', '-P5', '-P4', '-m3', '-M2', 'P1', 'M2', 'm3', 'P4', 'P5', 'M6', 'm7', 'P8'],
   'Phrygian': ['-P8', '-M7', '-M6', '-P5', '-P4', '-M3', '-M2', 'P1', 'm2', 'm3', 'P4', 'P5', 'm6', 'm7', 'P8'],
   'Lydian': ['-P8', '-m7', '-m6', '-d5', '-P4', '-m3', '-m2', 'P1', 'M2', 'M3', 'A4', 'P5', 'M6', 'M7', 'P8'],  # A4 is augmented 4th
   'Mixolydian': ['-P8', '-m7', '-m6', '-P5', '-P4', '-m3', '-M2', 'P1', 'M2', 'M3', 'P4', 'P5', 'M6', 'm7', 'P8'],
   'Aeolian': ['-P8', '-m7', '-M6', '-P5', '-P4', '-M3', '-M2', 'P1', 'M2', 'm3', 'P4', 'P5', 'm6', 'm7', 'P8'],
   'Locrian': ['-P8', '-M7', '-M6', '-P5', '-A4', '-M3', '-M2', 'P1', 'm2', 'm3', 'P4', 'd5', 'm6', 'm7', 'P8'],  # d5 is diminished 5th
}

interval_semitones = {
   'P1': 0, 'm2': 1, 'M2': 2, 'm3': 3, 'M3': 4, 'd4':5,  'P4': 5,  'A4': 6,   'd5': 6,   'P5': 7, 'A5':8, 'm6': 8,    'M6': 9,  'm7': 10,   'M7': 11,   'P8': 12,
   '-m2': -1, '-M2': -2, '-m3': -3, '-M3': -4, '-d4':-5, '-P4': -5, '-A4': -6, '-d5': -6, '-P5': -7, '-A5':-8, '-m6': -8, '-M6': -9, '-m7': -10, '-M7': -11, '-P8': -12
}



# Function to convert HEX to RGB
def hex_to_rgb(hex_color: str) -> List[float]:
   return mcolors.hex2color(hex_color)

# Function to convert RGB to HEX
def rgb_to_hex(rgb_color: List[float]) -> str:
   return mcolors.to_hex(rgb_color)

# Function to adjust brightness of the color
def adjust_brightness(rgb_color: List[float], factor: float) -> List[float]:
   if factor >= 0:
      # Brighten: move color towards 1
      return [min(1, c + (1 - c) * factor) for c in rgb_color]
   else:
      # Darken: move color towards 0
      return [max(0, c * (1 + factor)) for c in rgb_color]



# Function to determine the color based on the interval with brightness adjustment
def get_interval_color(interval: str) -> str:
   interval_color_map = {
      'P': '#FFFF00',    # Yellow (Perfect intervals)
      'm': '#003F7B',    # Dark Blue (Minor intervals)
      'M': '#00A41B',    # Green (Major intervals)
      'd': '#898989',    # Grey (Diminished intervals)
      'A': '#540000'     # Dark Green (Augmented intervals)
   }
   base_color = interval_color_map[interval[-2]]  # Base color from the map
   rgb_color = hex_to_rgb(base_color)  # Convert to RGB

   # Determine a brightness factor based on the interval distance from the tonic
   distance_from_tonic = interval_semitones[interval] # Absolute distance in semitones
   factor = (0.05 * distance_from_tonic)

   adjusted_rgb = adjust_brightness(rgb_color, factor)  # Adjust brightness
   return rgb_to_hex(adjusted_rgb)  # Convert back to HEX


@dataclass
class ModeNotes:
   notes: list[str]
   colours: dict[str, str]

class Direction(Enum):
   UP = 1
   DOWN = 2

# Function to generate colors for the scale intervals
def make_modes(root: str, scale_type: str, base_octave: int = 1, direction: Direction = Direction.UP) -> ModeNotes:
   root_index = note_names.index(root)

   scale_intervals = []
   # Calculate the notes in the scale
   if direction == Direction.UP:
      scale_intervals = scales_intervals[scale_type][len(scales_intervals[scale_type]) // 2:]
   if direction == Direction.DOWN:
      scale_intervals = scales_intervals[scale_type][:len(scales_intervals[scale_type]) // 2 + 1]

   note_colours: Dict[str, str] = {}

   # Assign colours for notes in the scale
   for i, interval in enumerate(scale_intervals):
      note_index = (root_index + interval_semitones[interval]) % keys_per_octave
      note_name = note_names[note_index]
      octave_adjustment = (root_index + interval_semitones[interval]) // keys_per_octave
      full_note_name = f'{note_name}{base_octave + octave_adjustment}'
      color = get_interval_color(interval)
      note_colours[full_note_name] = color

   return ModeNotes(
      [note for note in note_colours.keys()],
      note_colours
   )


@dataclass
class ModeOutput:
   mode_description: str
   image_tag: str


def generate_mode_output(
      note: str, mode: str, direction: Direction, base_octave: int = 1, output_dir: str = "output/scales/"
) -> ModeOutput:
   mode_notes = make_modes(note, mode, base_octave=base_octave, direction=direction)
   dir_suffix = "up" if direction == Direction.UP else "do"
   file_name = f"mode-{mode}-{note}-{dir_suffix}.png"
   draw_keyboard(output_dir, file_name, mode_notes.notes, mode_notes.colours, 2)
   dir_arrow = "->" if direction == Direction.UP else "<-"
   return ModeOutput(
      f"{mode} Mode: {note}{dir_arrow}{note}",
      f"<img src=\"{file_name}\"/>"
   )

modes_from_file: Dict[str, Dict[str,str]] = read_file()
with open('modes2.txt', mode='w') as csvfile:
   csvfile.write("\t".join(['ModeAndDirection', 'KeyboardPicture', 'SongToPractice', 'Syllables', 
                            'KeyboardPictureNoColours']) + "\n")
   for mode in scales_intervals.keys():
      for note in note_names[0:12]:
         print(", ".join([mode, note]))
         for direction in Direction:
            mode_output = generate_mode_output(note, mode, direction, base_octave=1)
            mode_and_direction = mode_output.mode_description
            keyboard_picture = mode_output.image_tag
            song_to_practice = ""
            syllables = ""
            keyboard_picture_no_colours_ionian = ""
            if mode_and_direction in modes_from_file:
               song_to_practice = modes_from_file[mode_and_direction]["SongToPractice"]
               song_to_practice = "" if song_to_practice is None else song_to_practice
            output = "\t".join(
               [mode_and_direction, keyboard_picture, song_to_practice, syllables, keyboard_picture_no_colours_ionian])
            csvfile.write(output + "\n")
