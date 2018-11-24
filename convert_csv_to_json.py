# -*- coding: utf-8 -*-
import csv
import json
import sys
import codecs

def convert_to_json_object(result, key):
    out_object = {}
    for line in result:
        out_object[result[key]] = line
    return out_object

if __name__ == '__main__':
    f_name = sys.argv[1]
    key = sys.argv[2]
    result = {};
    with open(f_name + '.csv') as f:
        for line in csv.DictReader(f):
            result[line[key]] = line
    f_out = codecs.open(f_name+".json", "w", "utf-8")
    json.dump(result, f_out, ensure_ascii=False)
