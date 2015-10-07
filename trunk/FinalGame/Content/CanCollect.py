import Zero
import Events
import Property
import VectorMath

class CanCollect:
    
    def Initialize(self, initializer):
        self.hudmanager = self.Space.FindObjectByName("LevelSettings").LevelStart.HUDManager
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.Collectible:
            CollisionEvent.OtherObject.Collectible.Collected()
            
            type = CollisionEvent.OtherObject.Collectible.GetType()
            self.hudmanager.AddScore(1,type)

Zero.RegisterComponent("CanCollect", CanCollect)