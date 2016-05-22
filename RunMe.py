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
    bt1 = Button(introFrame, relief = GROOVE, font = "Courier 13 bold", text="Recognize Language", fg="black", command=partial(WindowParse, introFrame, window))
    bt2 = Button(introFrame, relief = GROOVE, font = "Courier 13 bold", text="Generate Infomercial!", fg="red4", command=partial(WindowGen, introFrame, window))
    bt3 = Button(window, relief = GROOVE, font = "Courier 12 bold", text="About", command=WindowAbout)

    # put the buttons at their right positions
    bt1.place(x=390, y=560)
    bt2.place(x=600, y=560)
    bt3.place(x=835, y=15)

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

    #destroys previous window
    frame.destroy()
    
    #makes a new frame for the widgets
    recFrame = Frame(window)
    recFrame.pack(fill=BOTH)
    
    #makes a new frame for the image
    recImage = Frame(recFrame)
    recImage.pack(fill=BOTH)
    
    #creates widget and assign image to it
    img = PhotoImage(file="img\\background.gif")   # convert the Image object into a TkPhoto object
    backgroundImage = Label(recImage, image=img)    # put it in the display window
    backgroundImage.pack()
   
   #create label for the current file and selects the style options
    labelFile = Label(recFrame, text="Current file:", background = "AntiqueWhite1", font = "Courier 13 bold underline")
    labelFile.place(x=60,y=110)
    
    #create text box that will show the file path
    fileText = Text(recFrame, borderwidth="2",height=1, width=46, font = "Courier 13 bold", selectbackground= "coral1")
    fileText.place(x=200,y=112)
    #disables it so the user can't write what they want, a search function will be provided
    fileText["state"] = DISABLED
    
    #creates the search button
    btFileOpen = Button(recFrame, text="Search",relief = GROOVE, command= partial(DialogGrammarParse, fileText), font = "Courier 10 bold")
    btFileOpen.place(x=668,y=112,height=25)
    
    #creates the text area frame that will be called by other functions to show the result
    recTextArea = Frame(recFrame)
    recTextArea.place(x=70, y=145, height=410, width=824)
    
    #put the scroll bar filling the right side of the frame
    scr = Scrollbar(recTextArea, orient=VERTICAL)
    scr.pack(side=RIGHT, fill=Y)
    
    #creates the actual text area
    showTreeArea = Text(recTextArea, wrap=WORD, yscrollcommand=scr.set, relief=FLAT, background = "AntiqueWhite1", font = "Courier 15 bold", selectbackground= "coral1")
    showTreeArea.pack(fill=BOTH)
    showTreeArea.insert(INSERT, "Enter a phrase up here ↑ \n and then choose a file to parse it\n  with the Earley Parsing Algorithm!!")
    #disables it so the user don't write what they want, only the program will
    showTreeArea["state"] = DISABLED

    #configures the scroll to work in the text area frame
    scr.config(command = showTreeArea.yview)
    
    #the same that was done with the current file label
    labelQuestion = Label(recFrame, text="Enter your Language:",background = "AntiqueWhite1",font = "Courier 13 bold underline")
    labelQuestion.place(x=60,y=80)
    
    #creates a new entry for the end user to enter with a valid or invalid text
    qtText = Entry(recFrame,width=20, borderwidth="2",font = "Courier 13 bold", selectbackground= "coral1")
    qtText.place(x=272,y=82)  
    
    #creates a null string to be used as a pointer
    text = ""
    #creates the button that will handle getting the current file and parsing the user entered text
    btAccRecLan = Button(recFrame, text="OK",relief = GROOVE, command=partial(ActionParse, qtText, showTreeArea), font = "Courier 13 bold")
    btAccRecLan.place(x=480,y=82,height=25)
    
    #the return button
    btReturn = Button(recFrame, text="←",relief = GROOVE, command=partial(ActionGotoMain, recFrame, window),font = "Courier 15 bold")
    btReturn.place(x=55, y=39)

    #this is only necessary in the Windows platform, and it makes images persistent
    recFrame.mainloop()


def DialogGrammarParse(fileText):
    """
    File open dialog for the text recognition window

    Keyword arguments:
        fileText = Text
    """

    global g

    #calls tkinters filedialog that will handle the search for a new file
    filePath = fdialog.askopenfile(mode='r', defaultextension='txt', title="Find the grammar to be parsed...")
    filename = filePath.name
    
    #try parsing the file
    try:
        g = libGrammarReader.parseGrammarFile(filename)
        fileText["state"] = NORMAL
        fileText.delete('1.0', END)
        fileText.insert('end', filename)
        fileText["state"] = DISABLED

    #returns the right error from the exception class if something goes wrong  
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

    #try parsing the text
    try:
        inText = inputArea.get()
        acc, trees = libTextParser.parseText(g, inText)

        if acc:
            outText = 'Text accepted!' + trees
        else:
            outText = 'Text rejected!'

        #puts the resulting tree in the text area
        outputArea["state"] = NORMAL
        outputArea.delete('1.0', END)
        outputArea.insert(INSERT, outText)
        outputArea["state"] = DISABLED

    #returns the right error from the exception class if something goes wrong  
    except GrammarError:
        messagebox.showerror("Error!", "Invalid grammar!")


