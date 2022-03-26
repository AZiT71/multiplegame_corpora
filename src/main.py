import dlg_parser
import csv

file_path = "C:/Users/Tim-c/PycharmProjects/multigame_corpora/data/src/dead_space_dlg.txt"
dialog = dlg_parser.parse_input(file_path)
dataset = []
bad_lines = []
for line in dialog:
    dlg_parser.line_to_data(dataset, line, bad_lines)

outfile = open("C:/Users/Tim-c/PycharmProjects/multigame_corpora/data/Out/dataset_dead_space.csv", "w")
writer = csv.DictWriter(outfile, ['speaker', 'text', 'action'])
writer.writeheader()
for datapoint in dataset:
    writer.writerow(datapoint)
outfile.close()

err_log_file = open("C:/Users/Tim-c/PycharmProjects/multigame_corpora/data/Out/_ERR_dataset_dead_space.txt", "w")
for err_line in bad_lines:
    err_log_file.write(err_line)
    err_log_file.write("\r\n=====================================\r\n")
