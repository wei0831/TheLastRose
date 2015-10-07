import Zero
import Events
import Property
import VectorMath

class Yeller:
    def Initialize(self, initializer):        
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)

    def OnCollision(self, CollisionEvent):
        pass
        #print(CollisionEvent.OtherObject.Name)
        #print(self.Owner.Transform.Translation)

Zero.RegisterComponent("Yeller", Yeller)