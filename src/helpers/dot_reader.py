#!/usr/bin/env python3
import sys
from helpers.python_ext import stripped_tokens

if len(sys.argv) != 2:
    print('provide dot file for input')
    exit(0)

with open(sys.argv[1]) as input_file:
    lines = stripped_tokens(input_file.readlines())


while True:
    cmd = input('state signals?: ').strip()
    if not cmd:
        continue

    # "t1" -> "t0" [label="-stop/c0"]
    state_and_signals = stripped_tokens(cmd.split())
    state, signals = state_and_signals[0], state_and_signals[1:]

    for l in lines:
        if l.startswith('"{0}"'.format(state)) and '->' in l:
            signals_in_line = ''.join((l[l.index('=')+2:l.index('/')])).split('\\n')
            correct = True
            for s in signals:
                if s in signals_in_line:
                    pass
                else:
                    correct = False
                    break
            if correct:
                print(l)