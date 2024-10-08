from draw_intervals import draw_piano_roll, draw_keyboard, bases


root_suffix = 'u'
mi_up = 'i'
ma_up = 'a'
pe_up = 'u'
mi_do = 'e'
ma_do = 'o'
pe_do = 'y'
tr_up = 'я'
tr_do = 'ё'
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
      draw_keyboard('output/intervals/keyboard/', img_url_keyboard, notes)
      draw_piano_roll('output/intervals/pianoroll/', img_url_piano_roll, notes)
print("count = ", count)
