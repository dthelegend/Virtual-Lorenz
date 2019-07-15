#Import Town
import keyboard
from tkinter import *
from random import randint as r, seed as seed

#Using a random seed to make sure wheel generation is always the same
seed(75434390)

#Indicates State of Figure Shift/Letter Shift
Omode = 0
Imode = 0

class TwoWayDict(dict): #What it says on the box
    def __missing__(self, key): #In case the box wasn't good enough, this creates exceptions that allow the values to be used as keys that map to their respective keys
        answer = None
        try:
            for i in self:
                if key in i:
                    answer = self[i]
        except TypeError:
            pass
        if(answer == None):
            for i in range(len(self.values())):
                if(list(self.values())[i] == key):
                    answer = list(self.keys())[i]
        
        if(answer != None):
            return answer
        else:
            #raise KeyError("No matching values found.")
            pass

class specials(dict): #Making my life easier to replace certain characters with symbols
    def __missing__(self, key):
        return key
    

IT2 = TwoWayDict() #A list of all the International Table 2 codes for the letters. Honestly this took way too long...
IT2.update({
("#","#"):(0,0,0,0,0),
("BACKSPACE","BACKSPACE"):(0,1,0,0,0),
("ENTER","ENTER"):(0,0,0,1,0),
("SPACE","SPACE"):(0,0,1,0,0),
("Q","1"):(1,0,1,1,1),
("W","2"):(1,0,0,1,1),
("E","3"):(0,0,0,0,1),
("R","4"):(0,1,0,1,0),
("T","5"):(1,0,0,0,0),
("Y","6"):(1,0,1,0,1),
("U","7"):(0,0,1,1,1),
("I","8"):(0,0,1,1,0),
("O","9"):(1,1,0,0,0),
("P","0"):(1,0,1,1,0),
("A","-"):(0,0,0,1,1),
("S","'"):(0,0,1,0,1),
("D","WRU?"):(0,1,0,0,1),
("F","!"):(0,1,1,0,1),
("G","&"):(1,1,0,1,0),
("H","$"):(1,0,1,0,0),
("J","Bell"):(0,1,0,1,1),
("K","("):(0,1,1,1,1),
("L",")"):(1,0,0,1,0),
("Z","+"):(1,0,0,0,1),
("X","/"):(1,1,1,0,1),
("C",":"):(0,1,1,1,0),
("V","="):(1,1,1,1,0),
("B","?"):(1,1,0,0,1),
("N",","):(0,1,1,0,0),
("M","."):(1,1,1,0,0),
("CAPS LOCK","CAPS LOCK"):(1,1,0,1,1),
("TAB","TAB"):(1,1,1,1,1)})

Translate = specials({"TAB":"-","ENTER":("\n"),"CAPS LOCK":"|","SPACE":"_","BACKSPACE":"<-"}) #The prodigal son returns
Rich = specials({"SPACE":" ", "BACKSPACE":"\b","ENTER":"\n"})

def xor(k,s): #eXclusive-OR function to perform modulo 2 addition
    
    if((int(k) == 0 or int(k) == 1) and (int(s) == 0 or int(s) == 1)):
        
        if(int(k) == int(s)):
            
            return 0
        
        else:
            
            return 1
        
    else:
        
        raise TypeError("Only accepts binary 0 or 1 inputs")

class wheel(): #Defines the characteristics and behaviours of each of the wheels in the program
    
    def __init__(self, numberOfPins, motor = None, pins = None):
        
        self.pins = ([r(0,1) for _ in range(numberOfPins)] if(pins == None) else pins)
        self.pointer = 0
        self.motor = motor
        
    def __len__(self):
        
        return len(self.pins)
    
    def setPosition(self, pos):
        
        if(pos < len(self)):
            while self.pointer != pos:
                self.step()
        else:
            raise IndexError("Value out of range")
        
    def step(self):
        
        self.pointer += 1
        #move self.motor 1 increment
        
        if(self.pointer >= len(self)):
            self.pointer -= len(self)
        
    def __repr__(self):
        
        return self.pins[self.pointer]
    
    def __int__(self):
        
        return int(self.pins[self.pointer])
    
    def __str__(self):
        
        return f"Wheel with {len(self)} pins. Current position: {str(self.pins[self.pointer])}"