def WindowGen(frame, window):
    """
    Text generation window

    Keyword arguments:
        frame = Frame
        window = Tk
    """

    #destroys previous window
    frame.destroy()

    #makes a new frame for the widgets
    genFrame = Frame(window)
    genFrame.pack(fill=BOTH)
    
    #makes a new frame for the image
    recImage = Frame(genFrame)
    recImage.pack(fill=BOTH)
    
    #creates widget and assign image to it
    img = PhotoImage(file="img\\background.gif")   # convert the Image object into a TkPhoto object
    backgroundImage = Label(recImage, image=img)    # put it in the display window
    backgroundImage.pack()
    
   #create label for the current file and selects the style options
    labelFile = Label(genFrame, text="Current file:", background = "AntiqueWhite1",font = "Courier 13 bold underline")
    labelFile.place(x=60,y=80)

    #create text box that will show the file path
    fileText = Text(genFrame, borderwidth="2",height=1, width=46, font = "Courier 13 bold", selectbackground= "coral1")
    fileText.place(x=200,y=82)
    #disables it so the user can't write what they want, a search function will be provided
    fileText["state"] = DISABLED
    
    #creates the text area frame that will be called by other functions to show the result
    recTextArea = Frame(genFrame)
    recTextArea.place(x=70, y=140, height=230, width=820)
    
    #put the scroll bar filling the right side of the frame
    scr = Scrollbar(recTextArea, orient=VERTICAL)
    scr.pack(side=RIGHT, fill=Y)
    
    #creates the actual text area
    infomercialText = Text(recTextArea, wrap=WORD, yscrollcommand=scr.set, relief=FLAT, background = "AntiqueWhite1", font = "Courier 17 bold", selectbackground= "coral1")
    infomercialText.pack(fill=BOTH)
    infomercialText.insert(INSERT, "PICK UP YOUR PHONE NOW AND CALL 1-800-EARLEY!!\n(choose a file so we can begin!)")
    #disables it so the user don't write what they want, only the program will
    infomercialText["state"] = DISABLED
    
    #configures the scroll to work in the text area frame
    scr.config(command = infomercialText.yview)
    
    #creates the search button
    btFileOpen = Button(genFrame, text="Search", command=partial(DialogGrammarGen, fileText, infomercialText))
    btFileOpen.place(x=668,y=82,height=25)

    #creates the butwait!! image and makes it a button
    butThereIsMore = PhotoImage(file = "img\\butwait.gif")
    btInfo = Button(genFrame, relief=GROOVE, command=partial(ActionGen, infomercialText))
    btInfo.image = butThereIsMore
    btInfo.configure(image = butThereIsMore)
    btInfo.place(x=260, y=380)

    #the return button
    btReturn = Button(genFrame, text="←",relief = GROOVE, command=partial(ActionGotoMain, genFrame, window),font = "Courier 15 bold")
    btReturn.place(x=55, y=39)

    #this is only necessary in the Windows platform, and it makes images persistent
    genFrame.mainloop()


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
    
    #creates the about window as a top level widget
    aboutWindow = Toplevel()
    aboutWindow.geometry("440x280+600+150")
    aboutWindow.title("About")
    aboutWindow.resizable(0, 0)
    msg= Label(aboutWindow,font = "Courier 13 bold", text="Earley Parser v0.8\nCriado pelos alunos: \nArateus Meneses\nCaio Fonseca Rodrigues\nDaniel Kelling Brum\nGuilherme Cattani de Castro")
    msg.grid(row=0,column=0, columnspan=3)

    #INF image
    img = PhotoImage(file="img/inf.gif")
    infImage = Label(aboutWindow, image=img)
    infImage.grid(row=1, column=0)

    #UFRGS image
    img2 = PhotoImage(file="img/ufrgs.gif")
    ufrgsImage = Label(aboutWindow, image=img2)
    ufrgsImage.grid(row=1, column=1)   

    aboutWindow.mainloop()


# global grammar
g = {}

# create window
w = Tk()
w.resizable(0, 0) # prevent resizing
w.title("The Amazing Earley Parsing Machine!")
w["bg"] = "ghost white"
w.geometry("941x621+200+200") # (width x height + leftMargin + topMargin) in pixels
WindowMain(w)

w.mainloop()
