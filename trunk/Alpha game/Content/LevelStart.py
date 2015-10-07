import Zero
import Events
import Property
import VectorMath
Vec4 = VectorMath.Vec4

class LevelStart:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        camera = self.Space.FindObjectByName("Camera")
        camera.CameraFunction.SetCameraFade(Vec4(1,1,1,1),Vec4(1,1,1,0),0.03,0)
        Zero.Disconnect(self.Space, Events.LogicUpdate, self)

Zero.RegisterComponent("LevelStart", LevelStart)