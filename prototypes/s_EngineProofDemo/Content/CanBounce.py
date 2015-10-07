import Zero
import Events
import Property
import VectorMath
import math

class CanBounce:
    Active = Property.Bool(True)
    ForcedVx = Property.Float(0)
    ForcedVy = Property.Float(0)
    UpdateBasedOnSprite = Property.Bool(False)
    def Initialize(self, initializer):
        self.InitialStrength = math.sqrt(self.ForcedVx**2 + self.ForcedVy**2)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        if self.Active:
            if self.UpdateBasedOnSprite:
                if (self.Owner.Sprite.FlipX == True and self.ForcedVx > 0) or (self.Owner.Sprite.FlipX == False and self.ForcedVx < 0):
                    self.ForcedVx = -self.ForcedVx
                    
            if CollisionEvent.OtherObject.Bounceable:
                impulseEvent = Zero.ScriptEvent()
                impulseEvent.ForcedVx = self.ForcedVx      
                impulseEvent.ForcedVy = self.ForcedVy      
                CollisionEvent.OtherObject.DispatchEvent("BounceEvent", impulseEvent)
                
    def ToDirection(self, normal):
        
        self.ForcedVx = self.InitialStrength * normal.x
        self.ForcedVy = self.InitialStrength * normal.y
        
        
            
            

Zero.RegisterComponent("CanBounce", CanBounce)