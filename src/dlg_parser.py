import codecs
import re

def parse_input(input_file):
    parsed_dlg = []
    infile = codecs.open(input_file, "r", "utf-8")
    for line in infile:
        quest_str = line
        parsed_q = quest_str.split("\r\n", 0)
        parsed_q = re.sub(r'\r\n$', '', parsed_q[0])
        datapoint = parsed_q
        if (datapoint != ''): parsed_dlg.append(datapoint)
    return parsed_dlg

def line_to_data (dataset, line, exeption_info):
    datapoint={}
    try:
        if not(re.match(r"^\[.*\]$", line)):
            splited = line.split(': ', 1)
            datapoint['speaker'] = splited[0]
            datapoint['text'] = re.sub(r"^\(.*\)\s",'',splited[1])
            try:
                action = re.findall(r"^\(.*\)", splited[1])[0]
                datapoint['action'] = comment
            except:
                datapoint['action'] = ''
            dataset.append(datapoint)
    except:
        exeption_info.append(line)
        print('Bad line exeption:')
        print('Line text: ',line)
        print('====================================================')