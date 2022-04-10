import dlg_parser
import dlg_to_dataset
from os import listdir
from os.path import isfile, join

dlg_dir = "data/ext/"
g_names = [f for f in listdir(dlg_dir) if isfile(join(dlg_dir, f))]
for g_name in g_names:
    short_name = ''
    pure_name = g_name.split('_dlg.', 1)[0]
    dialog = dlg_parser.parse_input(dlg_dir+g_name)
    for word in g_name.split('_'):
        if word != 'dlg.txt':
            short_name += word[:2]
        else:
            short_name += '-'
    dataset = dlg_to_dataset.dlg_to_dataset(dialog, short_name)
    dlg_to_dataset.dataset_to_file(dataset, pure_name)


# outfile = open("data/Out/dataset_dead_space.csv", "w")
# with open('out.csv', 'w', encoding='utf-8-sig', newline='') as outfile:
#    writer = csv.DictWriter(outfile,
#                            ['Row_ID', 'Speaker', 'Text', 'Action', 'Comment_flg', 'Prev_Row_ID', 'Next_Row_ID'])
#    writer.writeheader()
#    writer.writerows(dataset)
#    outfile.close()

# err_log_file = open("data/Out/_ERR_dataset_dead_space.txt", "w")
# for err_line in bad_lines:
#   err_log_file.write(err_line)
#   err_log_file.write("\r\n=====================================\r\n")
