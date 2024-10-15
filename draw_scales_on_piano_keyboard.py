from dataclasses import dataclass
from enum import Enum

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from typing import Dict, List, Optional

from draw_intervals import draw_keyboard, note_names, keys_per_octave

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

print("Mode\tPicture")
for mode in scales_intervals.keys():
   for note in note_names[0:12]:
      mode_up = make_modes(note, mode, base_octave=1, direction=Direction.UP)
      mode_do = make_modes(note, mode, base_octave=1, direction=Direction.DOWN)
      file_name_up = f"mode-{mode}-{note}-up.png"
      file_name_do = f"mode-{mode}-{note}-do.png"
      draw_keyboard("output/scales/", file_name_up, mode_up.notes, mode_up.colours, 2)
      draw_keyboard("output/scales/", file_name_do, mode_do.notes, mode_do.colours, 2,)
      print(f"{mode} Mode: {note}->{note}\t<img src=\"{file_name_up}\"/>")
      print(f"{mode} Mode: {note}<-{note}\t<img src=\"{file_name_do}\"/>")
