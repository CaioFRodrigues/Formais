#!/usr/bin/env python3
from tkinter import *
import tkinter.filedialog as fdialog
from functools import partial
from RunMeParserGUI import RunMeParserFunc
from libGrammarReader import parseGrammarFile
from libTextParser import parseText

def mainFunc(window):
    # creates the intro Frame block
    introFrame = Frame(window)
    introFrame.pack()

    # print the first dialog at the window
    # introLabel =
    Label(introFrame, text="Welcome to the Infomercial Generator!\nWhat would you like to do?").pack()

    # creating the bottom frame block o add the buttons
    bottomFrame = Frame(window)
    bottomFrame.pack(side=BOTTOM)

    # creating the buttons objects
    bt1 = Button(bottomFrame, text="Reconize Language", fg="black",
                 command=partial(RecLangFunc, bottomFrame, introFrame, window))
    bt2 = Button(bottomFrame, text="Generate Infomercial!", fg="red4", command=partial(genInfomercial, bottomFrame, introFrame, window))

    # put the buttons at their right positions
    bt1.pack(side=LEFT)
    bt2.pack(side=RIGHT)


def returnMainScreen(frame1, window):
    frame1.destroy()
    mainFunc(window)


def btAccRecLanClick(texto, filePath, enTex, recFrame, window):
    texto = enTex.get()
    # print(enTex.get())
    # print(texto)
    if filePath:
        RETORNO = RunMeParserFunc(texto, filePath['file'].name)
        # lbTextinho = Label(recFrame, text=RETORNO).grid(row=3, column=0, columnspan=5)
        # print(RETORNO)
        # textFrame = Frame(recFrame)
        # textFrame.grid(row = 3)

        scr = Scrollbar(recFrame, orient=VERTICAL)
        scr.grid(row=2, column=3, sticky=NS)
        texty = Text(recFrame, wrap=WORD, yscrollcommand=scr.set)
        texty.grid(row=2, sticky = W)
        scr.config(command = texty.yview)
        texty.insert(INSERT, RETORNO)
        texty["state"] = DISABLED
        
    return
    
# command for the bt1 button
def RecLangFunc(Frame1, Frame2, window):
    Frame1.destroy()
    Frame2.destroy()

    recFrame = Frame(window)
    recFrame.grid(row=0, column=0, ipadx=600, ipady=400)

    labelQuestion = Label(recFrame, text="Enter your Language:")
    labelQuestion.grid(row=0, column=0, pady=2, sticky=W)
    
    labelFile = Label(recFrame, text="Current file:")
    labelFile.grid(row=1, column=0, pady=2, sticky=W)

    enText = Entry(recFrame, borderwidth="2")
    enText.place(x=120,y=1)
    
    filePath ={}
    
    fileText = Text(recFrame, borderwidth="2",height=1, width=20)
    fileText.place(x=70,y=25)
    
    btFileOpen = Button(recFrame, text="Search", command= partial(getFilename, fileText, filePath))
    btFileOpen.place(x=225,y=20)
    
    texto = ""
    btAccRecLan = Button(recFrame, text="OK", command=partial(btAccRecLanClick, texto, filePath, enText, recFrame, window))
    btAccRecLan.place(x=245,y=0,height=20)
    
    btReturn = Button(recFrame, text="Return", command=partial(returnMainScreen, recFrame, window))
    btReturn.place(x=590, y=0)

def getFilename(fileText, filePath):
    filePath['file'] = fdialog.askopenfile(mode='r',defaultextension='txt', title="Find the gramatic to be parsed...")
    if len(filePath) > 0:
        fileText.delete('1.0',END)
        fileText.insert('end', filePath['file'].name)
    else:
        fileText.delete('1.0',END)
        fileText.insert('end', "File not found!")
    return
    
def genInfomercial(Frame1, Frame2, window):
    Frame1.destroy()
    Frame2.destroy()

    genFrame = Frame(window)
    genFrame.grid(row=0, column=0, ipadx=600, ipady=400, rowspan=8, columnspan=10)

    butThereIsMore = PhotoImage(file = "More.gif")
    btInfo = Button(genFrame)
    btInfo.image = butThereIsMore
    btInfo.configure(image = butThereIsMore)
    btInfo.place(x=2, y=210)
    # btInfo.config()

    infomercial = Text(genFrame,  wrap=WORD, height = "12", width = "81")
    infomercial.grid(row=0, column=0)

#def btInfoFunc():




# create window
w = Tk()

w.resizable(0,0) #forbid resizing

# insert a title on the window
w.title("Infomercial Generator")

# chooses the color
w["bg"] = "ghost white"

# size of the window: Pt_Br (Largura x Altura + DistEsquerda + DistTopo) -> pixels
w.geometry("660x410+200+200")

mainFunc(w)

w.mainloop()
