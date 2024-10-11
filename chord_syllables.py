from enum import Enum
from typing import Dict

from draw_intervals import draw_keyboard, bases, keys_per_octave, draw_piano_roll
from my_csv import read_file


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

root_colour = 'yellow'

mi_up_colour = 'lightblue'
ma_up_colour = 'lightgreen'
pe_up_colour = 'lightyellow'
au_up_colour = 'lightsalmon'
di_up_colour = 'plum'

mi_do_colour = 'cornflowerblue'
ma_do_colour = 'mediumseagreen'
pe_do_colour = 'khaki'
au_do_colour = 'darksalmon'
di_do_colour = 'orchid'

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
   elif chord_type == ChordType.MINOR:
      chord_interval_nums = [0, 3, 7]
   elif chord_type == ChordType.AUGMENTED:
      chord_interval_nums = [0, 4, 8]
   elif chord_type == ChordType.DIMINISHED:
      chord_interval_nums = [0, 3, 6]

   notes = [(root_index + interval) for interval in chord_interval_nums]

   if inversion_type == ChordInversionType.ROOT:
      syllables = [
         root_suffix,
         mi_up if chord_type == ChordType.MINOR or chord_type == ChordType.DIMINISHED else ma_up,
         di_up if chord_type == ChordType.DIMINISHED else pe_up
      ]
      colours = [
         root_colour,
         mi_up_colour if chord_type == ChordType.MINOR or chord_type == ChordType.DIMINISHED else ma_up_colour,
         di_up_colour if chord_type == ChordType.DIMINISHED else pe_up_colour
      ]
   if inversion_type == ChordInversionType.FIRST_INVERSION:
      notes[0] += 12
      notes  = [notes[1], notes[2], notes[0]]
      syllables = [
         mi_do if chord_type == ChordType.MINOR or chord_type == ChordType.DIMINISHED else ma_do,
         di_do if chord_type == ChordType.DIMINISHED else pe_do,
         root_suffix
      ]
      colours = [
         mi_do_colour if chord_type == ChordType.MINOR or chord_type == ChordType.DIMINISHED else ma_do_colour,
         di_do_colour if chord_type == ChordType.DIMINISHED else pe_do,
         root_colour
      ]
   if inversion_type == ChordInversionType.SECOND_INVERSION:
      notes[2] -= 12
      notes  = [notes[2], notes[0], notes[1]]
      notes = [note+12 for note in notes]
      syllables = [
         di_do if chord_type == ChordType.DIMINISHED else pe_do,
         root_suffix,
         mi_up if chord_type == ChordType.MINOR or chord_type == ChordType.DIMINISHED else ma_up,
      ]
      colours = [
         di_do_colour if chord_type == ChordType.DIMINISHED else pe_do_colour,
         root_colour,
         mi_up_colour if chord_type == ChordType.MINOR or chord_type == ChordType.DIMINISHED else ma_up_colour,
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

chord_from_file: Dict[str, Dict[str,str]] = read_file()
with open('result.txt', mode='w') as csvfile:
   csvfile.write("Syllables\tMnemonic\tKeyboard\tPianoroll\tTypeAndQuality\tKeyboardColoured\tPianorollColoured\n")
   for i, root in enumerate(bases):
      for inversion_type in ChordInversionType:
         for chord_type in ChordType:
            chord = make_chord(root, chord_type, inversion_type, 0)
            chord_name = f"{root}-{chord.syllables}-{chord_type.value}-{inversion_type.value}"
            file_name_keyboard = f"{chord_name}-keyboard-2.png"
            file_name_keyboard_coloured = (f"{chord_name}-keyboard-coloured-2.png")
            file_name_pianoroll = f"{chord_name}-pianoroll-2.png"
            file_name_pianoroll_coloured = (f"{chord_name}-pianoroll-coloured-2.png")

            mnemonic = ''
            if chord.syllables in chord_from_file:
               mnemonic = chord_from_file[chord.syllables]['Mnemonic']

            file_str = f"{chord.syllables}\t" \
                        f"{mnemonic}\t" \
                        f"<img src=\"{file_name_keyboard}\">\t" \
                        f"<img src=\"{file_name_pianoroll}\">\t" \
                        f"{chord_type.value} {inversion_type.value}\t" \
                        f"<img src=\"{file_name_keyboard_coloured}\">\t" \
                        f"<img src=\"{file_name_pianoroll_coloured}\">"
            print(chord.syllables)
            csvfile.write(file_str + '\n')

            draw_keyboard('output/chords/keyboard/', file_name_keyboard, chord.notes)
            draw_keyboard('output/chords/keyboard/', file_name_keyboard_coloured, chord.notes,
                          chord.colours)
            draw_piano_roll('output/chords/pianoroll/', file_name_pianoroll, chord.notes)
            draw_piano_roll('output/chords/pianoroll/', file_name_pianoroll_coloured,
                            chord.notes, chord.colours)
            count += 1
print("count = ", count)
