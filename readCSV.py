#!/usr/bin/python
import csv
from collections import namedtuple

with open('data.csv','r') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for row in f_csv:
        r = Row(*row)
        print(r.sourceUuid)


