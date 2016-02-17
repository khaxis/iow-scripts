import sys

lines = []
for line in sys.stdin:
    #sys.stdout.write(map(ord, line))
    sys.stdout.write(line.rstrip())
    sys.stdout.write('\n')
