from operator import index

from draw_intervals import draw_piano_roll, draw_keyboard, bases, keys_per_octave

from enum import Enum


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

def make_chord(root_: str, chord_type: ChordType, inversion_type: ChordInversionType,
               base_octave: int) -> list[str]:
   root_index = bases.index(root_)

   if chord_type == ChordType.MAJOR:
      chord_intervals = [0, 4, 7]  # Intervals for a major triad (Root, Major Third, Perfect Fifth)
   elif chord_type ==ChordType.MINOR:
      chord_intervals = [0, 3, 7]  # Intervals for a minor triad (Root, Minor Third, Perfect Fifth)
   elif chord_type == ChordType.AUGMENTED:
      chord_intervals = [0, 4, 8]
   elif chord_type == ChordType.DIMINISHED:
      chord_intervals = [0, 3, 6]
   else:
      raise ValueError("Unsupported chord type. Use 'major' or 'minor'.")

   notes = [(root_index + interval) for interval in chord_intervals]

   if inversion_type == ChordInversionType.ROOT:
      pass
   if inversion_type == ChordInversionType.FIRST_INVERSION:
      notes[0] += 12
   if inversion_type == ChordInversionType.SECOND_INVERSION:
      notes[2] -= 12
      notes = [note+12 for note in notes]

   names = [f"{bases[note_i % keys_per_octave]}{note_i // keys_per_octave + base_octave}" for note_i in notes]
   return sorted(names, key=lambda s: s[1] if len(s) > 1 else '')

count = 0
for i, root in enumerate(bases):
   for inversion_type in ChordInversionType:
      for chord_type in ChordType:
         chord = make_chord(root, chord_type, inversion_type, 0)
         chord_name = "".join(chord)
         file_name = f"{chord_name}-{chord_type.value}-{inversion_type.value}.png"
         print(chord_name)
         draw_keyboard(file_name, 'output/chords/keyboard/', chord)
         count += 1
print("count = ", count)
