#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Imports
import numpy as np 
import re
alphabet = "abcdefghijklmnopqrstuvwxyz"
cipheralphabet = "dguasmzerbcihvypkxqntfwloj"
letterIndex = dict(zip(alphabet, range(len(alphabet))))
indexLetter = dict(zip(range(len(alphabet)), alphabet))
cipherLetterIndex = dict(zip(cipheralphabet, range(len(cipheralphabet))))
indexCipherLetter = dict(zip(range(len(cipheralphabet)), cipheralphabet))


# In[2]:


#Letter frequencies 
freqList = []
Defaultfrequency = dict(zip(range(0,26),"etaoinsrhldcumfpgwybvkxjqz"))
freqList.append(Defaultfrequency)
OXfrequency = dict(zip(range(0,26),"eariotnslcudpmhgbfywkvxzjq"))
freqList.append(OXfrequency)
PressReport = dict(zip(range(0,26),"etaonisrhldcmufpgwybvkjxqz"))
freqList.append(PressReport)
ReligionFreq = dict(zip(range(0,26),"etiaonsrhldcumfpywgbvkxjqz"))
freqList.append(ReligionFreq)
ScientificFreq = dict(zip(range(0,26),"etaionsrhlcdumfpgybwvkxqjz"))
freqList.append(ScientificFreq)
WordAvFreq = dict(zip(range(0,26),"etaoinsrhldcumfpgwybvkxjqz"))
freqList.append(WordAvFreq)
WikiFreq = dict(zip(range(0,26),"etaoinshrdlcumwfgypbvkjxqz"))
freqList.append(WikiFreq)
FictionFreq = dict(zip(range(0,26),"etaohnisrdluwmcgfypvkbjxzq"))
freqList.append(FictionFreq)
Nonplurar = dict(zip(range(0,26),"eairtonslcupmdhgbyfvwkxzqj"))
freqList.append(Nonplurar)
plural = dict(zip(range(0,26),"eisarntolcdugpmhbyfvkwzxjq"))
freqList.append(plural)


# In[3]:


