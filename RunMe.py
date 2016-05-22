#!/usr/bin/env python3

from tkinter import *
import tkinter.filedialog as fdialog
import tkinter.messagebox as messagebox
from functools import partial
import libGrammarReader
import libTextParser
import libTextGen
from libExcept import *


# main function created from RunMeParser
# uses as parameter:
#   text -> aux string
#   g -> grammar
def RunMeParserFunc(text, g):
    try:
        acc, trees = libTextParser.parseText(g, text)
        if acc:
            return 'Text accepted!' + trees
        else:
            return 'Text rejected!'
    except GrammarError:
        messagebox.showerror("Error!", "Invalid grammar!")
        return 'Invalid grammar!'


# func to send the text to the GUI
#   g -> grammar
def RunMeGenFunc(g):
    try:
        text = libTextGen.genText(g)
        return text
    except GrammarError:
        messagebox.showerror("Error!", "Invalid grammar!")
        return 'Invalid grammar!'


# main function
# window -> Tk
def mainFunc(window):
    # creates the intro Frame block
    introFrame = Frame(window)
    introFrame.pack()
    
    # create the main logo
    img = PhotoImage(file="img\\earley.gif")   # convert the Image object into a TkPhoto object
    earleyImage = Label(introFrame, image=img)    # put it in the display window
    earleyImage.pack()

    # creating the buttons objects
    bt1 = Button(introFrame, text="Recognize Language", fg="black", command=partial(RecLangFunc, introFrame, window))
    bt2 = Button(introFrame, text="Generate Infomercial!", fg="red4", command=partial(genInfomercial, introFrame, window))
    bt3 = Button(window, text = "About", command=createaboutWindow)#about button
    
    # put the buttons at their right positions
    bt1.place(x=400, y=580)
    bt2.place(x=550, y=580)
    bt3.place(x=850, y=20)
    
    introFrame.mainloop()
    
    return


# Function to return to the main screen
# Frame1 -> Frame
# window -> Tk()
def returnMainScreen(Frame1, window):
    Frame1.destroy()
    mainFunc(window)
    return


# Function to reconize the button click from the Reconize Language screen and generate the tree
def btAccRecLanClick(text, filePath, enTex, recFrame, window, showTreeArea):
    text = enTex.get()
    
    if filePath:
        tree = RunMeParserFunc(text, g)
        showTreeArea["state"] = NORMAL
        showTreeArea.delete('1.0',END)
        showTreeArea.insert(INSERT, tree)
        showTreeArea["state"] = DISABLED
        
    return


# command for the bt1 button
# Reconize Language
# Frame1 -> Frame
# Frame2 -> Frame
# window -> Tk()
def RecLangFunc(Frame1, window):
    Frame1.destroy()
    
    recFrame = Frame(window)
    recFrame.pack(fill=BOTH)
    #recFrame.grid(row=0, column=0, ipadx=600, ipady=400)
    
    recImage = Frame(recFrame)
    recImage.pack(fill=BOTH)
    
    img = PhotoImage(file="img\\background.gif")   # convert the Image object into a TkPhoto object
    backgroundImage = Label(recImage, image=img)    # put it in the display window
    backgroundImage.pack()
   
    
    labelQuestion = Label(recFrame, text="Enter your Language:",background = "AntiqueWhite1",font = "Courier 13 bold underline")
    labelQuestion.place(x=60,y=80)
    
    labelFile = Label(recFrame, text="Current file:", background = "AntiqueWhite1",font = "Courier 13 bold underline")
    labelFile.place(x=60,y=110)

    qtText = Entry(recFrame, borderwidth="2",font = "Courier 13 bold underline")
    qtText.place(x=280,y=82)
    
    filePath ={}
    fileText = Text(recFrame, borderwidth="2",height=1, width=50, font = "Courier 13 bold underline")
    fileText.place(x=200,y=112)
    fileText["state"] = DISABLED
    
    btFileOpen = Button(recFrame, text="Search", command= partial(getFilenameRec, fileText, filePath), font = "Courier 10 bold")
    btFileOpen.place(x=670,y=112,height=25)
    
    recTextArea = Frame(recFrame)
    recTextArea.place(x=70, y=140, height=410, width=820)
    scr = Scrollbar(recTextArea, orient=VERTICAL)
    #scr.grid(row=2, column=3, sticky=NS)
    scr.pack(side=RIGHT, fill=Y)
    showTreeArea = Text(recTextArea, wrap=WORD, yscrollcommand=scr.set, relief=FLAT, background = "AntiqueWhite1", font = "Courier 15 bold")
    #showTreeArea.grid(row=2, sticky = W)
    #showTreeArea.place(x=10, y=20, height=300, width=200)
    showTreeArea.pack(fill=BOTH)
    scr.config(command = showTreeArea.yview)
    
    showTreeArea.insert(INSERT, "Enter a phrase up here ↑ \n and then choose a file to parse it\n  with the Earley Parsing Algorithm!")
    
    text = ""
    btAccRecLan = Button(recFrame, text="OK", command=partial(btAccRecLanClick, text, filePath, qtText, recFrame, window, showTreeArea))
    btAccRecLan.place(x=270,y=0,height=25)
    
    btReturn = Button(recFrame, text="<", command=partial(returnMainScreen, recFrame, window))
    btReturn.place(x=1, y=1)

    recFrame.mainloop()
    return


