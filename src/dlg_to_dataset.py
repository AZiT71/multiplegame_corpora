import codecs
import csv
import re


def dlg_to_dataset(dialog, short_name):
    dataset = []
    ord_num = 1
    dlg_size = len(dialog)
    for line in dialog:
        datapoint = {}
        try:
            # creating ID
            datapoint['Row_ID'] = short_name + str(ord_num)
            if ord_num != 1:
                datapoint['Prev_Row_ID'] = short_name + str(ord_num - 1)
            else:
                datapoint['Prev_Row_ID'] = ''
            if ord_num != dlg_size:
                datapoint['Next_Row_ID'] = short_name + str(ord_num + 1)
            else:
                datapoint['Next_Row_ID'] = ''
            ord_num += 1
            # checking if a line is a comment
            # if not -> looking for speaker and  action
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
            # else -> saving full line and add Comment flag
            else:
                datapoint['Comment_flg'] = 'Y'
                datapoint['Text'] = line
                datapoint['Speaker'] = ''
                datapoint['Action'] = ''
            dataset.append(datapoint)
        except Exception:
            print('Bad line exception:'
                  '\nLine ID: ', short_name + str(ord_num),
                  '\nLine text: ', line,
                  '\n')
    return dataset


def dataset_to_file(dataset, pure_name):
    # outfile = open("data/Out/dataset_dead_space.csv", "w")
    with open('data/Out/'+pure_name+'.csv', 'w', encoding='utf-8-sig', newline='') as outfile:
        writer = csv.DictWriter(outfile,
                                ['Row_ID', 'Speaker', 'Text', 'Action', 'Comment_flg', 'Prev_Row_ID', 'Next_Row_ID'])
        writer.writeheader()
        writer.writerows(dataset)
        outfile.close()
