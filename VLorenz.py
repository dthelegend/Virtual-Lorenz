#Import Town
import keyboard
from tkinter import *
from random import randint as r, seed as seed

#Using a random seed to make sure wheel generation is always the same
seed(75434390)

mode = 0

class TwoWayDict(dict):
    def __missing__(self, key):
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

class specials(dict):
    def __missing__(self, key):
        return key
    

IT2 = TwoWayDict()
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

Translate = specials({"TAB":"-","ENTER":("\n"),"CAPS LOCK":"|","SPACE":"_","BACKSPACE":"<-"})

def xor(k,s):
    
    if((int(k) == 0 or int(k) == 1) and (int(s) == 0 or int(s) == 1)):
        
        if(int(k) == int(s)):
            
            return 0
        
        else:
            
            return 1
        
    else:
        
        raise TypeError("Only accepts binary 0 or 1 inputs")

class wheel():
    
    def __init__(self, numberOfPins, motor, pins = None):
        
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
        
        return str(self.pins[self.pointer])

def stepAll(array):
    
    for g in array:
        
        g.step()
    
chi = [wheel(41),wheel(31),wheel(29),wheel(26),wheel(23)]
psi = [wheel(43),wheel(47),wheel(51),wheel(53),wheel(59)]
mu =  [wheel(61),wheel(37)]

def live_transcribe(e):
    
    global mode
    
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
            out += (xor(xor(IT2[translating][i],chi[i]),psi[i]),)
            
        stepAll(chi)
        if(mu[0] == 1):
            mu[1].step()
        mu[0].step()
        if(mu[0] == 1 and mu[1] == 1):
            stepAll(psi)
        
        #print(("".join([str(item) for item in IT2[str(e.name).upper()]]) if(len(IT2[str(e.name).upper()]) > 2) else IT2[str(e.name).upper()][mode])+ " ")
        #print("".join([str(stuff) for stuff in list(out)]))
        
        if(IT2[out][mode] == "CAPS LOCK"):
            mode = 0
        elif(IT2[out][mode] == "TAB"):
            mode = 1
        
        print(Translate[IT2[out][mode]], end = "")
        
    except:
        
        #raise
        pass

#Keyboard Setup
keyboard.on_press(live_transcribe)
keyboard.block_key("BACKSPACE")

#Tkinter Showcase Code
master = Tk()
master.geometry("800x300")
sub = Frame(master)
pre = Entry(sub, width = 100)
tran = Label(sub,text = "")
pre.pack()
tran.pack()
sub.place(relx = 0.5, rely = 0.5, anchor = CENTER)
master.mainloop()

"""
TEST for numbers:

#IGKZV
GRY
TEST for alphabet:
FAH-)8!Bell20&275$9.')=5)WRU?WRU?://+_6+,8_!+_!1-<-!

"""