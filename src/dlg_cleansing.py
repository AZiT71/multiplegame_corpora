import re
import codecs
from os import listdir
from os.path import isfile, join

def cleansing():
    data_dir = "data/ext/src/"
    data = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
    for name in data:
        pure_name = name.split('_dlg.', 1)[0]
        parsed_dlg = []
        infile = codecs.open(data_dir + name, "r", "utf-8")
        lines = infile.readlines()
        for line in lines:
            line = re.sub(r'Edit\r\n$', '\r\n', line)
            line = re.sub(r'^\[]$', '', line)
            line = re.sub(r'^\(\)$', '', line)
            line = re.sub(r'^\(', '[', line)
            line = re.sub(r'\)\r\n$', ']\r\n', line)
            if line != '':
                parsed_dlg.append(line)
        with open('data/ext/cleansed/' + pure_name + '_dlg.txt', 'w', encoding='utf-8-sig',
                  newline='') as outfile:
            outfile.writelines(parsed_dlg)
            outfile.close()
