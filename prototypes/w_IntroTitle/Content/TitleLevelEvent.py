import Zero
import Events
import Property
import VectorMath
import Action

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class TitleLevelEvent:
    Camera = Property.Cog()
    Player = Property.Cog()
    CurrentFunction = None
   
    E1ToE2Delay = 2.5
    
    
    def Initialize(self, initializer):
        self.Space.SoundSpace.PlayMusic("Rain")

        
        Zero.Connect(self.Space, Events.LevelStarted, self.OnLevelStart)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    def OnLogicUpdate(self, UpdateEvent):
        if self.CurrentFunction == None: return
        
        self.CurrentFunction()
        
    def OnLevelStart(self, LevelStartEvent):
        self.Camera.CameraFunction.SetCameraFade(Vec4(0, 0, 0, 1), Vec4(0, 0, 0, 0), 0.005, 0)
        self.CurrentFunction = self.E1_ActivateLogo
    
    def E1_ActivateLogo(self):
        if self.Camera.CameraFunction.FadeDone :
            self.CurrentFunction = None
            self.Camera.ThunderGenerator.ActivateThunder()
            sequence = Action.Sequence(self.Owner.Actions)
            Action.Delay(sequence, self.E1ToE2Delay)
            Action.Call(sequence, self.GoToE2)
            
    def GoToE2(self):
        self.Camera.CameraFunction.SetChase(0.01)
        self.CurrentFunction = self.E2_CheckAnimatorEnd
    
    def E2_CheckAnimatorEnd(self):
        pass
            
            
    def GoToE3(self):
        self.Camera.CameraFunction.SetCameraFade(Vec4(0, 0, 0, 0), Vec4(0, 0, 0, 1), 0.005, 0)
        self.CurrentFunction = self.E3_Done
        
    def E3_Done(self):
        if self.Camera.CameraFunction.FadeDone :
            self.Space.LoadLevel("TitleScreen")

Zero.RegisterComponent("TitleLevelEvent", TitleLevelEvent)