import sys

def main():

    try:
        with open("enable2k.txt", "r") as file:
            file1 = file.read()
    except IOError:
        sys.exit("Could not read file1")
    try:
        with open("sowpods.txt", "r") as file:
            file2 = file.read()
    except IOError:
        sys.exit("Could not read file2")
    try:
        with open("twl06.txt", "r") as file:
            file3 = file.read()
    except IOError:
        sys.exit("Could not read file3")

    try:
        with open("mydict.txt", "a") as file:
            file.write(file1)
            file.write(file2)
            file.write(file3)

    except IOError:
        sys.exit("could not append")

if __name__ == "__main__":
    main()
