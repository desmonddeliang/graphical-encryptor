'''
Desmond's Magical Encryptor

Version 1.0 BETA!

This program can encrypt text information to a given GIF picture
and also extract information from a GIF picture.

This program supports both type in information or read from a
text file in the same folder.

In order to use this program, you have to have a availible GIF
formatted picture in the same folder where this program is put.


'''

import image
import random


def readImage(filename = "input"):
    
    '''This function read in a given picture
    '''
    
    img = image.Image(file = filename + '.gif', title = 'IMAGE')
    return img


def transcode(text):
    
    ''' This function transcode text information to ASCII code for
    later encoding to a picture.
    '''
    
    print("Transcoding......")
    code = ""
    for i in range(len(text)):
        code = code + str(ord(text[i])) + ","

    
    code = code + "."
    colorcode = []

    for char in code:
        if char == ",":
            colorcode.append(10)
        elif char == ".":
            colorcode.append(11)
        else:
            colorcode.append(int(char))
    return colorcode


def newRGB(rgb,num):

    ''' This function takes in a RGB tuple and returns a new
    RGB tuple with a code in it based on the original tuple.
    '''

    for i in range(3): # no exceeding 255
        if rgb[i] > 249:
            rgb[i] = 240
        rgb[i] = (rgb[i] // 10) * 10

    n = [0,0,0]

    if num < 10 and num > 0:
        n[0] = random.randrange(0,num + 1)
        n[1] = random.randrange(0,num - n[0] + 1)
        n[2] = num - n[0] - n[1]
    elif num >= 10:
        n[0] = random.randrange(4,10)
        n[1] = random.randrange(0,num - n[0] + 1)
        n[2] = num - n[0] - n[1]
    elif num == 0:
        n[0] = 0
        n[1] = 0
        n[2] = 0

    ranOrders = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,1,0],[2,0,1]]
    ranOrder = ranOrders[random.randrange(0,6)]

    for i in range(3):
        rgb[ranOrder[i]] = rgb[ranOrder[i]] + n[i]
        
    return rgb

   
def encode(photo,code,filename = "output"):

    ''' This function encode the text into the picture.
    '''
    print("Encryption in process...... 0 %")
    width = photo.width()
    height = photo.height()
    maxi = len(code)
    i = 0
    totalP = (height * width) // 10
    
    for y in range(height):
        for x in range(width):
            RGB = list(photo.get(x,y))
            if i < maxi:
                RGB = newRGB(RGB,code[i])
            else:
                RGB = newRGB(RGB,random.randrange(0,10))
            
            if i % totalP == 0 and i/totalP != 0: # print 10% of progress
                print(str(int(i/totalP)) + "0 %")
                
            photo.set(x,y,tuple(RGB))
            i = i + 1
            
    print("Encryption Completed 100 %")
    print("Image Used: " + str(((maxi/(height*width))*100)//1) + " %")
    
    photo.show()
    filenameext = filename + "_encrypted.gif"
    photo.save(filenameext)
    print("Processed image is saved as " + filenameext)

def decode(photo,filename):

    ''' This function decode the photo and extract hidden information
    '''
    print("Decryption in process......")
    width = photo.width()
    height = photo.height()
    jump = False
    codes = ""
    i = 0 
    for y in range(height):
        for x in range(width):
            if jump == False:
                RGB = list(photo.get(x,y))
                code = int(RGB[0]%10 + RGB[1]%10 + RGB[2]%10)
                if code == 11:
                    jump = True
                elif code == 10:
                    codes = codes + ","
                else:
                    codes = codes + str(code)

    # start to transcode back to text
    asciicode = codes.split(",")
    text = ""
    for item in asciicode:
        if item != "":
            text = text + chr(int(item))
    print("Decryption completed!")

    filenameext = filename + "_decrypted.txt"

    file = open(filenameext, mode = 'w')
    file.write(text)
    print("The extracted information is saved as "+ filenameext)
    print("")
    print("Here is a preview of the extracted information:")
    print("-----------------")
    print("")
    print(text[:1000])
    print("")
    print("-----------------")

    
def encrypt():

    ''' A simple UI for leading user to do encryptions.
    '''
    
    print("")
    print("Do you want to type in something or just read from a file?")
    answer = input("(enter T for typing and R for reading):")
    
    while answer != "T" and answer != "R":
        answer = input("Wrong answer! Enter T for typing and R for reading!")
        
    if answer == "T":
        text = input("Type in something you want to encrypt!")
    else:
        filename = input("Please type in filename of information you want to encrypt:")
        file = open(filename + ".txt","r")
        try:
            text = file.read()
        except UnicodeDecodeError:
            print("ERROR: FILE CONTAINS ILLEGAL CHARACTER! PLEASE RESTART THE PROGRAM!")
            return None
    print("")
    photoname = input("Please type in the photo you want the information to be encrypted to: (Don't type in extensions)")
    while photoname == "":
        photoname = input("Yo! Type in a filename of a photo!!")    
    
    encode(readImage(photoname),transcode(text),photoname)


def decrypt():
    
    ''' A simple UI for leading user to do decryptions.
    '''
    
    print("")
    photoname = input("Please type in the photo you want to decrypt: (Don't type in extensions)")
    while photoname == "":
        photoname = input("Yo! Type in a filename of a photo!!")        
    decode(readImage(photoname),photoname)


def main():
    print("Welcome to Desmond's Magical Encryptor!")
    answer = input("Type E if you want to encrypt something or D to decrypt an image:")
    
    while answer != "E" and answer != "D":
        answer = input("Wrong answer! Type E if you want to encrypt something or D to decrypt an image:")
    
    if answer == "E":
        encrypt()
    else:
        decrypt()

    print("Thanks for using this program! BYEBYE~~~")


main()

