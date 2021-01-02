res = [0,0,0]
for i in range(20):
 file = open(f'out{i}_board0.txt')
 cont = file.read()
 if 'Player 1 Won' in cont:
  res[0] += 1
 elif 'Player 2 Won' in cont:
  res[2] += 1
 else:
  res[1] += 1

print(res)