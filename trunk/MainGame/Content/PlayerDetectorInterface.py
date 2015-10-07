import Zero
import Events
import Property
import VectorMath

class PlayerDetectorInterface:
    Size = Property.Vector3(VectorMath.Vec3(1,1,1))
    def Initialize(self, initializer):
        self.playerdetector = None
        
    def Activate(self):
        if not self.playerdetector:
            self.playerdetector = self.Space.CreateAtPosition("PlayerDetectorEntity",self.Owner.Transform.Translation)
            self.SyncSize()
            self.playerdetector.AttachToRelative(self.Owner)
            
    def Deactivate(self):
        if self.playerdetector:
            self.playerdetector.DetachRelative()
            self.playerdetector.Destroy()
            
    def SetSize(self, size):
        self.Size = size
        self.SyncSize()
        
    def SyncSize(self):
        if self.playerdetector:
            self.playerdetector.Transform.Scale = VectorMath.Vec3(1,1,1) * self.Size
            
    def GetDirection(self):
        if self.playerdetector:
            return self.playerdetector.PlayerDetector.GetDirection()
        else:
            return VectorMath.Vec3(0,0,0)
    def InRange(self):
        if self.playerdetector:
            return self.playerdetector.PlayerDetector.InRange()
        else:
            return False
    def Destroyed(self):
        self.Deactivate()

Zero.RegisterComponent("PlayerDetectorInterface", PlayerDetectorInterface)