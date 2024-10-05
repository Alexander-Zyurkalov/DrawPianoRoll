import matplotlib.pyplot as plt

from make_piano_chord_pictures import height

octaves = 2  # Set the number of octaves you want to see
keys_per_octave = 12
white_keys_per_octave = 7
total_white_keys = octaves * white_keys_per_octave
bases = ('K', 'T', 'D', 'N', 'M', 'F', 'J', 'G', 'R', 'L', 'P', 'B', 'K')
note_names = bases

# Define the correct positions of notes on the keyboard
white_keys = ['K', 'D', 'M', 'F', 'G', 'L', 'B']
black_keys = ['T', 'N', 'J', 'R', 'P']

# Define white and black key indices for an octave
white_key_positions = {'K': 0, 'D': 1, 'M': 2, 'F': 3, 'G': 4, 'L': 5, 'B': 6}
black_key_positions = {'T': 0, 'N': 1, 'J': 3, 'R': 4, 'P': 5}
def draw_keyboard(file_name: str, highlighted_notes=None):
   highlighted_notes = highlighted_notes or []

   plt.figure(figsize=(7, 4))
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
   plt.savefig('output/intervals/keyboard/' + file_name)
   plt.close()

def get_note_index(note:str):
   note_name = note[0]
   octave = int(note[1])
   return note_names.index(note_name) + octave * keys_per_octave

def draw_piano_roll(file_name: str, note_list: list[str]):
   start_x = 1
   note_indexes = [get_note_index(note) for note in note_list]
   total_keys = octaves * keys_per_octave
   plt.figure(figsize=(8, 2*octaves))  # Increase the height of the graph to display more octaves
   plt.ylim(0, total_keys)
   plt.xlim(0, 5)

   smallest_index = min(note_indexes)
   biggest_index = max(note_indexes)
   height = biggest_index - smallest_index
   start_index_to_place_in_the_middle = total_keys//2 - height//2 - smallest_index

   # Draw the background for the piano roll
   for i in range(-start_index_to_place_in_the_middle, total_keys-start_index_to_place_in_the_middle):
      is_sharp = note_names[i % keys_per_octave] in black_keys
      back_colour = 'whitesmoke' if is_sharp else 'white'
      plt.gca().add_patch(plt.Rectangle((0, i+start_index_to_place_in_the_middle), 28, 1,
                                        facecolor=back_colour, edgecolor='whitesmoke'))

   # Draw the notes on the piano roll
   for i, note in enumerate(note_indexes):
      plt.gca().add_patch(plt.Rectangle((start_x, note+start_index_to_place_in_the_middle), 3, 1,
                                        facecolor='pink', edgecolor='whitesmoke'))

   # Remove axis ticks and labels for a cleaner look on the piano roll
   plt.xticks([])
   plt.yticks([])
   
   plt.savefig('output/intervals/pianoroll/' + file_name)
   # plt.show()
   plt.close()


root_suffix = 'u'
mi_up = 'i'
ma_up = 'a'
pe_up = 'u'
mi_do = 'e'
ma_do = 'o'
pe_do = 'y'
tr_up = ''
tr_do = ''
intervalQualities = {
   mi_up: 'm',
   ma_up: 'M',
   pe_up: 'P',
   tr_up: ''
}
intervalNames = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'Triton', 'P5', 'm6', 'M6', 'm7', 'M7', 'Octave']
up_qualities = [root_suffix, mi_up, ma_up, mi_up, ma_up, pe_up, tr_up, pe_up, mi_up, ma_up, mi_up, ma_up, pe_up + pe_up]
do_qualities = [root_suffix, mi_do, ma_do, mi_do, ma_do, pe_do, tr_do, pe_do, mi_do, ma_do, mi_do, ma_do, pe_do + pe_do]
assert len(bases) == len(up_qualities)

count = 0
for i, root in enumerate(bases):
   if i == len(bases)-1:
      break
   for j in range(12):
      interval_index = (i + j) % 12
      up_quality = up_qualities[j]
      do_quality = do_qualities[j]
      n_note = bases[interval_index]
      if root == n_note:
         continue
      count += 1
      if intervalNames[j] == 'Triton':
         continue
      leftToRight = root + root_suffix + n_note + up_quality
      rightToLeft = n_note + root_suffix + root + do_quality
      img_url_keyboard = f"keyboard_{leftToRight}_{rightToLeft}.png"
      img_url_piano_roll = f"pianoroll_{leftToRight}_{rightToLeft}.png"
      notes = [root+'0', n_note + str((i+j)//12)]
      print(f"{leftToRight}\t\t"
            f"{rightToLeft}\t\t"
            f"{intervalNames[j]}\t"
            f"<img src=\"{img_url_keyboard}\">\t"
            f"<img src=\"{img_url_piano_roll}\">")
      draw_keyboard(img_url_keyboard, notes)
      draw_piano_roll(img_url_piano_roll, notes)
print("count = ", count)
