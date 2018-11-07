#import enchant
from collections import OrderedDict
import sys

def csv_reader(csvfiles):
    ''' Takes a list of Mechanical Turk csv files as input. For each file, it
    finds all sentences and answers and creates two dictionaries. One maps
    sentences to answers and their frequencies. The other maps answers to the
    questions in which they appear.
    Inputs: csvfiles, a list of csv files
    Outputs: (question_dict, answer_dict), a tuple of dictionaries
    '''
    question_dict = {}
    answer_dict = {}
    header = []
    for csvfile in csvfiles:
        indices = [] #Tracks columns in the csv that have sentences and answers
        with open(csvfile, 'r') as file:
            header = file.readline()
            header_list = header.split('","')

            for i in range(len(header_list)):
                if "sentence" in header_list[i]:
                    indices.append(i)

            for line in file:
                line_list = line.split('","')
                #Half of 'indices' are sentences and half are the responses
                num_questions = len(indices) // 2
                for i in range(num_questions):
                    question = line_list[indices[i]].lower()
                    answer = line_list[indices[i+num_questions]].lower()
                    if i == (num_questions - 1):
                        #Strip the newline character off the end of last answer
                        answer = answer.strip('"\n')
                    if question in question_dict:
                        question_dict[question].append(answer)
                    else:
                        question_dict[question] = [answer]
                    if answer in answer_dict:
                        answer_dict[answer].add(question)
                    else:
                        answer_dict[answer] = set([question])

    #Get proportion of total answers
    for key, val in question_dict.items():
        counter = {}
        total = len(val)
        for item in val:
            #Track how many times an item appears as an answer
            if item in counter:
                counter[item][0] += 1
            else:
                counter[item] = [1]
        #Add additional field with proportion of total answers to each answer
        for k, v in counter.items():
            v.append('{}/{}'.format(v[0], total))
        question_dict[key] = counter

    return (question_dict, answer_dict)

def freq_sorter(data_dict):
    '''Sorts answers by the their frequency, such that higher frequency answers
    appear first.
    Inputs: data_dict, a dictionary that maps sentences to a dictionary, which
    maps answers to a pair of: the number of responses and the proportion of
    total responses
    Outputs: data_dict, the same dictionary except answers are now sorted such
    that higher frequency responses appear first
    '''
    for key, value in data_dict.items():
        #Sorts answers in descending order with the frequency as the key
        data_dict[key] = OrderedDict(sorted(value.items(),
                                    key=lambda x: x[1][0], reverse=True))
    return data_dict

def output_file(data_dict, filename='output.txt'):
    '''Writes input dictionary out to a file.
    Inputs: -data_dict, a dictionary
    -filename, a string (default value is 'output.txt')
    Outputs: None, creates file named filename with data from data_dict
    '''
    with open(filename, 'w') as file:
        count = 1 #For printing Question # above each question
        for k, v in data_dict.items():
            file.write("Question {}\n".format(count))
            file.write("{}: {}\n\n".format(k,v))
            count += 1

# # Relies on a Python Library (pyenchant) to determine if a word is real or not
# # doesn't account for misspellings
# def word_checker(data_dict):
#     '''Checks if each answer is in the english dictionary, if not the answer is
#     removed.
#     Inputs: data_dict, a dictionary that maps sentences to a dictionary, which
#     maps answers to a pair of: the number of responses and the proportion of
#     total responses
#     Outputs: data_dict, the same dictionary but potentially with some answers
#     removed
#     '''
#     en_dic = enchant.Dict('en_US')
#     for k, v in data_dict.items():
#         bad_keys = []
#         new_total = 0
#
#         for key in v:
#             if not en_dic.check(key):
#                 bad_keys.append(key)
#         for i in bad_keys:
#             del v[i]
#
#         if len(bad_keys) > 0:
#             for key, val in v.items():
#                 new_total += val[0]
#             for key, val in v.items():
#                 val[1] = '{}/{}'.format(val[0], new_total)
#
#     return data_dict

# # Combines infrequent responses into one 'Other' category
# # doesn't account for misspellings
# def infrequency_checker(data_dict, cutoff=2, write_file):
#     '''Combines responses that have a number of occurrences less than or equal
#     to the cutoff into a single 'Other' category. Optionally writes out all
#     removed responses to a file.
#     Inputs: -data_dict, a dictionary that maps sentences to a dictionary, which
#     maps answers to a pair of: the number of responses and the proportion of
#     total responses
#     -cutoff, an int that determines how few responses an answer can have before
#     it is removed
#     -write_file, a bool, if True then the words are written to a file
#     Outputs: -(data_dict, infreq_resp), a tuple of the dictionary (potentially)
#     with some answer combined into the 'Other' category and the list of answers
#     that were removed
#     -Optionally writes out a file called 'infreq_resp.txt' that contains all the
#     removed words
#     '''
#     infreq_resp = []
#     for k, v in data_dict.items():
#         count = 0
#         bad_keys = []
#
#         for key, val in v.items():
#             if val[0] <= cutoff:
#                 count += val[0]
#                 total = val[1].split('/')[1]
#                 bad_keys.append(key)
#         for i in bad_keys:
#             infreq_resp.append(v[i])
#             del v[i]
#         v['other'] = [count, '{}/{}'.format(count, total)]
#
#     if write_file:
#         with open('infreq_resp.txt', 'w') as file:
#             for resp in infreq_resp:
#                 file.write('{}\n'.format(resp))
#
#     return (data_dict, infreq_resp)

dicts = csv_reader(["fill-in-1x35.csv", "fill-in-1x50.csv", "fill-in-61x50.csv"])
q_dict = dicts[0]
a_dict = dicts[1]
sorted_q_dict = freq_sorter(q_dict)

args = sys.argv

##HELP String
if 'help' in args:
    print('Run with "$python3 predict_sent_analysis.py"')
    print('Optional argument "print" prints output to stdout')
    print('Optional argument "file" writes output to a file')

##PRINT TO STDOUT
if 'print' in args:
    for k, v in q_dict.items():
       sorted_answers = sorted(v.items(), key=lambda x: x[1][0], reverse=True)
       print(k, sorted_answers)
       print('\n')

##WRITE TO FILE
if 'file' in args:
    output_file(sorted_q_dict)
