import Zero
import Events
import Property
import VectorMath

class Key:
    KeyValue = Property.String("")
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        self.GetKeyEvent = Zero.ScriptEvent()
        self.GetKeyEvent.Callback = lambda: self.Owner.Destroy()
        self.GetKeyEvent.KeyValue = self.KeyValue
        
    def OnCollision(self, CollisionEvent):
        CollisionEvent.OtherObject.DispatchEvent("GetKeyEvent", self.GetKeyEvent)
        

Zero.RegisterComponent("Key", Key)