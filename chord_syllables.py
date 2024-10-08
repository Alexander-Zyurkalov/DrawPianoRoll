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
   if all(note >= 12 for note in notes):
      notes = [note-12 for note in notes]

   return [f"{bases[note_i % keys_per_octave]}{note_i // keys_per_octave + base_octave}" for note_i in sorted(notes)]

count = 0
for i, root in enumerate(bases):
   for inversion_type in ChordInversionType:
      for chord_type in ChordType:
         if chord_type == ChordType.AUGMENTED and inversion_type != ChordInversionType.ROOT:
            continue
         chord = make_chord(root, chord_type, inversion_type, 0)
         chord_name = "".join(chord)
         print(chord_name)
         file_name_keyboard = f"{chord_name}-{chord_type.value}-{inversion_type.value}-keyboard.png"
         file_name_pianoroll = f"{chord_name}-{chord_type.value}-{inversion_type.value}-pianoroll.png"
         draw_keyboard(file_name_keyboard, 'output/chords/keyboard/', chord)
         draw_piano_roll('output/chords/pianoroll/', file_name_pianoroll, chord)
         count += 1
print("count = ", count)
