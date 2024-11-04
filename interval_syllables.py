from draw_intervals import draw_piano_roll, draw_keyboard, bases

# Original syllable definitions
root_suffix = 'u'
mi_up = 'i'
ma_up = 'a'
pe_up = 'u'
mi_do = 'e'
ma_do = 'o'
pe_do = 'y'
tr_up = 'ya'
tr_do = 'yo'

# Map western intervals to Sargam interval names
sargam_intervals_up = {
   'P1': 'Sa',
   'm2': 'ry',
   'M2': 'Re',
   'm3': 'go',
   'M3': 'Ga',
   'P4': 'Ma',
   'Triton': "Mo'",
   'P5': 'Pa',
   'm6': 'dho',
   'M6': 'Dha',
   'm7': 'ny',
   'M7': 'Ni',
   'Octave': 'Sa.'
}

sargam_intervals_down = {
   'P1': 'Sa',
   'm2': '.ny',
   'M2': '.Ni',
   'm3': '.dho',
   'M3': '.Dha',
   'P4': '.Pa',
   'Triton': ".Mo'",
   'P5': '.Ma',
   'm6': '.go',
   'M6': '.Ga',
   'm7': '.ry',
   'M7': '.Re',
   'Octave': '.Sa'
}

intervalNames = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'Triton', 'P5', 'm6', 'M6', 'm7', 'M7', 'Octave']
up_qualities = [root_suffix, mi_up, ma_up, mi_up, ma_up, pe_up, tr_up, pe_up, mi_up, ma_up, mi_up, ma_up, pe_up + pe_up]
do_qualities = [root_suffix, mi_do, ma_do, mi_do, ma_do, pe_do, tr_do, pe_do, mi_do, ma_do, mi_do, ma_do, pe_do + pe_do]
assert len(bases) == len(up_qualities)

# Open CSV file for writing
with open('intervals.csv', 'w', encoding='utf-8') as csvfile:
   # Write header
   csvfile.write("LeftToRight\tRightToLeft\tInterval\tKeyboard\tPianoRoll\tSargamUp\tSargamDown\n")

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
         leftToRight = root + root_suffix + n_note + up_quality
         rightToLeft = n_note + root_suffix + root + do_quality
         img_url_keyboard = f"keyboard_{leftToRight}_{rightToLeft}.png"
         img_url_piano_roll = f"pianoroll_{leftToRight}_{rightToLeft}.png"
         notes = [root+'0', n_note + str((i+j)//12)]

         # Get Sargam interval names for both directions
         sargam_up = sargam_intervals_up[intervalNames[j]]
         sargam_down = sargam_intervals_down[intervalNames[j]]

         # Write data row
         csvfile.write(f"{leftToRight}\t{rightToLeft}\t{intervalNames[j]}\t"
                       f"<img src=\"{img_url_keyboard}\">\t<img src=\"{img_url_piano_roll}\">\t"
                       f"{sargam_up}\t{sargam_down}\n")

         draw_keyboard('output/intervals/keyboard/', img_url_keyboard, notes)
         draw_piano_roll('output/intervals/pianoroll/', img_url_piano_roll, notes)

print("count = ", count)
