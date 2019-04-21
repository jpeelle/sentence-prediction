import sys

def mturk_anonymizer(csvfiles):
    '''
    Anonymizes Mechanical Turk data by changing the HITId to a number that can't
    be used to identify the participant, but ensures that each participant has
    the same new number even if they participate in multiple trials.
    Inputs: csvfiles, a list of csv files with Mechanical Turk data that need to
    be anonymized. Assumes the first column is the HITId.
    Outputs: None, writes a file for each input file (files named the same with
    'anonymized_' appended to the front). The file that is written out replaces
    the HITId with a different number that can't be used to identify the
    participant
    '''
    header = []
    id_dict = {} #Keeps track of which number each WorkerId has been mapped to
    id_count = 0
    for csvfile in csvfiles:
        with open('anonymized_'+csvfile, 'w') as anon_file:
            with open(csvfile, 'r') as file:
                header = file.readline()
                header_list = header.split('","')
                anon_file.write(header)
                worker_id_index = header_list.index('WorkerId')

                for line in file:
                    line_list = line.split('","')
                    id = str(line_list[15]) #line_list[15] is the WorkerId
                    if id not in id_dict:
                        id_count += 1
                        id_dict[id] = str(id_count)
                        line_list[15] = id_dict[id]
                    else:
                        line_list[15] = id_dict[id]
                    anon_line = '","'.join(line_list)
                    anon_file.write('"'+anon_line)
'''
Takes each csv with Mechanical Turk data as a command line argument
Example: $python3 anonymizer.py file1.csv file2.csv file3.csv
    Would write an anonymized file for file1.csv, file2.csv, and file3.csv
'''
mturk_anonymizer([f for f in sys.argv[1:]])
