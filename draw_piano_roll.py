import matplotlib.pyplot as plt

chord_key = 'F#'
octaves = 4  # Set the number of octaves you want to see
keys_per_octave = 12
total_keys = octaves * keys_per_octave
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

plt.figure(figsize=(15, 2 * octaves))  # Increase the height of the graph to display more octaves
plt.ylim(0, total_keys)
plt.xlim(0, 28)
plt.yticks(range(total_keys), [f'{note}{octave}' for octave in range(1, octaves + 1) for note in note_names])

# Draw the background of the keys with pale colors
for i in range(total_keys):
   is_sharp = '#' in note_names[i % keys_per_octave]
   color = 'whitesmoke' if is_sharp else 'white'
   plt.gca().add_patch(plt.Rectangle((0, i), 28, 1, facecolor=color, edgecolor='whitesmoke'))


# Determine the indices for the notes
def get_note_index(note, octave):
   return note_names.index(note) + (octave - 1) * keys_per_octave


# Define the chords
def get_chord_notes(root, chord_type):
   root_index = note_names.index(root)
   if chord_type == 'major':
      intervals = [0, 4, 7]  # Intervals for a major triad (Root, Major Third, Perfect Fifth)
   elif chord_type == 'minor':
      intervals = [0, 3, 7]  # Intervals for a minor triad (Root, Minor Third, Perfect Fifth)
   else:
      raise ValueError("Unsupported chord type. Use 'major' or 'minor'.")

   chord_notes = [(root_index + interval) for interval in intervals]
   return chord_notes


# Create the chord inversions
def create_chord_inversions(root, chord_type, base_octave):
   notes = get_chord_notes(root, chord_type)
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


# Function to draw chords
def draw_chord(chord, start_x, color):
   for i, note in enumerate(chord):
      plt.gca().add_patch(plt.Rectangle((start_x, note), 3, 1, facecolor=color, edgecolor='none'))


# Draw all chords considering the background and pale colors
def draw_chords_for_key(root, chord_type, base_octave, shift_x=1):
   chords = create_chord_inversions(root, chord_type, base_octave)
   colors = ['lightblue'] * 3  # if chord_type == 'major' else ['lightpink'] * 3
   for i, chord in enumerate(chords):
      draw_chord(chord, shift_x + i * 4, colors[i])

draw_chords_for_key(chord_key, 'major', 2)
draw_chords_for_key(chord_key, 'minor', 2, shift_x=13)

# Set up the grid and remove the labels with pale colors
plt.grid(True, color='whitesmoke', linestyle='-', linewidth=1.5)
plt.xticks([])
plt.yticks([])
plt.show()
