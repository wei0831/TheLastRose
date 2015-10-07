import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class AutoRotation:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    def OnLogicUpdate(self, LogicUpdate):
        dir = self.Owner.RigidBody.Velocity
        dir.normalized()
        self.Owner.Transform.WorldRotation = VectorMath.Quaternion.Between(Vec3(0, 1, 0), dir)
        
    
Zero.RegisterComponent("AutoRotation", AutoRotation)