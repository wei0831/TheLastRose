import Zero
import Events
import Property
import VectorMath

class CanBlow:
    BlowDirection = Property.Vector3(VectorMath.Vec3(0,1,0))
    BlowForce = Property.Float(4)
    
    def Initialize(self, initializer):
        pass
        
    def Blow(self, target, decay):
        if target.RigidBody:
            target.RigidBody.ApplyForce(self.BlowDirection * self.BlowForce * decay)

Zero.RegisterComponent("CanBlow", CanBlow)