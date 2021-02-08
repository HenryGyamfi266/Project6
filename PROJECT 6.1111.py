"""Author: Henry Gyamfi

  Date-Written: 11/12/2020

  Date-Modified: 11/16/2020

  Description: In this program, I created a GUI that has Buttons, a Radiogroup button, and labels.
  This code receives a gif file that is entered by the user. The code loads the file and display it to the user. There is a button which enables the user to
  change the current image of the loaded file to black and white. There is alos a butto which also displays the next gif file on the computer for the user's review.
  The color of the labels were changed to different colors, and the font sizes of some lables were also changed as well. There are buttons which displays current time
  and date. Default radioGroup button is do not display date or time.

  Variables Used:

     imagesList - gives the list of all the gif files

     self._Button1 - button for loading a file
     self._Button2 - button for changing image to black and white
     self._Button3 - button for displaying next file
     self.DateorTimeGroup - group for the radio buttons
     self._textField2 - displays the button for time
     self._textField3 - displays the button for date
     blackPixel - provides the color for black
     whitePixel - provides the color for white
     dayAndTime - connection.recv(1024)
     w    - gets image width size
     h - gets image height size

     
"""



























###from images import Image 

from breezypythongui import EasyFrame

from tkinter import *
from socket import *

import os

imagesList = [0]

currentDirectoryPath = os.getcwd()
listOfImages = os.listdir(currentDirectoryPath)
for name in listOfImages:
    if ".gif" in name:
        ###print(name)
        imagesList.append(name)

class changeImage(EasyFrame):


    def __init__(self):
    
        """Sets up the window and widgets"""
        EasyFrame.__init__(self)
      
        self._image = PhotoImage(file = "white.gif")
        self._imageLabel = self.addLabel(text="",row=1,column=0)
        self._imageLabel["image"] = self._image
        self._imageTitle = self.addLabel(text = "The Current Image", row = 0, column=0, font="Arial", foreground="red") 
       ###buttons do not work with font and color, gives me an error, only my labels work
        self._Button1 = self.addButton(text = "Load A File",
                                      row = 4, column = 0,
                                      command=self.loadAfile)
        self._Button2 = self.addButton(text = "Make Current File Black and White",
                              row =4 , column = 1,command=self.convertFile)
        self._Button3 = self.addButton(text = "Display Next File",
                              row = 4, column = 2,command=self.DisplayFile)
        self.addLabel(text = "Enter the FileName and Press the Load a File Button", row = 7, column = 0, font="Consolas", foreground="blue")
        self._textField = self.addTextField(text = "",row=8,column=0)
        
        

        self.DateorTimeGroup = self.addRadiobuttonGroup(row = 1,
                                                 column = 2, rowspan = 3 )
        ###defaultRB = self.DateorTimeGroup.addRadiobutton(text = "Display current Time")
                                    
        self.CurrentTime = self.DateorTimeGroup.addRadiobutton(text = "Display current Time", command =self.networkingTime)
        self.CurrentDate = self.DateorTimeGroup.addRadiobutton(text = "Display current Date", command = self.networkingDate)
        self.NoTimeorDate = self.DateorTimeGroup.addRadiobutton(text = "Do not display date or time", command = self.clearTheTextBoxes)
        self.DateorTimeGroup.setSelectedButton(self.NoTimeorDate)

        self._textField2 = self.addTextField(text = " ",row=1,column=1, rowspan =1)
        self._textField3 = self.addTextField(text = " ",row=2,column=1, rowspan = 2)

        self._text = self._textField.getText()
        
        
        

    def loadAfile(self):
        #image = []
        self._text = self._textField.getText()
        print(self._text)
        self._image = PhotoImage(file = self._text)
        self._imageLabel = self.addLabel(text="",row=1,column=0)
        self._imageLabel["image"] = self._image
        self._pictureThere=True
        self.showPicInfo()
        
        






    def convertFile(self):
        try:
            if self._pictureThere:
           
                # Converts the argument image to black and white
                from images import Image 
                image = Image(self._textField.getText())
                blackPixel = (0,0,0)
                whitePixel = (255,255,255)
                for y in range(image.getHeight()):
                    for x in range(image.getWidth()):
                        (r, g, b) = image.getPixel(x,y)
                        average = (r + g + b) / 3
                        if average < 128:
                            image.setPixel(x,y,blackPixel)
                        else:
                            image.setPixel(x,y,whitePixel)
                image.draw()
            else:
                print("uhhhhhhhh no image there")

        
        except Exception:
            self.messageBox(title = "ERROR", message = "THERE IS NO FILE INPUTTED. \n PLEASE ENTER A FILE NAME.")
        
            



    def DisplayFile(self):
        imagesList[0]+=1
        print (imagesList[0])
        if imagesList[0]<1 or imagesList[0]>len(imagesList)-1:
            imagesList[0]=1
        
        self.image = PhotoImage(file = imagesList[imagesList[0]])
        self._imageLabel["image"] = self.image
        return
        
    def networkingTime(self):
        from socket import socket

        self.CurrentDate.bind("<F2>", lambda event: self.clearTheTextBoxes())
               
        connection = socket()
        connection.connect(('time.nist.gov',13))
        dayAndTime= connection.recv(1024)
       
        Fields= dayAndTime.split()
        myList=[]
        for i in Fields:
            myList.append(i.decode("utf-8"))

        self._textField2.setText(myList[2])
        self._textField3.setText("")


    def networkingDate(self):
        from socket import socket

        self.CurrentDate.bind("<F2>", lambda event: self.clearTheTextBoxes())
               
        connection = socket()
        connection.connect(('time.nist.gov',13))
        dayAndTime= connection.recv(1024)
       
        Fields= dayAndTime.split()
        myList=[]
        for i in Fields:
            myList.append(i.decode("utf-8"))

        self._textField3.setText(myList[1])
        self._textField2.setText("")

    def clearTheTextBoxes(self):
        self._textField3.setText("")
        self._textField2.setText("")
        return


    def showPicInfo(self):
        from images import Image
        image= Image(self._textField.getText())
        w= image.getWidth()
        h= image.getHeight()
        print(self._textField.getText())
        print("The width is ", w)
        print("The height is ",h)     

changeImage().mainloop()

