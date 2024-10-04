import matplotlib.pyplot as plt

octaves = 4  # Set the number of octaves you want to see
keys_per_octave = 12
white_keys_per_octave = 7
total_white_keys = octaves * white_keys_per_octave
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Define correct positions of notes on the keyboard
white_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
black_keys = ['C#', 'D#', 'F#', 'G#', 'A#']

# Define white and black key indices for an octave
white_key_positions = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}
black_key_positions = {'C#': 0, 'D#': 1, 'F#': 3, 'G#': 4, 'A#': 5}


# Function to draw the piano keyboard with highlighted keys
def draw_keyboard(highlighted_notes=None):
   highlighted_notes = highlighted_notes or []

   plt.figure(figsize=(15, 4))
   plt.xlim(0, total_white_keys)
   plt.ylim(0, 6)

   # Draw white keys
   for octave in range(octaves):
      for i, white_key in enumerate(white_keys):
         key_index = octave * white_keys_per_octave + i
         color = 'lightcoral' if f'{white_key}{octave}' in highlighted_notes else 'white'
         plt.gca().add_patch(plt.Rectangle((key_index, 0), 1, 3, facecolor=color, edgecolor='black'))

   # Draw black keys
   for octave in range(octaves):
      for i, black_key in enumerate(black_keys):
         key_index = octave * white_keys_per_octave + black_key_positions[black_key]
         color = 'darkred' if f'{black_key}{octave}' in highlighted_notes else 'black'
         plt.gca().add_patch(plt.Rectangle((key_index + 0.7, 1.5), 0.6, 1.5, facecolor=color, edgecolor='black'))

   plt.axis('off')  # Hide the axes
   plt.show()

# Determine the indices for the notes
def get_note_index(note, octave):
   return note_names.index(note) + (octave - 1) * keys_per_octave


def create_chord_inversions(root, chord_type, base_octave):
   root_index = note_names.index(root)
   if chord_type == 'major':
      intervals = [0, 4, 7]  # Intervals for a major triad (Root, Major Third, Perfect Fifth)
   elif chord_type == 'minor':
      intervals = [0, 3, 7]  # Intervals for a minor triad (Root, Minor Third, Perfect Fifth)
   else:
      raise ValueError("Unsupported chord type. Use 'major' or 'minor'.")

   notes = [(root_index + interval) for interval in intervals]
   inversions = []

   # Root position
   root_position = [get_note_index(note_names[note % keys_per_octave], base_octave + (note // keys_per_octave)) for note in notes]
   inversions.append(root_position)

   # First inversion
   first_inversion = root_position[1:] + [root_position[0] + keys_per_octave]
   inversions.append(first_inversion)

   # Second inversion
   second_inversion = [root_position[2] - keys_per_octave] + root_position[0:2]
   inversions.append(second_inversion)

   return inversions

# Function to get the chord notes based on root, type, and inversion
def get_chord_notes(root, chord_type, base_octave=1, inversion=0):
   root_index = note_names.index(root)
   if chord_type == 'major':
      intervals = [0, 4, 7]
   elif chord_type == 'minor':
      intervals = [0, 3, 7]
   else:
      raise ValueError("Unsupported chord type. Use 'major' or 'minor'.")

   inversions = create_chord_inversions(root, chord_type, base_octave)
   chord_notes = inversions[inversion]

   # Get the note names in the correct octave
   note_names_in_chord = []
   for note_index in chord_notes:
      note_name = note_names[note_index % keys_per_octave]
      octave_adjustment = note_index // keys_per_octave
      note_names_in_chord.append(f'{note_name}{base_octave + octave_adjustment}')

   return note_names_in_chord

# Example usage: Draw the chords for the key of A minor, root position
highlighted_notes = get_chord_notes('A', 'major', base_octave=1, inversion=2)
draw_keyboard(highlighted_notes)
