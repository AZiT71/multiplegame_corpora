import codecs
import csv
import re
from dateparser.search import search_dates


def dlg_to_dataset(dialog, short_name):
    dataset = []
    ord_num = 1
    chapter = ''
    time_location = ''
    dlg_size = len(dialog)
    for line in dialog:
        datapoint = {}
        chapter_score = chapter_scorer(line)
        time_location_score = time_location_scorer(line)
        if chapter_score > time_location_score and chapter_score >= 0.3:
            chapter = line
            continue
        elif chapter_score < time_location_score and time_location_score >= 0.3:
            time_location = line
            continue
        try:
            # creating ID
            datapoint['Row_ID'] = short_name + str(ord_num)
            if ord_num != 1:
                datapoint['Prev_Row_ID'] = short_name + str(ord_num - 1)
            else:
                datapoint['Prev_Row_ID'] = ''
            if ord_num != dlg_size-1:
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
                datapoint['Text'] = re.sub(r"[(][A-z\s,-_]*[)]", '', separated[1])  # updated
                datapoint['Chapter'] = chapter
                datapoint['Time/Location'] = time_location
                try:
                    src_actions = re.findall(r"[(][A-z\s,-_]*[)]", separated[1])  # updated
                    actions = ''
                    for action in src_actions:
                        actions += action+' '
                    datapoint['Action'] = actions
                except Exception:
                    datapoint['Action'] = ''
            # else -> saving full line and add Comment flag
            else:
                datapoint['Comment_flg'] = 'Y'
                datapoint['Text'] = line
                datapoint['Speaker'] = ''
                datapoint['Action'] = ''
                datapoint['Chapter'] = chapter
                datapoint['Time/Location'] = time_location
            dataset.append(datapoint)
        except Exception:
            print('Bad line exception:'
                  '\nLine ID: ', short_name + str(ord_num),
                  '\nLine text: ', line,
                  '\n')
            with open('data/Out/rejected.txt', 'a', encoding='utf-8-sig', newline='') as err_log_file:
                err_log_file.write(short_name + str(ord_num)+': ')
                err_log_file.write(line)
                err_log_file.write("\r\n=====================================\r\n")
                err_log_file.close()
    return dataset


def dataset_to_file(dataset, pure_name):
    with open('data/Out/' + pure_name + '.csv', 'w', encoding='utf-8-sig', newline='') as outfile:
        writer = csv.DictWriter(outfile,
                                ['Row_ID',
                                 'Chapter',
                                 'Time/Location',
                                 'Speaker',
                                 'Text',
                                 'Action',
                                 'Comment_flg',
                                 'Prev_Row_ID',
                                 'Next_Row_ID'])
        writer.writeheader()
        writer.writerows(dataset)
        outfile.close()


def chapter_scorer(line):
    score = 0
    if re.match(r"^\[.*]$", line) or re.match(r"^\"\.*\"$", line) \
            or re.findall(r"^\.*:\s$", line) or len(line) > 50:
        score += 0
    else:
        if not re.findall(r":", line):
            score += 0.15
        if len(line) <= 35:
            score += 0.12
        if re.findall("chapter", str.lower(line)):
            score += 0.2
        if not re.findall(r"[,.!?\-;…”]$", line):
            score += 0.05
        if re.findall(r"[:\-]$", line):
            score += 0.03
        if re.findall(r"\d{1,2}\D", str.lower(line)):
            score += 0.05
    return score


def time_location_scorer(line):
    score = 0
    date_dict = ['next', 'previous', 'ago', 'later', 'after',
                 'before', 'second', 'minute', 'hour', 'day',  'week', 'year', 'apartment',
                 'January',
                 'February',
                 'March',
                 'April',
                 'May',
                 'June',
                 'July',
                 'August',
                 'September',
                 'October',
                 'November',
                 'December']
    if re.match(r"^\[.*]$", line) or re.findall(r"^\.*:\s", line) or len(line) > 80:
        score += 0
    else:
        if len(line) <= 50:
            score += 0.12
        if search_dates(line) is not None:
            score += 0.05
        for word in date_dict:
            if str.lower(line).find(word) != -1:
                score += 0.05
        if re.search(r"\s[1-2]\d{3}", line):
            score += 0.15
        if not re.findall(r":", line):
            score += 0.15
    return score
