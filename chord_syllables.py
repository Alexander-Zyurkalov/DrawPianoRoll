from enum import Enum

from draw_intervals import draw_keyboard, bases, keys_per_octave, draw_piano_roll


class ChordType(Enum):
   MAJOR = 'major'
   MINOR = 'minor'
   AUGMENTED = 'augmented'
   DIMINISHED = 'diminished'

class ChordInversionType(Enum):
   ROOT = 'root'
   FIRST_INVERSION = 'first inversion'
   SECOND_INVERSION = 'second inversion'


root_suffix = 'u'
mi_up = 'i'
ma_up = 'a'
pe_up = 'u'
mi_do = 'e'
ma_do = 'o'
pe_do = 'y'
tr_up = 'ya'
tr_do = 'yo'

class Chord:
   notes: list[str]
   colours: dict[str, str]

def make_chord(root_: str, chord_type: ChordType, inversion_type: ChordInversionType,
               base_octave: int) -> Chord:

   root_index = bases.index(root_)
   colours = []

   if chord_type == ChordType.MAJOR:
      chord_interval_nums = [0, 4, 7]
      colours = ['yellow', 'green', 'yellow']
   elif chord_type ==ChordType.MINOR:
      chord_interval_nums = [0, 3, 7]
      colours = ['yellow', 'blue', 'yellow']
   elif chord_type == ChordType.AUGMENTED:
      chord_interval_nums = [0, 4, 8]
      colours = ['yellow', 'green', 'orange']
   elif chord_type == ChordType.DIMINISHED:
      chord_interval_nums = [0, 3, 6]
      colours = ['yellow', 'blue', 'purple']

   notes = [(root_index + interval) for interval in chord_interval_nums]

   if inversion_type == ChordInversionType.ROOT:
      pass
   if inversion_type == ChordInversionType.FIRST_INVERSION:
      notes[0] += 12
      notes  = [notes[1], notes[2], notes[0]]
      colours = [colours[1], colours[2], colours[0]]
   if inversion_type == ChordInversionType.SECOND_INVERSION:
      notes[2] -= 12
      notes  = [notes[2], notes[0], notes[1]]
      colours = [colours[2], colours[0], colours[1]]
      notes = [note+12 for note in notes]
   if all(note >= 12 for note in notes):
      notes = [note-12 for note in notes]

   return_chord= Chord()
   return_chord.notes = [f"{bases[note_i % keys_per_octave]}{note_i // keys_per_octave + base_octave}" for note_i in notes]
   return_chord.colours = {}
   for i, note in enumerate(return_chord.notes):
      return_chord.colours[note] = colours[i]
   return return_chord

count = 0
for i, root in enumerate(bases):
   for inversion_type in ChordInversionType:
      for chord_type in ChordType:
         chord = make_chord(root, chord_type, inversion_type, 0)
         chord_name = "".join(chord.notes)
         print(chord_name)
         file_name_keyboard = f"{root}-{chord_name}-{chord_type.value}-{inversion_type.value}-keyboard.png"
         file_name_keyboard_coloured = (f"{root}-{chord_name}-{chord_type.value}-"
                                        f"{inversion_type.value}-keyboard-coloured.png")
         file_name_pianoroll = f"{root}-{chord_name}-{chord_type.value}-{inversion_type.value}-pianoroll.png"
         file_name_pianoroll_coloured = (f"{root}-{chord_name}-{chord_type.value}-"
                                         f"{inversion_type.value}-pianoroll-coloured.png")
         draw_keyboard('output/chords/keyboard/', file_name_keyboard, chord.notes)
         draw_keyboard('output/chords/keyboard/', file_name_keyboard_coloured, chord.notes,
                       chord.colours)
         draw_piano_roll('output/chords/pianoroll/', file_name_pianoroll, chord.notes)
         draw_piano_roll('output/chords/pianoroll/', file_name_pianoroll_coloured,
                         chord.notes, chord.colours)
         count += 1
print("count = ", count)
