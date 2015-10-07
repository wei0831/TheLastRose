import Zero
import Events
import Property
import VectorMath
import Action
Vec4 = VectorMath.Vec4
class KeyHoleDoor:
    KeyHole = Property.String("")
    DoorTable = Property.ResourceTable()
    NextLevel = Property.Level()
    Teleport = Property.Cog()
    SimpleTeleport = Property.Bool(False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        self.TryKeyEvent = Zero.ScriptEvent()
        self.TryKeyEvent.Callback = lambda: self.OpenDoor()
        
        self.TryKeyEvent.KeyHole = self.KeyHole
        self.Opened = True if not self.KeyHole else False
        
        self.observer_list = []
        
    def OnCollision(self, CollisionEvent):
        CollisionEvent.OtherObject.DispatchEvent("TryKeyEvent", self.TryKeyEvent)
                
        
            
    def TeleportThis(self, target):
        if self.NextLevel.Name != "DefaultLevel":
            self.Space.FindObjectByName("Camera").CameraFunction.SetCameraFade(Vec4(1,1,1,0),Vec4(1,1,1,1),.03,0)
            sequence = Action.Sequence(self.Owner.Actions)
            
            ls = self.Space.FindObjectByName("LevelSettings").LevelStart
            if ls:
                hm = ls.HUDManager
                hm.CacheSkills()
            
            Action.Delay(sequence, 1.5)
            Action.Call(sequence, lambda:self.Space.LoadLevel(self.NextLevel))
            
            
        elif self.Teleport:
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
        self.Owner.Sprite.SpriteSource = self.DoorTable.FindResource("Black")
        self.Opened = True
        for callback in self.observer_list:
            callback()
           
        self.observer_list = []


        
    def IsOpened(self):
        return self.Opened
                
        
        
Zero.RegisterComponent("KeyHoleDoor", KeyHoleDoor)