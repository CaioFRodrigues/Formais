from tkinter import *
from functools import partial
import copy
from RunMeParserGUI import RunMeParserFunc
from libGrammarReader import parseGrammarFile
from libTextParser import parseText

def btAccRecLanClick(texto, enTex, recFrame):
    texto = enTex.get()
    print(enTex.get())
    print(texto)
    RETORNO = RunMeParserFunc(texto)
    lbTextinho = Label(recFrame, text = RETORNO).grid(row=3, column = 0, columnspan = 5)
    print(RETORNO)


# command for the bt1 button
def RecLangFunc(Frame1, Frame2, wind):
    Frame1.destroy()
    Frame2.destroy()

    recFrame = Frame(wind)
    recFrame.grid(row = 0, column = 0, columnspan= 20)

    labelQuestion = Label(recFrame, text = "Enter your Language:")
    labelQuestion.grid(row=0, column=0, sticky=W, columnspan=4)

    enText = Entry(recFrame)
    enText.grid(row=0, column=5, columnspan = 8)

    texto = ""
    btAccRecLan = Button(recFrame, text = "OK", command = partial(btAccRecLanClick, texto, enText, recFrame))
    btAccRecLan.grid(row=0, column = 14)


# main function
def mainFunc():
    # create window
    window = Tk()

    # insert a title on the window
    window.title("Infomercial Generator")

    # chooses the color
    window["bg"] = "ghost white"

    # size of the window: Pt_Br (Largura x Altura + DistEsquerda + DistTopo) -> pixels
    window.geometry("600x400+200+200")

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
    bt1 = Button(bottomFrame, text = "Reconize Language", fg="black", command = partial(RecLangFunc, bottomFrame, introFrame, window))
    bt2 = Button(bottomFrame, text = "Generate Infomercial!", fg="red4")

    # put the buttons at their right positions
    bt1.pack(side=LEFT)
    bt2.pack(side=RIGHT)

    # main loop
    window.mainloop()




mainFunc()