from tkinter import *
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
    bt2 = Button(bottomFrame, text="Generate Infomercial!", fg="red4")

    # put the buttons at their right positions
    bt1.pack(side=LEFT)
    bt2.pack(side=RIGHT)

def btAccRecLanClick(texto, enTex, recFrame):
    texto = enTex.get()
    print(enTex.get())
    print(texto)
    RETORNO = RunMeParserFunc(texto)
    # lbTextinho = Label(recFrame, text=RETORNO).grid(row=3, column=0, columnspan=5)
    print(RETORNO)
    textFrame = Frame(recFrame)
    textFrame.grid(row = 3)
    scr = Scrollbar(textFrame, orient=VERTICAL)
    scr.grid(row=5, column=3, sticky=E)
    texty = Text(textFrame, wrap=WORD, yscrollcommand=scr.set)
    texty.grid(row=5, sticky = NS)
    scr.config(command = texty.yview)
    texty.insert(INSERT, RETORNO)

# command for the bt1 button
def RecLangFunc(Frame1, Frame2, wind):
    Frame1.destroy()
    Frame2.destroy()

    recFrame = Frame(wind)
    recFrame.grid(row=0, column=0, columnspan=5, rowspan=8)

    labelQuestion = Label(recFrame, text="Enter your Language:")
    labelQuestion.grid(row=0, column=0, sticky=W)

    enText = Entry(recFrame, borderwidth="2")
    enText.grid(row=0, column=1)

    texto = ""
    btAccRecLan = Button(recFrame, text="OK", command=partial(btAccRecLanClick, texto, enText, recFrame))
    btAccRecLan.grid(row=0, column=2)


# create window
w = Tk()

# w.resizable(0,0) #forbid resizing

# insert a title on the window
w.title("Infomercial Generator")

# chooses the color
w["bg"] = "ghost white"

# size of the window: Pt_Br (Largura x Altura + DistEsquerda + DistTopo) -> pixels
w.geometry("1000x600+200+200")

mainFunc(w)

w.mainloop()
