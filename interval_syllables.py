bases = ('K', 'T', 'D', 'N', 'M', 'F', 'J', 'G', 'R', 'L', 'P', 'B', 'K')
root_suffix = 'u'
mi_up = 'i'
ma_up = 'a'
pe_up = 'u'
mi_do = 'e'
ma_do = 'o'
pe_do = 'y'
tr_up = ''

qualities = [root_suffix, mi_up, ma_up, mi_up, ma_up, pe_up, tr_up, pe_up, mi_up, ma_up, mi_up, ma_up, pe_up+pe_up]
assert len(bases) == len(qualities)

count = 0
for i, root in enumerate(bases):
   if i == len(bases)-1:
      break
   for j in range(12):
      interval_index = (i + j) % 12
      q = qualities[j]
      n_note = bases[interval_index]
      if root == n_note:
         continue
      count += 1
      variant = root + root_suffix + n_note + q
      print(variant)
print("count = ", count)