def createaboutWindow():
    aboutWindow = Toplevel()
    aboutWindow.geometry("450x250+200+200")
    aboutWindow.title("About")
    aboutWindow.resizable(0,0)
    msg= Label(aboutWindow, text="Earley Parser v0.7\nCriado pelos alunos: \nArateus Meneses\nCaio Fonseca Rodrigues\nDaniel Kelling Brum\nGuilherme Cattani de Castro")
    msg.grid(row=0,column=0, columnspan=3)
    
    #im = Image.open('img\ufrgs.png').convert2byte()# open image and convert to byte format
    img = PhotoImage(file="img\\inf.gif")   # convert the Image object into a TkPhoto object
    infImage = Label(aboutWindow, image=img)    # put it in the display window
    infImage.grid(row=1,column=0)
    
    img2 = PhotoImage(file="img\\ufrgs.gif")   # convert the Image object into a TkPhoto object
    ufrgsImage = Label(aboutWindow, image=img2)    # put it in the display window
    ufrgsImage.grid(row=1,column=1)   
    
    aboutWindow.mainloop()


# Function to get the file
# fileText -> Text()
# filePath -> {}
def getFilenameRec(fileText, filePath):
    global g
    filePath['file'] = fdialog.askopenfile(mode='r',defaultextension='txt', title="Find the grammar to be parsed...")
    fileText["state"] = NORMAL
    fileText.delete('1.0',END)
    if filePath['file']:
        try:
            g = libGrammarReader.parseGrammarFile(filePath['file'].name)
            fileText.insert('end', filePath['file'].name)
        except ParseError as error:
            g = {}
            messagebox.showerror("Error!", error.args[0])
    else:
        fileText.insert('end', "File not found!")
    fileText["state"] = DISABLED
    return


# Function to get the file
# fileText -> Text()
# genFrame -> Frame
# filePath -> {}
# infoText -> Text()
def getFilenameGen(fileText, genFrame, filePath, infoText):
    global g
    filePath['file'] = fdialog.askopenfile(mode='r',defaultextension='txt', title="Find the grammar to be parsed...")
    fileText["state"] = NORMAL
    fileText.delete('1.0',END)
    if filePath['file']:
        try:
            g = libGrammarReader.parseGrammarFile(filePath['file'].name)
            fileText.insert('end', filePath['file'].name)
            btInfoFunc(genFrame, filePath, infoText)
        except ParseError as error:
            g = {}
            messagebox.showerror("Error!", error.args[0])
    else:
        fileText.insert('end', "File not found!")
    fileText["state"] = DISABLED
    return


# Function to generate the random infomercial
# Frame1 -> Frame
# Frame2 -> Frame
# window -> Tk()
def genInfomercial(Frame1, window):
    Frame1.destroy()

    genFrame = Frame(window)
    genFrame.grid(row=0, column=0, ipadx=600, ipady=400, rowspan=8, columnspan=10)

    labelFile = Label(genFrame, text="Current file:")
    labelFile.place(x=20,y=3)

    filePath = {}

    fileText = Text(genFrame, borderwidth="2", height=1, width=20)
    fileText.place(x=90,y=3)
    
    
    infomercialText = Text(genFrame,  wrap=WORD, height = "11", width = "81")
    infomercialText.grid(row=1, column=0)
    infomercialText.insert(INSERT, "PICK UP YOUR PHONE NOW AND CALL 1-800-EARLEY!!\n(choose a file so we can begin!)")
    
    btFileOpen = Button(genFrame, text="Search", command=partial(getFilenameGen, fileText, genFrame, filePath, infomercialText))
    btFileOpen.place(x=260, y=0)

    butThereIsMore = PhotoImage(file = "img\\More.gif")
    btInfo = Button(genFrame, command=partial(btInfoFunc, genFrame, filePath, infomercialText))
    btInfo.image = butThereIsMore
    btInfo.configure(image = butThereIsMore)
    btInfo.place(x=182, y=215)

    btReturn = Button(genFrame, text="<", command=partial(returnMainScreen, genFrame, window))
    btReturn.grid(row=0, column=0, sticky=W)

    return


# Function to show the text generator on the box Text
# genFrame -> Frame
def btInfoFunc(genFrame, filePath, infoText):
    if filePath:
        generator = RunMeGenFunc(g)
        infoText["state"] = NORMAL
        infoText.delete('1.0',END)
        infoText.insert(INSERT, generator)
        infoText["state"] = DISABLED
    return



# create window
w = Tk()

w.resizable(0,0) # forbid resizing

# insert a title on the window
w.title("Infomercial Generator")

# chooses the color
w["bg"] = "ghost white"

# size of the window: Pt_Br (Largura x Altura + DistEsquerda + DistTopo) -> pixels
w.geometry("941x621+200+200")

mainFunc(w)

w.mainloop()
