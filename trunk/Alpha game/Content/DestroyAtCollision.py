import Zero
import Events
import Property
import VectorMath

class DestroyAtCollision:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        self.Owner.Destroy()

Zero.RegisterComponent("DestroyAtCollision", DestroyAtCollision)