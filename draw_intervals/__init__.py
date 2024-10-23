from matplotlib import pyplot as plt


keys_per_octave = 12
white_keys = ['K', 'D', 'M', 'F', 'G', 'L', 'B']
white_keys_per_octave = len(white_keys)
bases = ('K', 'T', 'D', 'N', 'M', 'F', 'J', 'G', 'R', 'L', 'P', 'B', 'K')
note_names = bases
black_keys = ['T', 'N', 'J', 'R', 'P']
white_key_positions = {'K': 0, 'D': 1, 'M': 2, 'F': 3, 'G': 4, 'L': 5, 'B': 6}
black_key_positions = {'T': 0, 'N': 1, 'J': 3, 'R': 4, 'P': 5}
white_key_to_black_key = {'K': 'T', 'D': 'N', 'F': 'J', 'G': 'R', 'L': 'P'}


def draw_piano_roll(path, file_name: str, note_list: list[str], colours=None):
   octaves = 2  # Set the number of octaves you want to see
   total_keys = octaves * keys_per_octave
   total_white_keys = octaves * white_keys_per_octave
   colours = colours or {}
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
      colour = colours.get(note_list[i], 'pink')
      plt.gca().add_patch(plt.Rectangle((start_x, note+start_index_to_place_in_the_middle), 3, 1,
                                        facecolor=colour, edgecolor='whitesmoke'))

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


def draw_keyboard(path, file_name: str, highlighted_notes: list[str] = None, colours: dict[str, str] = None, octaves=2):
   total_keys = octaves * keys_per_octave
   total_white_keys = octaves * white_keys_per_octave
   highlighted_notes = highlighted_notes or []
   colours = colours or {}
   note_indexes = [get_note_index(note) for note in highlighted_notes]
   start_index = calculate_start_index(note_indexes, total_keys)
   start_white_key = round(start_index / keys_per_octave * white_keys_per_octave)

   plt.figure(figsize=(7/2*octaves, 2))
   plt.xlim(-start_white_key, total_white_keys-start_white_key)
   plt.ylim(0, 3)

   # Draw white keys
   for i in range(-start_white_key, white_keys_per_octave * octaves - start_white_key):
      white_key = white_keys[i % white_keys_per_octave]
      octave = i // white_keys_per_octave
      colour = 'white'
      if f'{white_key}{octave}' in highlighted_notes:
         colour = colours.get(f'{white_key}{octave}', 'lightcoral')
      plt.gca().add_patch(plt.Rectangle((i, 0), 1, 3,
                                        facecolor=colour, edgecolor='black'))

   for i in range(-start_white_key, white_keys_per_octave * octaves - start_white_key):
      white_key = white_keys[i % white_keys_per_octave]
      octave = i // white_keys_per_octave
      if white_key in white_key_to_black_key:
         black_key = white_key_to_black_key[white_key]
         colour = 'black'
         if f'{black_key}{octave}' in highlighted_notes:
            colour = colours.get(f'{black_key}{octave}', 'darkred')
         plt.gca().add_patch(plt.Rectangle((i+0.7, 1.3), (1-0.7)*2, 1.7,
                                           facecolor=colour, edgecolor='black'))

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

def interval_to_letters(interval_list: list[str]) -> list[str]:
   interval_names = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'Triton', 'P5', 'm6', 'M6', 'm7', 'M7', 'P8']
   up_qualities = ['u', 'i', 'a', 'i', 'a', 'u', 'ya', 'u', 'i', 'a', 'i', 'a', 'uu']
   do_qualities = ['u', 'e', 'o', 'e', 'o', 'y', 'yo', 'y', 'e', 'o', 'e', 'o', 'y']

   result = []
   for interval in interval_list:
      is_downward = interval.startswith('-')
      clean_interval = interval.lstrip('-')  # Remove the '-' sign if present
      if clean_interval == 'A4' or clean_interval == 'd5':
         clean_interval = 'Triton'
      if clean_interval in interval_names:
         index = interval_names.index(clean_interval)
         if is_downward:
            result.append(do_qualities[index])  # Use downward qualities
         else:
            result.append(up_qualities[index])  # Use upward qualities
      else:
         result.append(None)  # In case the interval is not found

   return result
