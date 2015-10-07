import Zero
import Events
import Property
import VectorMath

class Bounceable:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "BounceEvent", self.OnBounce)
        
    def OnBounce(self, BounceEvent):
        Vx = BounceEvent.ForcedVx
        Vy = BounceEvent.ForcedVy
        
        self_v = self.Owner.RigidBody.Velocity
        self_v.x = self_v.x if Vx == 0 else Vx
        self_v.y = self_v.y if Vy == 0 else Vy
        
        self.Owner.RigidBody.Velocity = self_v

Zero.RegisterComponent("Bounceable", Bounceable)