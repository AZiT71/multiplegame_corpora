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


def line_to_data(dataset, line, exception_info, short_name, ord_num, dlg_size):
    datapoint = {}
    try:
        if not (re.match(r"^\[.*]$", line)):
            datapoint['Comment_flg'] = 'N'
            separated = line.split(': ', 1)
            datapoint['Speaker'] = separated[0]
            datapoint['Text'] = re.sub(r"^\(.*\)\s", '', separated[1])
            try:
                action = re.findall(r"^\(.*\)", separated[1])[0]
                datapoint['Action'] = action
            except Exception:
                datapoint['Action'] = ''
            dataset.append(datapoint)
        else:

            datapoint['Comment_flg'] = 'Y'
            datapoint['Text'] = line
            datapoint['Speaker'] = ''
            datapoint['Action'] = ''
            dataset.append(datapoint)
        datapoint['Row_ID'] = short_name + str(ord_num)
        if id != 1:
            datapoint['Prev_Row_ID'] = short_name + str(ord_num - 1)
        else:
            datapoint['Prev_Row_ID'] = ''
        if id != dlg_size:
            datapoint['Next_Row_ID'] = short_name + str(ord_num + 1)
        else:
            datapoint['Next_Row_ID'] = ''
    except Exception:
        exception_info.append(line)
        print('Bad line exception:\nLine text: ', line, '\n==========================\n')
