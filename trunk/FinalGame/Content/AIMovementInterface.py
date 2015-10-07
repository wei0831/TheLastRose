import Zero
import Events
import Property
import VectorMath

class AIMovementInterface:
    def Initialize(self, initializer):
        self.AIMovement = None
        
    def Set(self, AI):
        self.AIMovement = AI
        
    def IsSet(self):
        return not self.AIMovement is None
        
    def Deactivate(self):
        if self.AIMovement:
            self.AIMovement.Active = False
    def Activate(self):
        if self.AIMovement:
            self.AIMovement.Active = True
            
    def Get(self):
        return self.Owner.AIMovement
        
    def SlowDownBy(self, SlowDownRatio, TimeSteps):
        if self.AIMovement:
            self.AIMovement.SlowDownBy(SlowDownRatio, TimeSteps)
        

Zero.RegisterComponent("AIMovementInterface", AIMovementInterface)