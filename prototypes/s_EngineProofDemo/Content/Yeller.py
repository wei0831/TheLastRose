import Zero
import Events
import Property
import VectorMath

class Yeller:
    def Initialize(self, initializer):        
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)

    def OnCollision(self, CollisionEvent):
        print(CollisionEvent.OtherObject.Name)

Zero.RegisterComponent("Yeller", Yeller)