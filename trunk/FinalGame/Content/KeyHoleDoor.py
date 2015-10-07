import Zero
import Events
import Property
import VectorMath
import Action
Vec4 = VectorMath.Vec4
import Color
class KeyHoleDoor:
    KeyHole = Property.String("")
    DoorTable = Property.ResourceTable()
    NextLevel = Property.Level()
    Teleport = Property.Cog()
    SimpleTeleport = Property.Bool(False)
    TransitionColor = Property.Color(Color.White)
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        self.TryKeyEvent = Zero.ScriptEvent()
        self.TryKeyEvent.Callback = lambda: self.OpenDoor()
        
        self.TryKeyEvent.KeyHole = self.KeyHole
        self.Opened = False
        
        self.teleporting = False
        self.observer_list = []
        
    def OnCollision(self, CollisionEvent):
        if not self.Opened:
            CollisionEvent.OtherObject.DispatchEvent("TryKeyEvent", self.TryKeyEvent)
                
        
            
    def TeleportThis(self, target):
        
        if not self.teleporting :
            if self.NextLevel.Name != "DefaultLevel":
                self.Space.FindObjectByName("Camera").CameraFunction.SetCameraFade(self.TransitionColor*Vec4(1,1,1,0),self.TransitionColor,.03,0)
                
                ls = self.Space.FindObjectByName("LevelSettings").LevelStart
                if ls:
                    ls.HUDManager.HideBoxes()
                    hm = ls.HUDManager
                    hm.CacheSkills()
                
                sequence = Action.Sequence(self.Owner.Actions)
                Action.Delay(sequence, 1.5)
                Action.Call(sequence, lambda:self.Space.LoadLevel(self.NextLevel))
                self.teleporting = True
            
        if self.Teleport:
            camera = self.Space.FindObjectByName("Camera")

            dest = self.Teleport.Transform.Translation
            ct = camera.Transform.Translation
            pt = target.Transform.Translation

            #camera.CameraFunction.SetCameraFade(Vec4(0,0,0,1),Vec4(0,0,0,0),.03,0)
            #camera.Transform.Translation = VectorMath.Vec3(dest.x, dest.y,ct.z)
            target.Transform.Translation = VectorMath.Vec3(dest.x, dest.y,pt.z)

    def RegisterObserver(self, observer):
        self.observer_list.append(observer)
        
    def OpenDoor(self):
        if not self.Owner.Sprite.SpriteSource.Name == "BlackDoor":
            self.Owner.Sprite.SpriteSource = self.DoorTable.FindResource("Black")
            self.Space.SoundSpace.PlayCue("DoorOpenCue")
        self.Opened = True
        for callback in self.observer_list:
            callback()
           
        self.observer_list = []


        
    def IsOpened(self):
        return self.Opened
                
        
        
Zero.RegisterComponent("KeyHoleDoor", KeyHoleDoor)