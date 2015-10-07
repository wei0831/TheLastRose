import Zero
import Events
import Property
import VectorMath

class TouchDisappear:
    def Initialize(self, initializer):
        self.count = 0
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        self.count += 1
        if self.count == 1:
            self.Owner.Destroy()
        #self.Owner.Destroy()

Zero.RegisterComponent("TouchDisappear", TouchDisappear)