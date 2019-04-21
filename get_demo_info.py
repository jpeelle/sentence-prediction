import sys

def get_demo_info(csvfiles):
    with open('demo_file.csv', 'w') as dfile:
        demo_info = {}
        for csvfile in csvfiles:
            with open(csvfile, 'r') as cfile:
                header = cfile.readline()
                header_list = header.split('","')
                demo_categories = [i.replace('Answer.', '') for i in header_list if 'Answer' in i and 'sentence' not in i]
                demo_indices = [header_list.index(i) for i in header_list if 'Answer' in i and 'sentence' not in i]
                num_questions = len([i for i in header_list if 'sentence' in i]) // 2
                for line in cfile:
                    line_list = line.split('","')
                    subject_id = line_list[15].strip('"')
                    if subject_id in demo_info:
                        for i in range(len(demo_categories)):
                            demo_info[subject_id].append(line_list[demo_indices[i]])
                    for i in range(len(demo_categories)):
                        if subject_id not in demo_info:
                            demo_info[subject_id] = [line_list[demo_indices[i]]]
                        else:
                            demo_info[subject_id].append(line_list[demo_indices[i]])
                if csvfile == csvfiles[0]:
                    dfile.write('SubjectID')
                    for i in demo_categories:
                        dfile.write(',{}'.format(i))
                    dfile.write('\n')
        for k,v in demo_info.items():
            dfile.write('{}'.format(k))
            for i in v:
                dfile.write(',{}'.format(i))
            dfile.write('\n')

get_demo_info(['example/anonymized_fill-in-1x35.csv','example/anonymized_fill-in-1x50.csv','example/anonymized_fill-in-61x50.csv'])
