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
    datapoint = {}
    try:
        if not(re.match(r"^\[.*\]$", line)):
            datapoint['Comment_flg'] = 'N'
            splitted = line.split(': ', 1)
            datapoint['Speaker'] = splitted[0]
            datapoint['Text'] = re.sub(r"^\(.*\)\s", '', splitted[1])
            try:
                action = re.findall(r"^\(.*\)", splitted[1])[0]
                datapoint['Action'] = action
            except:
                datapoint['Action'] = ''
            dataset.append(datapoint)
        else:
            datapoint['Comment_flg'] = 'Y'
            datapoint['Text'] = line
            datapoint['Speaker'] = ''
            datapoint['Action'] = ''
            dataset.append(datapoint)
    except:
        exeption_info.append(line)
        print('Bad line exeption:')
        print('Line text: ', line)
        print('====================================================')