from os import system
from os import chdir


chdir('./..')
for i in range(20):
    print(f"running the {i + 1} game")
    system(f'python ./main.py -terminal_viz > test_results\out{i}_board0.txt')
    
