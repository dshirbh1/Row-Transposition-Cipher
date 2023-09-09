import sys
import re
import os

#Pattern to match the name of input file as an argument
pattern = r'^[a-z0-9]+$'

#keylength: the length of the key (e.g., 6)
keyLength = int(sys.argv[1])
#key: the key used for encryption and decryption (e.g., 315462)
key = sys.argv[2]
keyList = list()
for c in key:
    keyList.append(int(c))
#inputfile: input file name (e.g., input)
inputFile = sys.argv[3]
#outputfile: output file name (e.g., output)
outputFile = sys.argv[4]
#enc/dec: encryption/decryption
encDec = sys.argv[5]


if __name__ == "__main__":
    #Check the condition of <keylength> must match the length of <key>
    if keyLength != len(keyList):
        raise ValueError("Key Length is not equal to number of keys")
    
    #Check the condition <key> must include all digits from 1 to <keylength> with each digit occurring exactly once
    for i in range(1, keyLength):
        if i not in keyList:
            raise ValueError("Not all the digits from 1 to key length are included in the key")

    #Check the condition <inputfile> must contain only lowercase letters (a-z) or digits (0-9)
    if not re.match(pattern, inputFile):
        raise ValueError("Input file name contains other characters than a-z and 0-9")
    
    #Read the input file here
    try:
        with open(inputFile, 'r') as file:
            #Read the text from the file
            text = file.read()
    
    #Handle exception
    except:
        raise ValueError("File is not present or not openeing")
    
    #Encryption
    if encDec == "enc":
        #Append extra z to the text here
        if len(text) % keyLength != 0:
            text = text + "".join(['z'] * (keyLength - (len(text) % keyLength)))
            
        #Calculate the number of rows to be in the cipher text
        row = len(text) // keyLength

        #Create a 2D array to make a cipher eventually
        text_2D = list()
        for i in range(row):
            rowContent = list(text[i*keyLength:(i*keyLength + keyLength)])
            text_2D.append(rowContent)

        #Create a cipher text from the arranged a plain text
        cypherText = ""
        for key in keyList:
            colContent = list()
            for r in range(0, row):
                colContent.append(text_2D[r][key-1])
            cypherText = cypherText + "".join(colContent)

        #Write it to outputFile
        with open(outputFile, 'w') as file:
            file.write(cypherText)

        print("Obtained cipher text with fillers is ", cypherText)

    #Decryption
    elif encDec == "dec":
        col = len(text) // keyLength

        #Create a 2D array to make a cipher eventually
        cipher_2D = list()
        for i in range(keyLength):
            colContent = list(text[i*col:(i*col + col)])
            cipher_2D.append(colContent)

        #Rearrange the ciphertext accoring to keys
        plainText = [0] * keyLength
        index = 0
        for key in keyList:
            rowContent = list()
            for r in range(0, col):
                rowContent.append(cipher_2D[index][r])
            plainText[key - 1] = rowContent
            index += 1

        #Read the whole text in one go and save it to outputFile
        plainText_modified = ""
        for c in range(col):
            for key in range(keyLength):
                plainText_modified = plainText_modified + plainText[key][c]

        #Write it to outputFile
        with open(outputFile, 'w') as file:
            file.write(plainText_modified)

        print("Obtained plain text with fillers is ", plainText_modified)
