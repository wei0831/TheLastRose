import Zero
import Events
import Property
import VectorMath

class Key:
    KeyValue = Property.String("")
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        self.GetKeyEvent = Zero.ScriptEvent()
        
        def destroyer():
            if self.Owner.DestroyInterface:
                self.Owner.DestroyInterface.Destroy()
            else:
                self.Owner.Destroy()
            self.Owner.Destroy()
        self.GetKeyEvent.Callback = destroyer
        self.GetKeyEvent.KeyValue = self.KeyValue
        
    def OnCollision(self, CollisionEvent):
        CollisionEvent.OtherObject.DispatchEvent("GetKeyEvent", self.GetKeyEvent)
        
Zero.RegisterComponent("Key", Key)