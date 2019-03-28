#!/usr/bin/env python3

import click
import sys
from Bio import SeqIO


@click.command()
@click.option('--in-fastq', help='gz compressed input fastq file')
@click.option('--out-fastq', help='gz compressed output fastq file')
@click.option('--keep-reads', help='gz compressed file with read names to keep')
@click.option('--verbose', help='verbose', default=False, is_flag=True, flag_value=True)
def filter_by_read_name(in_fastq, out_fastq, keep_reads, verbose):
    # Put reads that are in the keep list in the output file
    keep_read_set = set(line.decode('ISO-8859-1').rstrip() for line in open(keep_reads, 'rb'))
    if verbose:
        print('Done loading keep read list', file=sys.stderr)

    # Loop over input and filter reads
    with open(out_fastq, 'wt') as output_file:
        with open(in_fastq, 'rt') as input_file:
            counter = 0
            for rec in SeqIO.parse(input_file, 'fastq'):
                counter += 1
                if verbose and counter % 1e5 == 0:
                    print('Processed {} reads'.format(counter))
                if rec.id in keep_read_set:
                    SeqIO.write(rec, output_file, 'fastq')

    # Print completed message
    if verbose:
        print('Completed', file=sys.stderr)


if __name__ == '__main__':
    filter_by_read_name()
