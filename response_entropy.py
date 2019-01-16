from math import log2

def calc_resp_entropy(probability_list):
    return -1*sum([p*log2(p) for p in probability_list])
