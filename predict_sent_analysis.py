#import enchant
from collections import OrderedDict
import sys
import string
import argparse

def csv_reader(csvfiles, replacement_file=None):
    ''' Takes a list of Mechanical Turk csv files as input. For each file, it
    finds all sentences and answers and creates two dictionaries. One maps
    sentences to answers and their frequencies. The other maps answers to the
    questions in which they appear.
    Inputs: csvfiles, a list of csv files
    Outputs: (question_dict, answer_dict), a tuple of dictionaries
    '''
    question_dict = {}
    answer_dict = {}
    question_numbers = {}
    question_number = 1
    header = []
    if replacement_file not None:
        replacement_dict = word_replacer(replacement_file)
    else:
        replacement_dict = {}
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
                    question = line_list[indices[i]]
                    if question not in question_numbers:
                        question_numbers[question] = str(question_number)
                        question_number += 1
                    answer = line_list[indices[i+num_questions]].lower()
                    answer = answer.rstrip(string.whitespace)
                    answer = answer.rstrip(string.punctuation)
                    if len(answer) == 0:
                        answer = 'No Response'
                    if question_numbers[question] in replacement_dict:
                        if answer in replacement_dict[question_numbers[question]]:
                            answer = replacement_dict[question_numbers[question]][answer]

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
            v[0] = round(int(v[0]) / total, 2)
        question_dict[key] = counter

    return (question_dict, answer_dict)

def word_replacer(replacement_file):
    replacement_dict = {}
    with open(replacement_file, 'r') as file:
        header = file.readline()
        for line in file:
            line_list = line.split(',')
            question_number = ''.join(c for c in line_list[0] if c.isdigit())
            if question_number not in replacement_dict:
                replacement_dict[question_number] = {}
            replacement_dict[question_number][line_list[1]] = line_list[2]
    return replacement_dict

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

def output_markdown(data_dict, filename='output.md'):
    '''Writes input dictionary out to a file.
    Inputs: -data_dict, a dictionary
    -filename, a string (default value is 'output.txt')
    Outputs: None, creates file named filename with data from data_dict
    '''
    filename = filename + extension
    with open(filename, 'w') as file:
        count = 1 #For printing Question number above each question
        for k, v in data_dict.items():
            file.write("{}. {}\n\n".format(count, k))
            for key, val in v.items():
                file.write("\t* {} ({:.2f})\n".format(key, val[0]))
            file.write("\n")
            count += 1

def output_csv(data_dict, filename='output.csv'):
    print("Not yet implemented")
    return 0

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

args = sys.argv

if ('--help' or '-h') in args:
    print('Usage:')
    print(' python3 predict_sent_analysis.py <input file 1> <input file 2> ... [options]')
    print('Optional Arguments:')
    print(' -h, --help\tShow help and exit.')
    print(' -r <replacement file>\tTakes input csv with "Question #,word_to_replace,word_to_replace_with" on each line and makes replacements.')
    print(' -p\tPrints output to stdout.')
    print(' -m\tWrites output to a markdown file.')
    print(' -c\tWrites output to a csv with "Question,(Answer 1, Freq),(Answer 2, Freq),..." on each line.')
    exit()
##Input Files
filenames = []
i = 1
while(args[i][0] != '-'):
    filenames.append(args[i])
    i += 1
if not filenames:
    print('No input filenames provided. Please include input filenames or run with --help for help.')
    exit()
##REPLACEMENT FILE
if '-r' in args:
    index = args.index('-r')
    if len(args) <= index+2:
        print('No replacement filename provided. Please include a replacement filename or run with --help for help.')
        exit()
    if args[index+1][0] == '-':
        print('No replacement filename provided. Please include a replacement filename or run with --help for help.')
        exit()
    replacement_file = args[index+1]

#Run the program
dicts = csv_reader(filenames, replacement_file)
q_dict = dicts[0]
a_dict = dicts[1]
sorted_q_dict = freq_sorter(q_dict)

##PRINT TO STDOUT
if '-p' in args:
    for k, v in q_dict.items():
       sorted_answers = sorted(v.items(), key=lambda x: x[1][0], reverse=True)
       print(k, sorted_answers)
       print('\n')
##WRITE TO MARKDOWN FILE
if '-m' in args:
    index = args.index('-m')
    if len(args) >= index+2:
        if args[index+1][0] != '-':
            output_markdown(sorted_q_dict, args[index+1])
    output_markdown(sorted_q_dict)
##WRITE TO CSV FILE
if '-c' in args:
    if len(args) >= index+2:
        if args[index+1][0] != '-':
            output_markdown(sorted_q_dict, args[index+1])
    output_csv(sorted_q_dict)
