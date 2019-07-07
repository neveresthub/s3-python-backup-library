import argparse

parser = argparse.ArgumentParser(
    prog='digital-ocean-ss3-client',
    description="Command line script to upload files to digital ocean spaces"
)

parser.add_argument('-v', '--version', action='version', version='%(prog)s v1.0')

parser.add_argument(
    '-d', '--dir',
    help="the root directory to upload.",
    dest='dir',
    required=True
)

parser.add_argument(
    '-b', '--bucket',
    help="default='backup', if left blank ",
    dest='bucket'
)
