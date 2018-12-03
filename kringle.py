#!/usr/bin/env python3

# -*- coding: utf-8 -*-

""" description """

import os
import sys
import logging
import random
import json

__author__ = "Alexander O'Connor <oconnoat@gmail.com>"
__credits__ = ["Alexander O'Connor"]
__license__ = "Copyright"
__version__ = "0.1"
__email__ = "Alexander O'Connor <<oconnoat@gmail.com>"
__status__ = "Prototype"





if __name__ == "__main__":

    entries = [p.strip() for p in open('example.csv','r')]
    participants = [e.split(',')[0] for e in entries]
    exceptions = [(e.split(',')[0], e.split(',')[1]) for e in entries if ',' in e] + [(p,p) for p in participants]

    print('participants:')
    print(len(participants))

    combos = list()
    for i in range(500):
        combination = list()
        r_participants = random.sample(participants, len(participants))
        for i in range(len(participants)):
            combination.append((participants[i], r_participants[i]))
        combos.append(combination)

    print(len(combos))
    filtered = [c for c in combos if not any([e in c for e in exceptions])]
    print(len(filtered))
    result = filtered[0]
    json.dump(result,open('result.json','w'))
