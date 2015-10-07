import Zero
import Events
import Property
import VectorMath
Vec4 = VectorMath.Vec4
class ChangeLevel:
    LevelToLoad = Property.Resource("Level")

    KeyToEnter = Zero.Keys.W
    KeyPressDelay = Property.Float(0.5)
    timer = 0
    TouchDoor = False
    ReadyToGoNextLevel = False
    
    def Initialize(self, initializer):
        self.Camera = self.Space.FindObjectByName("Camera")
        self.Player = self.Space.FindObjectByName("Player")
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OncollisionStart)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.OncollisionEnd)
        
    def OnLogicUpdate(self, LogicUpdate):
        if not self.ReadyToGoNextLevel and self.TouchDoor and Zero.Keyboard.KeyIsDown(self.KeyToEnter):
            self.timer += LogicUpdate.Dt
            if self.timer > self.KeyPressDelay:
                self.Player.PlayerController.Active = False
                self.ReadyToGoNextLevel = True
                self.LoadLevelEvent()
                self.timer = 0
                
        if self.ReadyToGoNextLevel:
            if self.Camera.CameraFunction.FadeDone :
                self.Space.LoadLevel(self.LevelToLoad)
                
    def OncollisionStart(self, CollsionEvent):
        if CollsionEvent.OtherObject == self.Player:
            self.TouchDoor = True
            CollsionEvent.OtherObject.PlayerController.JumpActive = False
            
    def OncollisionEnd(self, CollsionEvent):
        if CollsionEvent.OtherObject == self.Player:
            self.TouchDoor = False
            self.timer = 0
            CollsionEvent.OtherObject.PlayerController.JumpActive = True
        
    def LoadLevelEvent(self):
        self.Camera.CameraFunction.SetCameraFade(Vec4(0, 0, 0, 0), Vec4(0, 0, 0, 1), 0.01, 0)

Zero.RegisterComponent("ChangeLevel", ChangeLevel)