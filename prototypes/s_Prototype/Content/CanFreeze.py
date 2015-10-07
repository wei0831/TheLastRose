import Zero
import Events
import Property
import VectorMath

class CanFreeze:
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        if not self.Owner.FreezeAnim:
            self.Owner.AddComponentByName("FreezeAnim")
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):    
        if self.Active:
            FreezeEvent = Zero.ScriptEvent()
            CollisionEvent.OtherObject.DispatchEvent("FreezeEvent", FreezeEvent)
        
    def Defrost(self):
        self.Owner.FreezeAnim.Active = False
        self.Active = False
    def Refrost(self):
        self.Owner.FreezeAnim.Active = True
        self.Active = True
            

Zero.RegisterComponent("CanFreeze", CanFreeze)

