# # Count
# with open('example/sub_id_hits.csv', 'w') as wf:
#     with open('example/demographics.csv', 'r') as rf:
#         header = rf.readline()
#         wf.write('{},{}\n'.format(header.split(',')[0],'NumberOfHits'))
#         demo_questions = header.split(',')
#         demo_questions[-1] = demo_questions[-1].strip()
#         for line in rf:
#             line_list = line.split(',')
#             num_hits = len(line_list) // 10
#             wf.write('{},{}\n'.format(line_list[0],num_hits))

# Combine
with open('consolidated_demographics.csv', 'w') as wf:
    with open('example/demographics.csv', 'r') as rf:
        header = rf.readline()
        header_list = header.split(',')
        header_list[0] = 'AnswerMismatch'
        header_list = ['SubjectID'] + header_list
        wf.write(','.join(header_list))

        for line in rf:
            line_list = line.split(',')
            subject_id = line_list[0]
            line_list = line_list[1:]
            mismatched_answer = 'N/A'

            num_questions = 10
            for i in range(0, len(line_list), num_questions):
                question_set = line_list[i:i+num_questions]
                count = 0
                for j in range(len(question_set)):
                    if (line_list[j] == '' or line_list[j] == '{}') and question_set[j] != '' and question_set[j] != '{}':
                        line_list[j] = question_set[j]
                        count = 0
                    else:
                        if question_set[j] != '' and question_set[j] != '{}':
                            if line_list[j] == question_set[j]:
                                if i != 0:
                                    count += 1
                            else:
                                if type(mismatched_answer) == set:
                                    mismatched_answer.add(header_list[j+2].strip())
                                else:
                                    mismatched_answer = set([header_list[j+2].strip()])
                                count += 0

                if count == len(question_set):
                    for k in range(i,i+num_questions):
                        line_list[k] = None

            if type(mismatched_answer) == set:
                line_list = [';'.join(mismatched_answer)] + line_list
            else:
                line_list = [mismatched_answer] + line_list
            #if mismatched_answer:
            #    line_list = ['answer mismatch'] + line_list
            wf.write(subject_id + ',' + ','.join([x for x in line_list if x is not None ]))
