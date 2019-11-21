import sys

def main():

    iso = []

    try:
        with open("portuguese-dict.txt", "r") as file:
            line = file.readline()
            while line:
                if is_isogram(line):
                    iso.append(line)
                line = file.readline()
    except IOError:
        sys.exit("Could not read file1")

    try:
        with open('portuguese-iso.txt', 'w') as file:
            file.writelines(iso)
    except IOError:
        sys.exit("could not append")

def is_isogram(word):

    # Convert the word or sentence in lower case letters.
    clean_word = word.lower()

    # Make an empty list to append unique letters
    letter_list = []

    for letter in clean_word:

        # Remove apostrophes
        if letter == "\'":
            return False

        # If letter is an alphabet then only check
        if letter.isalpha():
            if letter in letter_list:
                return False
            letter_list.append(letter)

    return True

if __name__ == '__main__':
    main()
