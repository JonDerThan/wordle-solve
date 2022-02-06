from string import ascii_lowercase as alphabet
from copy import deepcopy
import re, sys, getopt

wordLength = 5

def main(argv):
    wordlist0 = "./words-en.dic"

    try:
        opts, args = getopt.getopt(argv, "hl:", ["wordlist="])
    except getopt.GetoptError:
        print("usage: main.py -l <wordlist>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("usage: main.py -l <wordlist>")
            sys.exit()

        elif opt in ("-l", "--wordlist"):
            wordlist0 = arg

    if wordlist0 == "":
        print("usage: main.py -l <wordlist>")
        sys.exit(2)

    with open(wordlist0, "r") as wordlist:
        words = wordlist.read().lower()

        wordlist.close()

    possibleLetters = []

    for i in range(wordLength):
        possibleLetters.append(alphabet)

    print("Commands:\nq\tQuit.\nn\tGet number of possible words.\ns\tGet 5 suggested new words\na\tShow all possible words.\n")
    print("To register a new input use the format 01021asdfg\nasdfg:\tThe word you entered.\n01021:\tThe response you get:\n\t0:\tgrey\n\t1:\tyellow\n\t2:\tgreen\n")

    while True:
        cmd = input(">")

        if cmd == "q":
            return

        elif cmd == "n":
            print("Number of possible words: " + str(len(getPossibleWords(possibleLetters, words))))

        elif cmd == "s":
            bestWords = getBestWords(possibleLetters, words)

            out = "Suggested words:"

            for bestWord in bestWords:
                out += "\n\t" + bestWord[0] + ": " + str(bestWord[1])

            print(out)

        elif cmd == "a":
            print("Possible words:")
            print("\t" + "\n\t".join(getPossibleWords(possibleLetters, words)))

        else:
            flags = cmd[0:wordLength]
            word = cmd[wordLength:]

            for i in range(wordLength):
                flag = flags[i]
                letter = word[i]

                if flag == "0":
                    # if letter was already in this word, dont do anything
                    if not letter in word[0:i]:
                        # remove this letter from every position
                        for j in range(len(possibleLetters)):
                            possibleLetters[j] = possibleLetters[j].replace(letter, "")

                elif flag == "1":
                    # remove this letter from this position
                    possibleLetters[i] = possibleLetters[i].replace(letter, "")

                elif flag == "2":
                    # set this position to this character
                    possibleLetters[i] = letter

                else: raise RuntimeError("invalid flag: " + flag)


def getPossibleWords(possibleLetters, words):
    str = "^"

    for possibleLetter in possibleLetters:
        str += "[" + possibleLetter + "]"

    str += "$"

    regex = re.compile(str, re.MULTILINE | re.IGNORECASE)

    return regex.findall(words)

def countCharDistribution(words):
    distribution = {}

    for char in alphabet:
        distribution[char] = words.count(char)

    return distribution

def countMostUnusedChars(possibleLetters):
    mostUnusedChars = {}

    for char in alphabet:
        mostUnusedChars[char] = 0
        for pos in possibleLetters:
            if char in pos: mostUnusedChars[char] += 1

    return mostUnusedChars

def getBestWords(possibleLetters, words, count=5):
    bestWords = []

    for i in range(count):
        bestWords.append(["", -1]);

    possibleWords = getPossibleWords(possibleLetters, words)
    mostUnusedChars = countMostUnusedChars(possibleLetters)
    charDistribution = countCharDistribution("".join(possibleWords))

    for word in possibleWords:
        score = 0
        for i in range(len(word)):
            char = word[i]

            if not char in word[0:i]:
                # arbitrary, change as needed
                score += mostUnusedChars[char] / wordLength + charDistribution[char] / len(possibleWords)

        for i in range(count):
            if score > bestWords[i][1]:
                bestWords[i] = [word, score]
                break

    bestWords.sort(reverse=True, key=lambda pair: pair[1])

    bestWords2 = []
    for i in range(count):
        if bestWords[i][1] != -1: bestWords2.append([bestWords[i][0], round(bestWords[i][1], 2)])

    return bestWords2

if __name__ == '__main__':
    main(sys.argv[1:])
