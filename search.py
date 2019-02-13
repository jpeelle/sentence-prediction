def search(a_file, q_file):

    search_dicts = read_files(a_file, q_file)
    answer_dict = search_dicts[0]
    num_resp_dict = search_dicts[1]
    entropy_dict = search_dicts[2]

    while(True):
        entropy = False
        num_resp = False
        response = False
        while(True):
            print('Please type search parameters below or "help" for help:')
            user_input = input()
            try:
                user_input.lower()
                break
            except AttributeError:
                print('ERROR: Command not recognized, please try again.')
                continue

        if 'help' in user_input:
            print('Search parameters are "entropy", "unique responses", and "answer".')
            print('Type "exit" to quit.')
            continue
        if user_input == 'exit':
            print('EXITING')
            exit()
        if 'entropy' in user_input:
            entropy = True
        if 'unique responses' in user_input:
            num_resp = True
        if 'answer' in user_input:
            response = True
        if not (entropy or num_resp or response):
            print('ERROR: Command not recognized, please try again.')
            continue

        if entropy:
            while(True):
                print('Please input a lower bound for the response entropy:')
                entropy_lower = input()
                try:
                    entropy_lower = float(entropy_lower)
                    break
                except ValueError:
                    if entropy_lower == 'exit':
                        print('EXITING')
                        exit()
                    else:
                        print('ERROR: Invalid input. Please input a number or type "exit" to quit.')
            while(True):
                print('Please input an upper bound for the response entropy:')
                entropy_upper = input()
                try:
                    entropy_upper = float(entropy_upper)
                    break
                except ValueError:
                    if entropy_upper == 'exit':
                        print('EXITING')
                        exit()
                    else:
                        print('ERROR: Invalid input. Please input a number or type "exit" to quit.')

        if num_resp:
            while(True):
                print('Please input a lower bound for the number of unique responses:')
                num_resp_lower = input()
                try:
                    num_resp_lower = float(num_resp_lower)
                    break
                except ValueError:
                    if num_resp_lower == 'exit':
                        print('EXITING')
                        exit()
                    else:
                        print('ERROR: Invalid input. Please input a number or type "exit" to quit.')
            while(True):
                print('Please input an upper bound for the the number of unique responses:')
                num_resp_upper = input()
                try:
                    num_resp_upper = float(num_resp_upper)
                    break
                except ValueError:
                    if num_resp_upper == 'exit':
                        print('EXITING')
                        exit()
                    else:
                        print('ERROR: Invalid input. Please input a number or type "exit" to quit.')

        if response:
            print('Please input the specific word you want to search for:')
            answer = input()
            answer = answer.lower()
            while(True):
                print('Please enter a lower bound for the number of occurrences (-1 if no minimum number of occurences):')
                occur_lower = input()
                try:
                    occur_lower = float(occur_lower)
                    break
                except ValueError:
                    if occur_lower == 'exit':
                        print('EXITING')
                        exit()
                    else:
                        print('ERROR: Invalid input. Please input a number or type "exit" to quit.')
            while(True):
                print('Please enter an upper bound for the number of occurrences (-1 if no maximum number of occurences):')
                occur_upper = input()
                try:
                    occur_upper = float(occur_upper)
                    break
                except ValueError:
                    if occur_upper == 'exit':
                        print('EXITING')
                        exit()
                    else:
                        print('ERROR: Invalid input. Please input a number or type "exit" to quit.')

        if entropy:
            entropy_results = search_entropy_dict(entropy_dict, entropy_lower, entropy_upper)
        if num_resp:
            num_resp_results = search_num_resp_dict(num_resp_dict, num_resp_lower, num_resp_upper)
        if response:
            response_results = search_answer_dict(answer_dict, answer, occur_lower, occur_upper)

        if entropy:
            if num_resp:
                if response:
                    results = entropy_results.intersection(num_resp_results, response_results)
                else:
                    results = entropy_results.intersection(num_resp_results)
            else:
                if response:
                    results = entropy_results.intersection(response_results)
                else:
                    results = entropy_results
        else:
            if num_resp:
                if response:
                    results = num_resp_results.intersection(response_results)
                else:
                    results = num_resp_results
            else:
                results = response_results

        print('Search returned {} results. Would you like to see the results? [y/n]'.format(len(results)))
        while(True):
            user_input = input()
            user_input = user_input.lower()
            if user_input == 'y':
                for r in results:
                    print('\n')
                    print(r + '\n')
                break
            elif user_input == 'n':
                break
            elif user_input == 'exit':
                print('EXITING')
                exit()
            else:
                print('ERROR: Please type "y" to print results, "n" to skip, or "exit" to quit.')
        #TODO: write out results to a file
    return 0

def read_files(a_file, q_file):
    a_dict = {}
    num_resp_dict = {}
    entropy_dict = {}

    with open(a_file, 'r') as afile:
        header = afile.readline()
        for line in afile:
            line_list = line.split('\t')
            a_dict[line_list[0]] = {}
            p = 1
            while(p < len(line_list[1:])):
                question = line_list[p]
                value = float(line_list[p+1])
                if value in a_dict[line_list[0]]:
                    a_dict[line_list[0]][value].append(question)
                else:
                    a_dict[line_list[0]][value] = [question]
                p += 2
            # for p in line_list[1:]:
            #     p_list = p.split(', 0')
            #     question = p_list[0][1:]
            #     value = float(p_list[1].strip()[:-1])
            #     if value in a_dict[line_list[0]]:
            #         a_dict[line_list[0]][value].append(question)
            #     else:
            #         a_dict[line_list[0]][value] = [question]

    with open(q_file, 'r') as qfile:
        header = qfile.readline()
        for line in qfile:
            line_list = line.split('\t')
            question = line_list[0]
            uniq_resps = line_list[1]
            resp_entropy = line_list[2]
            #answers = line_list[3:]
            if uniq_resps in num_resp_dict:
                num_resp_dict[uniq_resps].append(question)
            else:
                num_resp_dict[uniq_resps] = [question]

            if resp_entropy in entropy_dict:
                entropy_dict[resp_entropy].append(question)
            else:
                entropy_dict[resp_entropy] = [question]

    return (a_dict, num_resp_dict, entropy_dict)

def search_entropy_dict(e_dict, low, high):
    results = set([])
    for k, v in e_dict.items():
        c = float(k)
        if (c >= low) and (c <= high):
            for q in v:
                results.add(q)
    return results

def search_num_resp_dict(n_dict, low, high):
    results = set([])
    for k, v in n_dict.items():
        c = float(k)
        if (c >= low) and (c <= high):
            for q in v:
                results.add(q)
    return results

def search_answer_dict(a_dict, ans, low, high):
    results = set([])
    if low == -1 and high == -1:
        if ans not in a_dict:
            return results
        else:
            for val in a_dict[ans]:
                for sent in a_dict[ans][val]:
                    results.add(sent)
    elif low == -1:
        if ans not in a_dict:
            return results
        else:
            for val in a_dict[ans]:
                if (val <= high):
                    for sent in a_dict[ans][val]:
                        results.add(sent)
    elif high == -1:
        if ans not in a_dict:
            return results
        else:
            for val in a_dict[ans]:
                if (val >= low):
                    for sent in a_dict[ans][val]:
                        results.add(sent)
    else:
        if ans not in a_dict:
            return results
        else:
            for val in a_dict[ans]:
                if (val >= low) and (val <= high):
                    for sent in a_dict[ans][val]:
                        results.add(sent)
    return results

search('example/answers_dict.tsv', 'example/questions_dict.tsv')
