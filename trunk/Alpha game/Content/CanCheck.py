import Zero
import Events
import Property
import VectorMath

class CanCheck:
    def Initialize(self, initializer):
        self.CheckPosition = self.Owner.Transform.Translation
        
    def SetCheck(self, position):
        self.CheckPosition = position
    
    def GetCheck(self):
        return self.CheckPosition
    

Zero.RegisterComponent("CanCheck", CanCheck)