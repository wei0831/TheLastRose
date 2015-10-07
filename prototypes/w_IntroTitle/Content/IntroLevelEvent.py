import Zero
import Events
import Property
import VectorMath
import Action

Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class IntroLevelEvent:
    Camera = Property.Cog()
    CurrentFunction = None
    LogoDisplayDelay = Property.Float(1)
    
    
    def Initialize(self, initializer):
        self.Logo = self.Space.CreateAtPosition("DigipenLogo", Vec3(0, 0, 0))

        Zero.Connect(self.Space, Events.LevelStarted, self.OnLevelStart)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    def OnLevelStart(self, LevelStartEvent):
        self.Camera.CameraFunction.SetCameraFade(Vec4(0, 0, 0, 1), Vec4(0, 0, 0, 0), 0.005, 0)
        self.CurrentFunction = self.E1_ActivateLogo
    
    def OnLogicUpdate(self, UpdateEvent):
        if self.CurrentFunction == None: return
        
        self.CurrentFunction()
        
    def E1_ActivateLogo(self):
        if self.Camera.CameraFunction.FadeDone :
            self.Logo.Animator.Active = True
            self.GoToE2()
            
    def GoToE2(self):
        self.CurrentFunction = self.E2_CheckAnimatorEnd
    
    def E2_CheckAnimatorEnd(self):
        if not self.Logo.Animator.Active:
            self.CurrentFunction = None
            self.Space.SoundSpace.PlayCue("RavenCue")
            sequence = Action.Sequence(self.Owner.Actions)
            Action.Delay(sequence, self.LogoDisplayDelay)
            Action.Call(sequence, self.GoToE3)
            
    def GoToE3(self):
        self.Camera.CameraFunction.SetCameraFade(Vec4(0, 0, 0, 0), Vec4(0, 0, 0, 1), 0.005, 0)
        self.CurrentFunction = self.E3_Done
        
    def E3_Done(self):
        if self.Camera.CameraFunction.FadeDone :
            self.Space.LoadLevel("TitleScreen")
    
Zero.RegisterComponent("IntroLevelEvent", IntroLevelEvent)