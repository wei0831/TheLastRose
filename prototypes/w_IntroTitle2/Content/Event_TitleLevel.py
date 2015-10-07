import Zero
import Events
import Property
import VectorMath
Vec4 = VectorMath.Vec4
class Event_TitleLevel:
    Camera = Property.Cog()
    Player = Property.Cog()
    
    CurrentFunction = None
   
    E1ToE2Delay = 2
    
    def Initialize(self, initializer):
        self.Player.PlayerController.Active = False
        Zero.Connect(self.Space, Events.LevelStarted, self.OnLevelStart)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    def OnLogicUpdate(self, UpdateEvent):
        if self.CurrentFunction == None: return
        
        self.CurrentFunction()
        
    def OnLevelStart(self, LevelStartEvent):
        self.Camera.CameraFunction.SetCameraFade(Vec4(0, 0, 0, 1), Vec4(0, 0, 0, 0), 0.01, 0)
        self.CurrentFunction = self.E1_ActivateLogo
        self.Player.PlayerController.Active = True
        
    def E1_ActivateLogo(self):
        if self.Camera.CameraFunction.FadeDone :
            self.CurrentFunction = None
            

Zero.RegisterComponent("Event_TitleLevel", Event_TitleLevel)