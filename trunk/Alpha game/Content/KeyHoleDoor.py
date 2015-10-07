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
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        self.TryKeyEvent = Zero.ScriptEvent()
        self.TryKeyEvent.Callback = lambda: self.OpenDoor()
        
        self.TryKeyEvent.KeyHole = self.KeyHole
        
    def OnCollision(self, CollisionEvent):
        CollisionEvent.OtherObject.DispatchEvent("TryKeyEvent", self.TryKeyEvent)
        
    def OpenDoor(self):
        self.Owner.Sprite.SpriteSource = self.DoorTable.FindResource("Black")
        self.Space.FindObjectByName("Camera").CameraFunction.SetCameraFade(Vec4(1,1,1,0),Vec4(1,1,1,1),.03,0)
        
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, 1.5)
        Action.Call(sequence, lambda:self.Space.LoadLevel(self.NextLevel))
        
        
Zero.RegisterComponent("KeyHoleDoor", KeyHoleDoor)