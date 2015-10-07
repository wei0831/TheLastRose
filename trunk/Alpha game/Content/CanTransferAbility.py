import Zero
import Events
import Property
import VectorMath

class CanTransferAbility:    
    def Initialize(self, initializer):
        self.Callback = None
        self.Activated = False
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
    
    def SetCallback(self, callback):
        self.Callback = callback
        
    def OnCollision(self, CollisionEvent):
        if not self.Activated and CollisionEvent.OtherObject.AbilityStatus:
            if self.Callback:
                self.Callback()
            self.Activated = True
            self.Callback = None
            
    def IsActivated(self):
        return self.Activated

Zero.RegisterComponent("CanTransferAbility", CanTransferAbility)