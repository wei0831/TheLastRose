import Zero
import Events
import Property
import VectorMath
import math
class SpeedLimit:
    VerticalLimit = Property.Float(1)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    def OnLogicUpdate(self, UpdateEvent):
        if self.Owner.RigidBody.Velocity.y > self.VerticalLimit:
            v = self.Owner.RigidBody.Velocity 
            self.Owner.RigidBody.Velocity = VectorMath.Vec3(v.x, math.copysign(self.VerticalLimit, v.y),v.z)

Zero.RegisterComponent("SpeedLimit", SpeedLimit)