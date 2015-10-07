import Zero
import Events
import Property
import VectorMath

class CanBurn:
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        if not self.Owner.BurnAnim:
            self.Owner.AddComponentByName("BurnAnim")
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        if self.Active:
            BurnEvent = Zero.ScriptEvent()
            CollisionEvent.OtherObject.DispatchEvent("BurnEvent", BurnEvent)
    
    def Quench(self):
        self.Owner.BurnAnim.Active = False
        self.Active = False
        if self.Owner.CanSpawnWind:
            self.Owner.CanSpawnWind.Active = False
    
    def Reburn(self):
        self.Owner.BurnAnim.Active = True
        self.Active = True
        if self.Owner.CanSpawnWind:
            self.Owner.CanSpawnWind.Active = True
                

Zero.RegisterComponent("CanBurn", CanBurn)