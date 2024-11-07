import os
from os.path import exists as file_exists, join as join_path
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-b", "--broker", help="Define MQTT Broker IP", required=True)
    parser.add_argument("-t", "--tag", help="Define MQTT Tag", required=True)
    parser.add_argument("-m", "--msg", help="Define a text message to send", required=False, default=None)
    parser.add_argument("-f", "--file", help="Define a .sigma file to send", required=False, default=None)
    parser.add_argument("-a", "--amount", help="Define the amount of messages to be send", required=False, type=int, default=1)

    args = parser.parse_args()

    if args.msg and args.file:
        print("ERROR: You can't define a message and file at the same time!")
        parser.print_help()
        exit(1)

    if not args.msg and not args.file:
        print("ERROR: Please define a message or file!")
        parser.print_help()
        exit(1)

    if args.amount < 1:
        print("ERROR: Amount can't be less then zero!")
        parser.print_help()
        exit(1)

    if args.msg:
        for i in range(args.amount):
            os.system(f"mosquitto_pub -h {args.broker} -t '{args.tag}' -m '{args.msg.strip().replace("{i}", str(i + 1))}'")
            print(f"\rExecuting SPAM: {i + 1}/{args.amount}", end='')

    else:
        if len(args.file.split('.')) < 2:
            print(f"ERROR: File '{args.file}' is not a valid .sigma file!")
            parser.print_help()
            exit(1)

        if args.file.split('.')[1] != 'sigma':
            print(f"ERROR: File '{args.file}' is not a valid .sigma file!")
            parser.print_help()
            exit(1)

        path = args.file
        if not file_exists(path):
            print(f"ERROR: File '{args.file}' dose not Exist!")
            parser.print_help()
            exit(1)

        with open(path, 'r') as f:
            lines = f.readlines()

        for i in range(args.amount):
            for line in lines:
                os.system(f"mosquitto_pub -h {args.broker} -t '{args.tag}' -m '{line.strip().replace("{i}", str(i + 1))}'")
            print(f"\rExecuting SPAM: {i + 1}/{args.amount}", end='')
    print()
