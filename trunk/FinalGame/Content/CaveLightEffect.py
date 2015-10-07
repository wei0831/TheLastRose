import Zero
import Events
import Property
import VectorMath
Vec4 = VectorMath.Vec4
class CaveLightEffect:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnd)
        self.camera = self.Space.FindObjectByName("Camera")
        
        self.lightened = False
        
    def OnCollision(self, CollisionEvent):
        if not self.lightened:
            self.camera.CameraFunction.SetCameraFade(Vec4(1,1,1,0), Vec4(1,1,1,.1), .125,0)
            self.lightened = True
    def OnCollisionEnd(self, CollisionEvent):
        if self.lightened:
            self.camera.CameraFunction.SetCameraFade(Vec4(1,1,1,.1), Vec4(1,1,1,0), .125,0)
            self.lightened = False

Zero.RegisterComponent("CaveLightEffect", CaveLightEffect)