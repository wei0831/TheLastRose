import Zero
import Events
import Property
import VectorMath

class KeyHoleDoor:
    KeyHole = Property.String("")
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        self.TryKeyEvent = Zero.ScriptEvent()
        self.TryKeyEvent.Callback = lambda: self.OpenDoor()
        
        self.TryKeyEvent.KeyHole = self.KeyHole
        
    def OnCollision(self, CollisionEvent):
        CollisionEvent.OtherObject.DispatchEvent("TryKeyEvent", self.TryKeyEvent)
        
    def OpenDoor(self):
        self.Owner.Sprite.Color = VectorMath.Vec4(0,0,0,1)

Zero.RegisterComponent("KeyHoleDoor", KeyHoleDoor)