import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from typing import Dict, List, Optional

octaves: int = 4  # Set the number of octaves you want to see
keys_per_octave: int = 12
white_keys_per_octave: int = 7
total_white_keys: int = octaves * white_keys_per_octave
note_names: List[str] = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Define correct positions of notes on the keyboard
white_keys: List[str] = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
black_keys: List[str] = ['C#', 'D#', 'F#', 'G#', 'A#']

interval_color_map = {
   'P': '#999900',    # Yellow (Perfect intervals)
   'm': '#003F7B',    # Dark Blue (Minor intervals)
   'M': '#00A41B',    # Green (Major intervals)
   'd': '#898989',    # Grey (Diminished intervals)
   'A': '#540000'     # Dark Green (Augmented intervals)
}

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


# Define white and black key indices for an octave
white_key_positions: Dict[str, int] = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}
black_key_positions: Dict[str, int] = {'C#': 0, 'D#': 1, 'F#': 3, 'G#': 4, 'A#': 5}


# Function to draw the piano keyboard with highlighted keys
def draw_keyboard(highlighted_notes: Optional[Dict[str, str]] = None) -> None:
   highlighted_notes = highlighted_notes or {}

   plt.figure(figsize=(15, 4))
   plt.xlim(0, total_white_keys)
   plt.ylim(0, 6)

   # Draw white keys
   for octave in range(octaves):
      for i, white_key in enumerate(white_keys):
         key_index = octave * white_keys_per_octave + i
         key_name = f'{white_key}{octave}'
         color = highlighted_notes.get(key_name, 'white')
         plt.gca().add_patch(plt.Rectangle((key_index, 0), 1, 3, facecolor=color, edgecolor='black'))

   # Draw black keys
   for octave in range(octaves):
      for i, black_key in enumerate(black_keys):
         key_index = octave * white_keys_per_octave + black_key_positions[black_key]
         key_name = f'{black_key}{octave}'
         color = highlighted_notes.get(key_name, 'black')
         plt.gca().add_patch(plt.Rectangle((key_index + 0.7, 1.5), 0.6, 1.5, facecolor=color, edgecolor='black'))

   plt.axis('off')  # Hide the axes
   plt.show()


def get_note_index(note: str, octave: int) -> int:
   return note_names.index(note) + (octave - 1) * keys_per_octave


# Function to convert HEX to RGB
def hex_to_rgb(hex_color: str) -> List[float]:
   return mcolors.hex2color(hex_color)

# Function to convert RGB to HEX
def rgb_to_hex(rgb_color: List[float]) -> str:
   return mcolors.to_hex(rgb_color)

# Function to adjust brightness of the color
def adjust_brightness(rgb_color: List[float], factor: float) -> List[float]:
   return [min(1, max(0, c * factor)) for c in rgb_color]

# Function to determine the color based on the interval with brightness adjustment
def get_interval_color(interval: str) -> str:
   base_color = interval_color_map[interval[-2]]  # Base color from the map
   rgb_color = hex_to_rgb(base_color)  # Convert to RGB

   # Determine a brightness factor based on the interval distance from the tonic
   distance_from_tonic = abs(interval_semitones[interval])  # Absolute distance in semitones
   factor = 1 + (0.1 * distance_from_tonic)

   adjusted_rgb = adjust_brightness(rgb_color, factor)  # Adjust brightness
   return rgb_to_hex(adjusted_rgb)  # Convert back to HEX


# Function to generate colors for the scale intervals
def make_colours(root: str, scale_type: str, base_octave: int = 1) -> Dict[str, str]:

   root_index = note_names.index(root)

   # Calculate the notes in the scale
   scale_intervals = scales_intervals[scale_type]
   note_colors: Dict[str, str] = {}



   # Assign colors for notes in the scale
   for i, interval in enumerate(scale_intervals):
      note_index = (root_index + interval_semitones[interval]) % keys_per_octave
      note_name = note_names[note_index]
      octave_adjustment = (root_index + interval_semitones[interval]) // keys_per_octave
      full_note_name = f'{note_name}{base_octave + octave_adjustment}'
      print(full_note_name)
      color = get_interval_color(interval)
      note_colors[full_note_name] = color

   return note_colors

note = 'B'
# highlighted_notes = make_colours(note, 'Ionian', base_octave=1)
# highlighted_notes = make_colours(note, 'Dorian', base_octave=1)
# highlighted_notes = make_colours(note, 'Phrygian', base_octave=1)
# highlighted_notes = make_colours(note, 'Lydian', base_octave=1)
# highlighted_notes = make_colours(note, 'Mixolydian', base_octave=1)
highlighted_notes = make_colours(note, 'Aeolian', base_octave=1)
# highlighted_notes = make_colours(note, 'Locrian', base_octave=1)



draw_keyboard(highlighted_notes)
