import csv
import os
import time

def read_checkpoint():
    if os.path.exists('raw-data/checkpoint.txt'):
        with open('checkpoint.txt', 'r') as file:
            return int(file.read().strip)
    return 0

