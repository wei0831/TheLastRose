import Zero
import Events
import Property
import VectorMath

class AIMovementInterface:
    def Initialize(self, initializer):
        if self.Owner.AIMovementPacing:
            self.AIMovement = self.Owner.AIMovementPacing
        elif self.Owner.AIMovementSentry:
            self.AIMovement = self.Owner.AIMovementSentry
        else:
            self.AIMovement = None
            
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