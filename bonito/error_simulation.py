from random import randrange
import numpy as np
import argparse
import os


base_dict = {0: 'A', 1: 'T', 2: 'C', 3: 'G'}


def generate_random_seq(num=100, mean_length=500, std=0):
    # num is the number of sequence we need to generate
    # length is the average length of sequence
    # The generated sequences sequence length follows normal distribution, with standard deviation=std
    lengths = np.random.normal(loc=mean_length, scale=std, size=num)
    lengths = [int(l) for l in lengths]
    seqs = []

    for i in range(num):
        res = ''
        for j in range(lengths[i]):
            rand_num = randrange(4)
            base = base_dict.get(rand_num)
            res += base
        seqs.append(res)

    return seqs


# Generate a FASTA file containing all sequences
def generate_fasta(fasta_path, seqs):
    seq_num = 0

    if os.path.exists(fasta_path):
        os.remove(fasta_path)

    with open(fasta_path, 'a') as f:
        for i in range(len(seqs)):
            title_line = '>sequenceID-' + str(seq_num)
            f.write(title_line + '\n')
            seq_num += 1
            f.write(seqs[i] + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--n', default=100)
    parser.add_argument('--l', default=500)
    parser.add_argument('--std', default=0)
    parser.add_argument('-o', default='reference.fasta')
    args = vars(parser.parse_args())

    num = int(args.get('n'))
    length = int(args.get('l'))
    std = int(args.get('std'))
    fasta_path = args.get('o')
    seqs = generate_random_seq(num=num, mean_length=length, std=std)
    generate_fasta(fasta_path, seqs)
