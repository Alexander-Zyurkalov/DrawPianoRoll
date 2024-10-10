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

au_up = 'i'
au_do = 'e'
di_up = 'ya'
di_do = 'yo'

root_colour = 'lightyellow'
mi_up_colour = 'lightblue'
ma_up_colour = 'lightgreen'
pe_up_colour = 'lightyellow'
mi_do_colour = 'lightblue'
ma_do_colour = 'lightgreen'
pe_do_colour = 'lightyellow'

au_up_colour = 'lightsalmon'
au_do_colour = 'lightsalmon'
di_up_colour = 'plum'
di_do_colour = 'plum'

class Chord:
   notes: list[str]
   colours: dict[str, str]
   syllables: str

def make_chord(root_: str, chord_type: ChordType, inversion_type: ChordInversionType,
               base_octave: int) -> Chord:

   root_index = bases.index(root_)
   colours = []
   syllables = [root_suffix, ma_up, pe_up]

   if chord_type == ChordType.MAJOR:
      chord_interval_nums = [0, 4, 7]
      colours = [root_colour, ma_up_colour, pe_up_colour]
   elif chord_type == ChordType.MINOR:
      chord_interval_nums = [0, 3, 7]
      colours = [root_colour, mi_up_colour, pe_up_colour]
   elif chord_type == ChordType.AUGMENTED:
      chord_interval_nums = [0, 4, 8]
      colours = [root_colour, ma_up_colour, au_up_colour]
   elif chord_type == ChordType.DIMINISHED:
      chord_interval_nums = [0, 3, 6]
      colours = [root_colour, mi_up_colour, di_up_colour]

   notes = [(root_index + interval) for interval in chord_interval_nums]

   if inversion_type == ChordInversionType.ROOT:
      syllables = [
         root_suffix,
         mi_up if chord_type == ChordType.MINOR or chord_type == ChordType.DIMINISHED else ma_up,
         di_up if chord_type == ChordType.DIMINISHED else pe_up
      ]
   if inversion_type == ChordInversionType.FIRST_INVERSION:
      notes[0] += 12
      notes  = [notes[1], notes[2], notes[0]]
      colours = [colours[1], colours[2], colours[0]]
      syllables = [
         mi_do if chord_type == ChordType.MINOR or chord_type == ChordType.DIMINISHED else ma_do,
         di_do if chord_type == ChordType.DIMINISHED else pe_do,
         root_suffix
      ]
   if inversion_type == ChordInversionType.SECOND_INVERSION:
      notes[2] -= 12
      notes  = [notes[2], notes[0], notes[1]]
      colours = [colours[2], colours[0], colours[1]]
      notes = [note+12 for note in notes]
      syllables = [
         di_do if chord_type == ChordType.DIMINISHED else pe_do,
         root_suffix,
         mi_up if chord_type == ChordType.MINOR or chord_type == ChordType.DIMINISHED else ma_up,
      ]
   if all(note >= 12 for note in notes):
      notes = [note-12 for note in notes]

   return_chord= Chord()
   return_chord.notes = [f"{bases[note_i % keys_per_octave]}{note_i // keys_per_octave + base_octave}" for note_i in notes]
   return_chord.colours = {}
   s = ""
   for i, note in enumerate(return_chord.notes):
      return_chord.colours[note] = colours[i]
      s += f"{note[0]}{syllables[i]}"
   return_chord.syllables = s
   return return_chord

count = 0
print("Syllables\tmnemonic\tKeyboard\tPianoroll\tTypeAndQuality\tKeyboardColoured\tPianorollColoured")
for i, root in enumerate(bases):
   for inversion_type in ChordInversionType:
      for chord_type in ChordType:
         chord = make_chord(root, chord_type, inversion_type, 0)
         chord_name = f"{root}-{chord.syllables}-{chord_type.value}-{inversion_type.value}"
         file_name_keyboard = f"{chord_name}-keyboard.png"
         file_name_keyboard_coloured = (f"{chord_name}-keyboard-coloured.png")
         file_name_pianoroll = f"{chord_name}-pianoroll.png"
         file_name_pianoroll_coloured = (f"{chord_name}-pianoroll-coloured.png")
         print(f"{chord.syllables}\t\t"
               f"<img src=\"{file_name_keyboard}\">\t"
               f"<img src=\"{file_name_pianoroll}\">\t"
               f"{chord_type.value} {inversion_type.value}\t"
               f"<img src=\"{file_name_keyboard_coloured}\">\t"
               f"<img src=\"{file_name_pianoroll_coloured}\">")
         draw_keyboard('output/chords/keyboard/', file_name_keyboard, chord.notes)
         draw_keyboard('output/chords/keyboard/', file_name_keyboard_coloured, chord.notes,
                       chord.colours)
         draw_piano_roll('output/chords/pianoroll/', file_name_pianoroll, chord.notes)
         draw_piano_roll('output/chords/pianoroll/', file_name_pianoroll_coloured,
                         chord.notes, chord.colours)
         count += 1
print("count = ", count)
