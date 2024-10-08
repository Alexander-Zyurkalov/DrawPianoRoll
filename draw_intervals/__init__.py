from matplotlib import pyplot as plt

octaves = 2  # Set the number of octaves you want to see
keys_per_octave = 12
total_keys = octaves * keys_per_octave
bases = ('K', 'T', 'D', 'N', 'M', 'F', 'J', 'G', 'R', 'L', 'P', 'B', 'K')
note_names = bases
white_keys = ['K', 'D', 'M', 'F', 'G', 'L', 'B']
white_keys_per_octave = len(white_keys)
total_white_keys = octaves * white_keys_per_octave
black_keys = ['T', 'N', 'J', 'R', 'P']
white_key_positions = {'K': 0, 'D': 1, 'M': 2, 'F': 3, 'G': 4, 'L': 5, 'B': 6}
black_key_positions = {'T': 0, 'N': 1, 'J': 3, 'R': 4, 'P': 5}
white_key_to_black_key = {'K': 'T', 'D': 'N', 'F': 'J', 'G': 'R', 'L': 'P'}


def draw_piano_roll(path, file_name: str, note_list: list[str]):
   start_x = 1
   note_indexes = [get_note_index(note) for note in note_list]
   total_keys = octaves * keys_per_octave
   plt.figure(figsize=(8, 2*octaves))  # Increase the height of the graph to display more octaves
   plt.ylim(0, total_keys)
   plt.xlim(0, 5)

   start_index_to_place_in_the_middle = calculate_start_index(note_indexes, total_keys)

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

   plt.savefig(path + file_name)
   # plt.show()
   plt.close()


def get_note_index(note:str):
   note_name = note[0]
   octave = int(note[1])
   return note_names.index(note_name) + octave * keys_per_octave


def draw_keyboard(file_name: str, path, highlighted_notes=None):
   highlighted_notes = highlighted_notes or []
   note_indexes = [get_note_index(note) for note in highlighted_notes]
   start_index = calculate_start_index(note_indexes, total_keys)
   start_white_key = round(start_index / keys_per_octave * white_keys_per_octave)

   plt.figure(figsize=(7, 2))
   plt.xlim(-start_white_key, total_white_keys-start_white_key)
   plt.ylim(0, 3)

   # Draw white keys
   for i in range(-start_white_key, white_keys_per_octave * octaves - start_white_key):
      white_key = white_keys[i % white_keys_per_octave]
      octave = i // white_keys_per_octave
      color = 'lightcoral' if f'{white_key}{octave}' in highlighted_notes else 'white'
      plt.gca().add_patch(plt.Rectangle((i, 0), 1, 3,
                                        facecolor=color, edgecolor='black'))

   for i in range(-start_white_key, white_keys_per_octave * octaves - start_white_key):
      white_key = white_keys[i % white_keys_per_octave]
      octave = i // white_keys_per_octave
      if white_key in white_key_to_black_key:
         black_key = white_key_to_black_key[white_key]
         color = 'darkred' if f'{black_key}{octave}' in highlighted_notes else 'black'
         plt.gca().add_patch(plt.Rectangle((i+0.7, 1.3), (1-0.7)*2, 1.7,
                                           facecolor=color, edgecolor='black'))

   plt.axis('off')  # Hide the axes
   plt.savefig(path + file_name)
   # plt.show()
   plt.close()


def calculate_start_index(note_indexes, total_keys):
   smallest_index = min(note_indexes)
   biggest_index = max(note_indexes)
   height = biggest_index - smallest_index
   start_index_to_place_in_the_middle = total_keys // 2 - height // 2 - smallest_index
   return start_index_to_place_in_the_middle
