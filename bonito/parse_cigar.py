import re
from collections import defaultdict
from util import split_cigar

import numpy as np
import matplotlib.pyplot as plt
import sys


def parse_file(cigar_path):
    with open(cigar_path) as cigar_txt:
        line_count = 0
        bins = bin_num
        sum_ins_hist = np.zeros(bins)
        sum_del_hist = np.zeros(bins)
        sum_sub_hist = np.zeros(bins)

        total_ins = 0
        total_sub = 0
        total_del = 0

        total_len = 0

        for cigar_str in cigar_txt:
            if cigar_str[0] != '*':
                line_count += 1
                ref_len = ref_str_len(cigar_str)
                counts, ins_pos, del_pos, sub_pos = parse_str(cigar_str)
                total_ins += counts.get('I')
                total_del += counts.get('D')
                total_sub += counts.get('X')

                num_match = counts.get('=')
                total_len += total_ins + total_del + total_sub + num_match

                bin_width = int(round(ref_len / bins))
                ins_hist = to_hist_arr(ref_len, bin_width, ins_pos)
                del_hist = to_hist_arr(ref_len, bin_width, del_pos)
                sub_hist = to_hist_arr(ref_len, bin_width, sub_pos)

                sum_ins_hist += ins_hist
                sum_del_hist += del_hist
                sum_sub_hist += sub_hist

        avg_ins_hist = sum_ins_hist / line_count
        avg_del_hist = sum_del_hist / line_count
        avg_sub_hist = sum_sub_hist / line_count

        ins_rate = total_ins / total_len * 100
        del_rate = total_del / total_len * 100
        sub_rate = total_del / total_len * 100

    return avg_ins_hist, avg_del_hist, avg_sub_hist, ins_rate, del_rate, sub_rate


def to_hist_arr(cigar_len, bin_width, op_pos):
    res = np.zeros(bin_num)
    rem_cigar_len = cigar_len
    op_start = 0
    # Sum array of errors into 100 bins
    for pos in range(bin_num):
        cur_bin_width = round(rem_cigar_len / (bin_num - pos))
        num = sum(op_pos[op_start: op_start + cur_bin_width])
        op_start += cur_bin_width
        res[pos] = num
        rem_cigar_len -= cur_bin_width
    # Scale by bin_width
    return np.array(res) / bin_width


def parse_str(cigar_str):
    cigar_len = ref_str_len(cigar_str)
    cur_pos = 0
    ins_pos = np.zeros(cigar_len)
    del_pos = np.zeros(cigar_len)
    sub_pos = np.zeros(cigar_len)
    counts = defaultdict(int)

    for count, op in re.findall(split_cigar, cigar_str):
        count = int(count)
        if op == 'I':
            fill_pos_arr(cur_pos, count, ins_pos)
        elif op == 'D':
            fill_pos_arr(cur_pos, count, del_pos)
        elif op == 'X':
            fill_pos_arr(cur_pos, count, sub_pos)
        cur_pos += count

        # Count the total number of matches, insertion/deletion/substitution errors
        counts[op] += count

    # Return the dictionary showing the count number of each operation
    # Also return the arrays representing insertion/deletion/substitution error positions
    return counts, ins_pos, del_pos, sub_pos


def ref_str_len(cigar_str):
    res = 0
    for count, op in re.findall(split_cigar, cigar_str):
        res += int(count)
    return res


def fill_pos_arr(cur_pos, count, pos_arr):
    for i in range(cur_pos, cur_pos + count):
        pos_arr[i] = 2
    return pos_arr


if __name__ == '__main__':
    cigar_path = sys.argv[1]
    bin_num = int(sys.argv[2])

    avg_ins_hist, avg_del_hist, avg_sub_hist, ins_rate, del_rate, sub_rate = parse_file(cigar_path)
    print('Average insertion error rate is: {ins_rate}%'.format(ins_rate=ins_rate))
    print('Average deletion error rate is: {del_rate}%'.format(del_rate=del_rate))
    print('Average substitution error rate is: {sub_rate}%'.format(sub_rate=sub_rate))

    agg_err_hist = avg_ins_hist + avg_del_hist + avg_sub_hist

    plt.xlabel('Relative Position (%)')
    plt.ylabel('Frequency (%)')

    x = list(range(0, 100, int(100 / bin_num)))
    agg_sum = sum(agg_err_hist)
    normalize_factor = 100 / agg_sum

    plt.plot(x, avg_ins_hist * normalize_factor, label='Insertion error')
    plt.plot(x, avg_del_hist * normalize_factor, label='Deletion error')
    plt.plot(x, avg_sub_hist * normalize_factor, label='Substitution error')
    plt.plot(x, agg_err_hist * normalize_factor, label='Total error')

    plt.legend()
    plt.show()



