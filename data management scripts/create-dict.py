import sys
import re

def main():

    dict = []

    try:
        with open("portuguese.txt", "r") as file:
            line = file.readline()
            while line:
                line = re.sub('[0-9]', '', line)
                line = line.strip(' ')
                dict.append(line)
                line = file.readline()

    except IOError:
        sys.exit("Could not read file1")

    try:
        with open("portuguese-dict.txt", "a") as file:
            file.writelines(dict)
    except IOError:
        sys.exit("could not append")

if __name__ == "__main__":
    main()
