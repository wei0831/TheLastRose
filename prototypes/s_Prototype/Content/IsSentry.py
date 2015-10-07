import Zero
import Events
import Property
import VectorMath

class IsSentry:
    SentryDirection = Property.Vector3(VectorMath.Vec3(0,0,0))
    def Initialize(self, initializer):
        pass
    

Zero.RegisterComponent("IsSentry", IsSentry)