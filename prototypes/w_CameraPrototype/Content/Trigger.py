import Zero
import Events
import Property
import VectorMath
import Keys

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class Trigger:
    Follow = False
    Chase = False
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, Events.MouseUpdate, self.OnMouseUpdate)
        Zero.Connect(self.Space, Events.MouseDown, self.OnMouseDown)
        self.gameCamera = self.Space.FindObjectByName("Camera")
        
    def OnLogicUpdate(self, UpdateEvent):
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.Q)):
            # Shake in X with 0.5 radius
            # Shake in Y with 0.5 radius
            # Shake for 1 sec, each shake has 0.05sec in between
            self.gameCamera.CameraFunction.SetCameraShake(True, 0.5, True, 0.5, 1, 0.05)
        
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.W)):
            self.gameCamera.CameraFunction.SetCameraFade(Vec4(0, 0, 0, 0), Vec4(0, 0, 0, 1.0), 0.05, 0)
        
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.E)):
            self.gameCamera.CameraFunction.SetCameraFade(Vec4(0, 0, 0, 1.0), Vec4(0, 0, 0, 0.0), 0.05, 0)
            
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.R)):
           if self.Follow: 
                self.gameCamera.CameraFunction.TurnOffCameraFollow()
           else:
                self.gameCamera.CameraFunction.SetFollowTarget(self.Space.FindObjectByName("Monster"))
           self.Follow = not self.Follow
           
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.T)):
           if self.Chase: 
                self.gameCamera.CameraFunction.TurnOffCameraChase()
           else:
                self.gameCamera.CameraFunction.SetChaseTarget(self.Space.FindObjectByName("Monster"), 0.025)
           self.Chase = not self.Chase
           
    def OnMouseUpdate(self, MouseUpdate):
        self.mousePos = MouseUpdate.ToWorldZPlane(0)
        
    def OnMouseDown(self, MouseDownEvent):
         self.gameCamera.CameraFunction.SetShiftTarget(self.mousePos, 0.025, 2, True)

Zero.RegisterComponent("Trigger", Trigger)