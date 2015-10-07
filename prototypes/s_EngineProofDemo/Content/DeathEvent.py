import Zero
import Events
import Property
import VectorMath

class DeathEvent:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollideEvent):
        otherObj = CollideEvent.OtherObject
        
        if(otherObj.CanDie != None):
            otherObj.CanDie.Die()


Zero.RegisterComponent("DeathEvent", DeathEvent)