def stepAll(array): #A function to step all the wheels in an array
    
    for g in array:
        
        g.step()

#Wheel Town
chi = [wheel(41),wheel(31),wheel(29),wheel(26),wheel(23)]
psi = [wheel(43),wheel(47),wheel(51),wheel(53),wheel(59)]
mu =  [wheel(61),wheel(37)]

#The transcription function in the flesh
def live_transcribe(e):
    
    global Imode
    global Omode
    
    #print(e.name)
    
    try:
        
        try:
            translating = str(e.name).upper()
        except:
            translating = str(e)
        
        """if(translating in (list("QWERTYUIOPASDFGHJKLZXCVBNM") + list(Translate.keys())) and mode != 0):
            mode = 0
            live_transcribe("CAPS LOCK")
        elif(translating not in (list("QWERTYUIOPASDFGHJKLZXCVBNM") + list(Translate.keys())) and mode != 1):
            mode = 0
            live_transcribe("TAB")"""
        
        out = ()
        i = 0
        
        #print(IT2[str(e.name).upper()])
        for i in range(5):
            #print(IT2[str(e.name).upper()][i],chi[i],psi[i])
            out += (xor(xor(IT2[translating][i],chi[i]),psi[i]),) #xorxorxorxor
            
        stepAll(chi)
        if(mu[0] == 1):
            mu[1].step()
        mu[0].step()
        if(mu[0] == 1 and mu[1] == 1):
            stepAll(psi)
        
        #print(("".join([str(item) for item in IT2[str(e.name).upper()]]) if(len(IT2[str(e.name).upper()]) > 2) else IT2[str(e.name).upper()][mode])+ " ")
        #print("".join([str(stuff) for stuff in list(out)]))
        
        if(translating == "CAPS LOCK"):
            Imode = 0
        elif(translating == "TAB"):
            Imode = 1
        if(IT2[out][Omode] == "CAPS LOCK"):
            Omode = 0
        elif(IT2[out][Omode] == "TAB"):
            Omode = 1
        
        #Outputs to the labels I have made
        pre.config(text = (pre.cget("text") + (Translate[str(e.name).upper()])))
        for a in list(IT2.keys()):
            if(translating in a and (translating not in list(Translate.keys()) or (translating == "SPACE" or translating == "BACKSPACE" or translating == "ENTER"))):
                if(translating == "BACKSPACE"):
                    if(len(before.cget("text")) > 9):
                        before.config(text = before.cget("text")[0:-1])
                else:
                    before.config(text = before.cget("text") + Rich[a[Imode]])
        tran.config(text = (tran.cget("text") + str(Translate[IT2[out][Omode]])))
        for b in list(IT2.keys()):
            if(IT2[out][Omode] in b): #  and (IT2[out][Omode] not in list(Translate.keys()) or (IT2[out][Omode] == "SPACE" or IT2[out][Omode] == "BACKSPACE" or IT2[out][Omode] == "ENTER"))
                after.config(text = after.cget("text") + Translate[b[Imode]])
        
    except:
        
        #raise
        pass

#Keyboard Setup
keyboard.on_press(live_transcribe)

#Tkinter Showcase Code
master = Tk()
master.geometry("800x300")
sub = Frame(master)
pre = Label(sub, text = "RAW IN: ")
before = Label(sub, text = "RICH IN: ")
tran = Label(sub,text = "RAW OUT: ")
after = Label(sub,text = "RICH OUT: ")
pre.pack()
before.pack()
tran.pack()
after.pack()
sub.place(relx = 0.5, rely = 0.5, anchor = CENTER)
master.mainloop()

"""
TEST for numbers:

#IGKZV
GRY
TEST for alphabet:
FAH-)8!Bell20&275$9.')=5)WRU?WRU?://+_6+,8_!+_!1-<-!

TEST for free:
TXHGNBQEZO|S|QBCA

"""
