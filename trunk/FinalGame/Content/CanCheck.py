import Zero
import Events
import Property
import VectorMath

class CanCheck:
    def Initialize(self, initializer):
        self.init_place = self.Owner.Transform.Translation
        self.current_check = None
        
    def SetCheck(self, checkpoint):
        if self.current_check:
            self.current_check.Checkable.CheckOut()
            
        self.current_check = checkpoint
    
    def GetCheck(self):
        if not self.current_check:
            return self.init_place
        else:
            return self.current_check.Transform.Translation
    

Zero.RegisterComponent("CanCheck", CanCheck)