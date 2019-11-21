import sys
import sqlite3

file = "jotto-db"
conn = sqlite3.connect(file)
c = conn.cursor()

def main():

    iso = []
    try:
        with open("indonesian-iso.txt", "r") as file:
            line = file.readline()
            while line:
                iso.append(line)
                line = file.readline()
    except IOError:
        sys.exit("Could not read file1")


    for words in iso:
        words = words.decode("utf-8")
        sql = "INSERT INTO indonesian (word, length) VALUES (?, ?)"
        val = (words, len(words))
        c.execute(sql, val)

if __name__ == '__main__':
    main()
    conn.commit()
    conn.close()
