#!python

import os
import sys
import argparse


def create_link(src, dst, hard, override):
    if override and os.path.exists(dst):
        os.remove(dst)

    if hard:
        os.link(src, dst)
    else:
        os.symlink(src, dst)


def main():

    parser = argparse.ArgumentParser(description='Create a directory with symbolic links to files in another directory')
    parser.add_argument('inputdir', help='Input directory')
    parser.add_argument('outputdir', help='Output directory')
    parser.add_argument('--stride', type=int, default=1, help="Only create a symlink for every n'th file where n is this parameter")
    parser.add_argument('--offset', type=int, default=0, help='Start with a certain offset')
    parser.add_argument('--hard', action='store_true', help="Create hardlinks instead of softlinks")
    parser.add_argument('--force', action='store_true', help="Force override if link already exists")

    args = parser.parse_args()

    filenames = sorted(os.listdir(args.inputdir))

    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    for i in range(args.offset, len(filenames), args.stride):
        create_link(os.path.join(args.inputdir, filenames[i]), os.path.join(args.outputdir, filenames[i]), args.hard, args.force)

if __name__ == '__main__':
    main()
