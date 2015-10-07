import Zero
import Events
import Property
import VectorMath

class CanTeleport:
    Offset = Property.Vector3(VectorMath.Vec3(0,4,0))
    
    def Initialize(self, initializer):
        pass
        
    def Teleport(self, target):
        target.Transform.Translation += self.Offset

Zero.RegisterComponent("CanTeleport", CanTeleport)