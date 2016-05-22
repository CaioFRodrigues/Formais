#!/usr/bin/env python3

from tkinter import *
import tkinter.filedialog as fdialog
import tkinter.messagebox as messagebox
from functools import partial
import libGrammarReader
import libTextParser
import libTextGen
from libExcept import *


def WindowMain(window):
    """
    Main window

    Keyword arguments:
        window = Tk
    """

    # creates the intro Frame block
    introFrame = Frame(window)
    introFrame.pack()

    # create the main logo
    img = PhotoImage(file="img/earley.gif")
    earleyImage = Label(introFrame, image=img)
    earleyImage.pack()

    # creating the buttons objects
    bt1 = Button(introFrame, text="Recognize Language", fg="black", command=partial(WindowParse, introFrame, window))
    bt2 = Button(introFrame, text="Generate Infomercial!", fg="red4", command=partial(WindowGen, introFrame, window))
    bt3 = Button(window, text="About", command=WindowAbout)

    # put the buttons at their right positions
    bt1.place(x=400, y=580)
    bt2.place(x=550, y=580)
    bt3.place(x=850, y=20)

    introFrame.mainloop()


def ActionGotoMain(frame, window):
    """
    Return to the main window

    Keyword arguments:
        frame = Frame
        window = Tk
    """

    frame.destroy()
    WindowMain(window)


def WindowParse(frame, window):
    """
    Text recognition window

    Keyword arguments:
        frame = Frame
        window = Tk
    """

    frame.destroy()

    recFrame = Frame(window)
    recFrame.pack(fill=BOTH)

    recImage = Frame(recFrame)
    recImage.pack(fill=BOTH)

    img = PhotoImage(file="img/background.gif")
    backgroundImage = Label(recImage, image=img)
    backgroundImage.pack()

    labelQuestion = Label(recFrame, text="Enter your Language:", background="AntiqueWhite1", font="Courier 13 bold underline")
    labelQuestion.place(x=60,y=80)

    labelFile = Label(recFrame, text="Current file:", background="AntiqueWhite1", font="Courier 13 bold underline")
    labelFile.place(x=60,y=110)

    qtText = Entry(recFrame, borderwidth="2", font="Courier 13 bold underline")
    qtText.place(x=280,y=82)

    fileText = Text(recFrame, borderwidth="2", height=1, width=50, font="Courier 13 bold underline")
    fileText.place(x=200, y=112)
    fileText["state"] = DISABLED

    btFileOpen = Button(recFrame, text="Search", command=partial(DialogGrammarParse, fileText), font="Courier 10 bold")
    btFileOpen.place(x=670, y=112, height=25)

    recTextArea = Frame(recFrame)
    recTextArea.place(x=70, y=140, height=410, width=820)
    scr = Scrollbar(recTextArea, orient=VERTICAL)
    scr.pack(side=RIGHT, fill=Y)
    showTreeArea = Text(recTextArea, wrap=WORD, yscrollcommand=scr.set, relief=FLAT, background="AntiqueWhite1", font="Courier 15 bold")
    showTreeArea.pack(fill=BOTH)
    scr.config(command=showTreeArea.yview)

    showTreeArea.insert(INSERT, "Enter a phrase up here ↑ \n and then choose a file to parse it\n  with the Earley Parsing Algorithm!")

    btAccRecLan = Button(recFrame, text="OK", command=partial(ActionParse, qtText, showTreeArea))
    btAccRecLan.place(x=270, y=0, height=25)

    btReturn = Button(recFrame, text="<", command=partial(ActionGotoMain, recFrame, window))
    btReturn.place(x=1, y=1)

    recFrame.mainloop()


def DialogGrammarParse(fileText):
    """
    File open dialog for the text recognition window

    Keyword arguments:
        fileText = Text
    """

    global g

    filePath = fdialog.askopenfile(mode='r', defaultextension='txt', title="Find the grammar to be parsed...")
    filename = filePath.name

    try:
        g = libGrammarReader.parseGrammarFile(filename)
        fileText["state"] = NORMAL
        fileText.delete('1.0', END)
        fileText.insert('end', filename)
        fileText["state"] = DISABLED

    except ParseError as error:
        g = {}
        messagebox.showerror("Error!", error.args[0])


