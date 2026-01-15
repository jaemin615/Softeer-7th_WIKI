import sys
import re

for line in sys.stdin:
    line = line.strip().lower()
    words = re.findall(r'[a-z]+', line)
    for word in words:
        print(f'{word}\t1')