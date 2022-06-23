import argparse

parser = argparse.ArgumentParser(
    description='Process app functional arguments')

parser.add_argument('--period', type=str,
                    help='period being processed eg. CCYYMMDD')
parser.add_argument('--distributor', type=str,
                    help='distributor being processed eg. CARDINAL, MCKESSON, etc.')
parser.add_argument('--file_path', type=str,
                    help='file_path to file to process eg. $env:USERPROFILE\Downloads\*.xlsx')
parser.add_argument('--fields_file', type=str,
                    help='fields_file with mapping info for distributor tracings')
