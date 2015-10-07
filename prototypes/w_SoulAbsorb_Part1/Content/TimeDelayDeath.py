import Zero
import Events
import Property
import VectorMath
import Keys
import Action
import math

class TimeDelayDeath:
    #The amount of time before this object will be destroyed
    
    def Initialize(self, init):
        #Queue up a delay for our lifetime, after that much
        Action.Delay(sequence, self.Lifetime)
        Action.Call(sequence, self.OnDeath)
    
    def OnDeath(self):
        #let anyone listening know we just died
        self.Owner.DispatchEvent("Death", toSend)
        
        self.Owner.Destroy()

Zero.RegisterComponent("TimeDelayDeath", TimeDelayDeath)