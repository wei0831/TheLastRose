import Zero
import Events
import Property
import VectorMath

class CanPoison:
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        if not self.Owner.PoisonAnim:
            self.Owner.AddComponentByName("PoisonAnim")
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):        
        PoisonEvent = Zero.ScriptEvent()
        CollisionEvent.OtherObject.DispatchEvent("PoisonEvent", PoisonEvent)
    
    def Depoison(self):
        self.PoisonAnim.Active = False
        self.Active = False
    def Repoison(self):
        self.PoisonAnim.Active = True
        self.Active = True
Zero.RegisterComponent("CanPoison", CanPoison)

