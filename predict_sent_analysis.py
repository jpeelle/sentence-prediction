#import enchant
from collections import OrderedDict
import sys
import string
import argparse
from math import log2

def csv_reader(csvfiles, replacement_file=None, censor_file=None, exclusion_file=None):
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
    censor_list = []
    exclusion_list = []

    if exclusion_file is not None:
        with open(exclusion_file, 'r') as file:
            for line in file:
                exclusion_list.append(line.rstrip(string.whitespace).rstrip(string.punctuation))

    if censor_file is not None:
        with open(censor_file, 'r') as file:
            for line in file:
                censor_list.append(line.rstrip(string.whitespace).rstrip(string.punctuation))

    if replacement_file is not None:
        replacement_dict = word_replacer(replacement_file)
    else:
        replacement_dict = {}

    for csvfile in csvfiles:
        indices = [] #Tracks columns in the csv that have sentences and answers
        with open(csvfile, 'r') as file:
            header = file.readline()
            header_list = header.split('","')

            sub_id_index = header_list.index('WorkerId')

            for i in range(len(header_list)):
                if 'sentence' in header_list[i]:
                    indices.append(i)

            for line in file:
                line_list = line.split('","')
                if line_list[sub_id_index] in exclusion_list:
                    continue
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
                    if answer in censor_list:
                        answer = answer.replace(answer[1:],'*'*(len(answer)-1))
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
            answer_dict[k].add((key,v[0]))
            answer_dict[k].remove(key)
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
    print('Writing markdown file, {}'.format(filename))
    with open(filename, 'w') as file:
        count = 1 #For printing Question number above each question
        for k, v in data_dict.items():
            file.write('{}. {}\n\n'.format(count, k))
            for key, val in v.items():
                file.write('\t* {} ({:.2f})\n'.format(key, val[0]))
            file.write('\n')
            count += 1

def output_csv(data_dict, filename='output.tsv', separator='\t'):
    print('Writing tsv file, {}'.format(filename))
    with open(filename, 'w') as file:
        max_resp = 0
        for k, v in data_dict.items():
            num_answers = len(v)
            if num_answers > max_resp:
                max_resp = num_answers
        #num_ans_resp = []
        num_ans = []
        num_resp = []
        for i in range(max_resp):
            #num_ans_resp.append('Answer_' + str(i + 1))
            #num_ans_resp.append('Percent_of_Responses_' + str(i + 1))
            num_ans.append('Answer_' + str(i + 1))
            num_resp.append('Percent_of_Responses_' + str(i + 1))
        #header = separator.join(['Question','Number_of_Unique_Responses', 'Response_Entropy', 'Highest_Response_Percent'] + num_ans_resp)
        header = separator.join(['Question','Number_of_Unique_Responses', 'Response_Entropy', 'Highest_Response_Percent'] + num_ans + num_resp)
        file.write(header + '\n')
        for k, v in data_dict.items():
            entropy = 0
            question = k
            num_answers = str(len(v))
            answers = []
            values = []
            highest_percent = 0
            for key, val in v.items():
                p = val[0]
                entropy += p*log2(p)
                if p > highest_percent:
                    highest_percent = p
                #answers.append('{}\t{}'.format(key, val[0]))
                answers.append(str(key))
                values.append(str(val[0]))
            entropy *= -1
            entropy_str = str(round(entropy, 2))
            highest_percent_str = str(highest_percent)
            if len(answers) < max_resp:
                diff = max_resp - len(answers)
                for i in range(diff):
                    answers.append("")
                    values.append("")
            answer_str = separator.join(answers)
            value_str = separator.join(values)
            line = separator.join((question, num_answers, entropy_str, highest_percent_str, answer_str, value_str))
            file.write(line + '\n')

def output_answer_dict(ans_dict, filename):
    with open(filename, 'w') as file:
        max_qs = 0
        for k, v in ans_dict.items():
            if len(v) > max_qs:
                max_qs = len(v)
        num_q = []
        for i in range(max_qs):
            num_q.append('Question_' + str(i + 1))
            num_q.append('Freq_' + str(i + 1))
        header = '\t'.join(['Answer', 'Number_of_Questions'] + num_q)
        file.write(header + '\n')
        for k, v in ans_dict.items():
            v_list = [n[0]+'\t'+str(n[1]) for n in v]
            line = '\t'.join([k]+[str(len(v_list))]+v_list)
            file.write(line + '\n')

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
    print(' -m [filename]\tWrites output to a markdown file, default file name is output.md.')
    print(' -t [filename]\tWrites output to a tsv with "Question Answer 1 Answer 2 ... Freq 1 Freq 2 ..." on each line, default filename is output.tsv.')
    print(' -c <censor file>\tTakes input file with one word to censor per line and censors those words.')
    print(' -e <exclusion file>\tTakes input file with one Worker ID number to exclude per line and removes responses from those workers.')
    exit()

#Optional Files
replacement_file = None
censor_file = None
exclusion_file = None

##Input Files
filenames = []
i = 1
if len(args) == 0:
    print('No input filenames provided. Please include input filenames or run with --help for help.')
while(args[i][0] != '-'):
    filenames.append(args[i])
    i += 1
if not filenames:
    print('No input filenames provided. Please include input filenames or run with --help for help.')
    exit()
##REPLACEMENT FILE
if '-r' in args:
    index = args.index('-r')
    if len(args) < index+2:
        print('No replacement filename provided. Please include a replacement filename or run with --help for help.')
        exit()
    if args[index+1][0] == '-':
        print('No replacement filename provided. Please include a replacement filename or run with --help for help.')
        exit()
    replacement_file = args[index+1]

##CENSOR FILE
if '-c' in args:
    index = args.index('-c')
    if len(args) < index+2:
        print('No censor filename provided. Please include a censor filename or run with --help for help.')
        exit()
    if args[index+1][0] == '-':
        print('No censor filename provided. Please include a censor filename or run with --help for help.')
        exit()
    censor_file = args[index+1]

##EXCLUSION FILE
if '-e' in args:
    index = args.index('-e')
    if len(args) < index+2:
        print('No exclusion filename provided. Please include an exclusion filename or run with --help for help.')
        exit()
    if args[index+1][0] == '-':
        print('No exclusion filename provided. Please include an exclusion filename or run with --help for help.')
        exit()
    exclusion_file = args[index+1]

#Run the program
dicts = csv_reader(filenames, replacement_file, censor_file, exclusion_file)
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
    else:
        output_markdown(sorted_q_dict)
##WRITE TO CSV FILE
if '-t' in args:
    index = args.index('-t')
    if len(args) >= index+2:
        if args[index+1][0] != '-':
            output_csv(sorted_q_dict, args[index+1])
    else:
        output_csv(sorted_q_dict)

##OUTPUTS FOR SEARCH FUNCTION
output_csv(sorted_q_dict, 'questions_dict.tsv', '\t')
output_answer_dict(a_dict, 'answers_dict.tsv')