#Extended euclidean algorithm 
#Recursive function 
#FIX THE EXTENDED EUCLIDEAN ALGORITHM
def gcdExtended(a, b): 
    if a == 0 : 
        return b,0,1
    gcd,x1,y1 = gcdExtended(b%a, a) 
    # Update x and y using results of recursive 
    x = y1 - (b//a) * x1 
    y = x1 
    return gcd,x,y 


# In[4]:


#Matrix inverse
def matrixInverse(matrix, modulus):
    #Using linear algebra in the numpy library we find the determinant of the matrix
    det = int(np.round(np.linalg.det(matrix)))
    #Find the inverse of the derminant using the extended euclidean algorithm
    detInv = gcdExtended(det, modulus)[1] % modulus
    #Multipy the inverse determinat by the inverse of the matrix 
    matrixInverse = detInv * np.round(det*np.linalg.inv(matrix)).astype(int) % modulus
    return matrixInverse


# In[5]:


def hillmessageformat(message):
    message = message.replace(" ", "")
    message = re.sub(r'[^\w\s]', '', message) 
    message = message.lower()
    return message


# In[6]:


def hillEncrypt(ciphertext, key):
    plaintext = ""
    messageInNumbers = []

     #Make the letters into a number equivalent 
    for letter in ciphertext:
        messageInNumbers.append(letterIndex[letter])

    #Split the message into the size of the matrix
    split = [
        messageInNumbers[i : i + int(key.shape[0])]
        for i in range(0, len(messageInNumbers), int(key.shape[0]))
    ]

    for P in split:
         #This matrix to be a column matrix
        P = np.transpose(np.asarray(P))[:, np.newaxis]

        while P.shape[0] != key.shape[0]:
            P = np.append(P, letterIndex["x"])[:, np.newaxis]

        numbers = np.dot(key, P) % len(alphabet)
        n = numbers.shape[0]  # length of encrypted message (in numbers)

        # Map back to get encrypted text
        for index in range(n):
            number = int(numbers[index, 0])
            plaintext += indexLetter[number]

    return plaintext


# In[7]:


def hillDecrypt(ciphertext, inverseKey):
    plaintext = ""
    cipherNumbers = []

    #Convert numbers to letter equivalent
    for letter in ciphertext:
        cipherNumbers.append(letterIndex[letter])

    #Split the letters into the groups of the matrix size
    split = [
        cipherNumbers[i : i + int(inverseKey.shape[0])]
        for i in range(0, len(cipherNumbers), int(inverseKey.shape[0]))
    ]

    #Iterate through each portions of the text and decrypt using the inverse cipher key 
    for S in split:
        #Np.newaxis is used to make the matrix size the same
        S = np.transpose(np.asarray(S))[:, np.newaxis]
        numbers = np.dot(inverseKey, S) % len(alphabet)
        n = numbers.shape[0]

        #Mapping the numbers back to letters 
        for idx in range(n):
            number = int(numbers[idx, 0])
            plaintext += indexLetter[number]

    return plaintext


# In[8]:


#function to format string
def messageformat(message):
    message = re.sub(r'[^\w\s]', '', message) 
    message = message.lower()
    return message


# In[9]:


#Monoalphabetic encryption using a encryption key predefined
def monoalphabeticEncryption(plaintext):
    ciphertext = ""
    for letter in plaintext:
        if(letter != " "):
            letternumber =letterIndex[letter]
            ciphertext += indexCipherLetter[letternumber]
        else:
            ciphertext += " "
    return ciphertext


# In[10]:


#Monoalphabetic decryption using a encryption key predefined
def monoalphabeticDecryption(ciphertext):
    plaintext = ""
    for letter in ciphertext:
        if(letter != " "):
            letternumber = cipherLetterIndex[letter]
            plaintext += indexLetter[letternumber]
        else:
            plaintext += " "
    return plaintext


# In[12]:


def frequencySubstitution(message, frequency, sortedFrequency):
    deciphered = ""
    comparisonDict = {}
    #Creates dictionary that has mapped the most frequent characters with a frequency dict
    for value, char in sortedFrequency.items():
        comparisonDict[char] = frequency[value]

    #Goes through letter by letter mapping out characters
    for letter in message:
        if(letter != " "):
            deciphered += comparisonDict[letter]
        else:
            deciphered += " "
    return deciphered
    


# In[13]:


#Maps out the most frequent characters in the string
def frequencyAttack(ciphertext, noofattacks):
    letterFrequency = {}
    letterRanking = {}
    resultingMessages = []
    for letter in ciphertext:
        if(letter != " "):
            if letter not in letterFrequency:
                letterFrequency[letter] = 1
            else:
                letterFrequency[letter] += 1

    #Sorts the characters by most values 
    sortedFrequency = {k: v for k, v in sorted(letterFrequency.items(), reverse=True, key=lambda  item: item[1])}
    #Assigns ranks to characters (ie e:0 etc)
    rank = 0
    for letter in sortedFrequency:
        letterRanking[rank] = letter
        rank += 1
    
    print("IN CIPHERTEXT:", ciphertext)
    print("LETTER RANKING:", letterRanking)
    for freq in range(0, noofattacks):
        resultingMessages.append(frequencySubstitution(ciphertext, freqList[freq], letterRanking))
        
    return resultingMessages
    


# In[14]:


def printPlainCipherFreq(plaintext, ciphertext, freqtext):
    for freq in freqtext:
        print("plaintext:",plaintext)
        print("ciphertext:",ciphertext)
        print("frequency analysed:",freq)
        print("----------------------------------------------------------------------")


# In[24]:


def main():
    message = input("Enter your message: ") 
    hillmessage = hillmessageformat(message)
    message = messageformat(message)
    #ENCRYPTION CIPHER
    key = np.array([[3,3], [2,5]])
    keyinverse = matrixInverse(key, len(alphabet))
    print("ENCRYPTING MESSAGE WITH HILL CIPHER")
    ciphertext = hillEncrypt(hillmessage, key)
    print("ENCRYPTED", ciphertext)
    print("DECRYPTING MESSAGE WITH HILL CIPHER")
    plaintext = hillDecrypt(ciphertext, keyinverse)
    print("ENCRYPTED", plaintext)
    
    print("----------------FREQUENCY ATTACK------------------")
    #FRQ ATTACKS
    noofattacks = input("How many frequency attacks to perform: ") 
    if(noofattacks.isalpha()):
        print("INCORRECT INPUT DEFAULTING TO 9")
        noofattacks = 9
    if(int(noofattacks) < 0 or int(noofattacks) > 9):
        print("INCORRECT INPUT DEFAULTING TO 10")
        noofattacks = 9
    noofattacks = int(noofattacks)    
    ciphertext =  monoalphabeticEncryption(message)
    plaintext = monoalphabeticDecryption(ciphertext)
    freqMsg = frequencyAttack(ciphertext, noofattacks)
    printPlainCipherFreq(plaintext, ciphertext, freqMsg)
    
    


# In[25]:


main()


# In[ ]:




