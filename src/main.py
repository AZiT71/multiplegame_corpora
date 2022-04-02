import dlg_parser
import csv
from os import listdir
from os.path import isfile, join

dlg_dir = "data/src/"
dataset = []
bad_lines = []
short_name = ''
ord_num = 0
g_names = [f for f in listdir(dlg_dir) if isfile(join(dlg_dir, f))]
for g_name in g_names:
    dialog = dlg_parser.parse_input(dlg_dir+g_name)
    for word in g_name.split('_'):
        if word != 'dlg.txt':
            short_name += word[0]
        else:
            short_name += '-'
    for line in dialog:
        ord_num += 1
        dlg_parser.line_to_data(dataset, line, bad_lines, short_name, ord_num, len(dialog))


outfile = open("data/Out/dataset_dead_space.csv", "w")
writer = csv.DictWriter(outfile, ['Row_ID', 'Speaker', 'Text', 'Action', 'Comment_flg', 'Prev_Row_ID', 'Next_Row_ID'])
writer.writeheader()
writer.writerows(dataset)
outfile.close()

err_log_file = open("data/Out/_ERR_dataset_dead_space.txt", "w")
for err_line in bad_lines:
    err_log_file.write(err_line)
    err_log_file.write("\r\n=====================================\r\n")
