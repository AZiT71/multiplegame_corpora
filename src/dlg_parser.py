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
        if datapoint != '':
            parsed_dlg.append(datapoint)
    return parsed_dlg