def ActionParse(inputArea, outputArea):
    """
    Parse the text currently in the input field with the loaded grammar

    Keyword arguments:
        inputArea = text input with the phrase to be parsed
        outputArea = text area to display the results
    """

    global g

    try:
        inText = inputArea.get()
        acc, trees = libTextParser.parseText(g, inText)

        if acc:
            outText = 'Text accepted!' + trees
        else:
            outText = 'Text rejected!'

        outputArea["state"] = NORMAL
        outputArea.delete('1.0', END)
        outputArea.insert(INSERT, outText)
        outputArea["state"] = DISABLED

    except GrammarError:
        messagebox.showerror("Error!", "Invalid grammar!")


def WindowGen(frame, window):
    """
    Text generation window

    Keyword arguments:
        frame = Frame
        window = Tk
    """

    frame.destroy()

    genFrame = Frame(window)
    genFrame.grid(row=0, column=0, ipadx=600, ipady=400, rowspan=8, columnspan=10)

    labelFile = Label(genFrame, text="Current file:")
    labelFile.place(x=20, y=3)

    fileText = Text(genFrame, borderwidth="2", height=1, width=20)
    fileText.place(x=90, y=3)

    infomercialText = Text(genFrame,  wrap=WORD, height = "11", width = "81")
    infomercialText.grid(row=1, column=0)
    infomercialText.insert(INSERT, "PICK UP YOUR PHONE NOW AND CALL 1-800-EARLEY!!\n(choose a file so we can begin!)")

    btFileOpen = Button(genFrame, text="Search", command=partial(DialogGrammarGen, fileText, infomercialText))
    btFileOpen.place(x=260, y=0)

    img = PhotoImage(file = "img/more.gif")
    btInfo = Button(genFrame, command=partial(ActionGen, infomercialText))
    btInfo.image = img
    btInfo.configure(image=img)
    btInfo.place(x=182, y=215)

    btReturn = Button(genFrame, text="<", command=partial(ActionGotoMain, genFrame, window))
    btReturn.grid(row=0, column=0, sticky=W)


def DialogGrammarGen(fileText, infoText):
    """
    File open dialog for the text generation window

    Keyword arguments:
        fileText = Text
        infoText = Text
    """

    global g

    filePath = fdialog.askopenfile(mode='r', defaultextension='txt', title="Find the grammar to be parsed...")
    filename = filePath.name

    try:
        g = libGrammarReader.parseGrammarFile(filename)
        fileText["state"] = NORMAL
        fileText.delete('1.0', END)
        fileText.insert('end', filename)
        ActionGen(infoText)
        fileText["state"] = DISABLED

    except ParseError as error:
        g = {}
        messagebox.showerror("Error!", error.args[0])


def ActionGen(infoText):
    """
    Generate a valid text from a grammar

    Keyword arguments:
        infoText = Text
    """

    global g

    try:
        genText = libTextGen.genText(g)
        infoText["state"] = NORMAL
        infoText.delete('1.0', END)
        infoText.insert(INSERT, genText)
        infoText["state"] = DISABLED

    except GrammarError:
        messagebox.showerror("Error!", "Invalid grammar!")


def WindowAbout():
    """
    About window

    Keyword arguments:
        frame = Frame
        window = Tk
    """

    aboutWindow = Toplevel()
    aboutWindow.geometry("450x250+200+200")
    aboutWindow.title("About")
    aboutWindow.resizable(0, 0)
    msg = Label(aboutWindow, text="Earley Parser v0.7\nCriado pelos alunos: \nArateus Meneses\nCaio Fonseca Rodrigues\nDaniel Kelling Brum\nGuilherme Cattani de Castro")
    msg.grid(row=0,column=0, columnspan=3)

    img = PhotoImage(file="img/inf.gif")
    infImage = Label(aboutWindow, image=img)
    infImage.grid(row=1, column=0)

    img2 = PhotoImage(file="img/ufrgs.gif")
    ufrgsImage = Label(aboutWindow, image=img2)
    ufrgsImage.grid(row=1, column=1)   

    aboutWindow.mainloop()


# global grammar
g = {}

# create window
w = Tk()
w.resizable(0, 0) # prevent resizing
w.title("Infomercial Generator")
w["bg"] = "ghost white"
w.geometry("941x621+200+200") # width x height + leftMargin + topMargin) -> px
WindowMain(w)
w.mainloop()
