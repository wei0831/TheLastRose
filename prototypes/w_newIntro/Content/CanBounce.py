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
            modifier = -1 if self.UpdateBasedOnSprite and self.Owner.Sprite.FlipX else 1

            if CollisionEvent.OtherObject.Bounceable:
                self.Space.SoundSpace.PlayCue("JumpCue")
                impulseEvent = Zero.ScriptEvent()
                impulseEvent.ForcedVx = self.ForcedVx * modifier     
                impulseEvent.ForcedVy = self.ForcedVy      
                CollisionEvent.OtherObject.DispatchEvent("BounceEvent", impulseEvent)
                
    def ToDirection(self, normal):
        
        self.ForcedVx = self.InitialStrength * normal.x
        self.ForcedVy = self.InitialStrength * normal.y
        
        
            
            

Zero.RegisterComponent("CanBounce", CanBounce)