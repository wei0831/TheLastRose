import Zero
import Events
import Property
import VectorMath

class CanSpawnWind:
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        self.windregion = self.Space.CreateAtPosition("WindRegion", self.Owner.Transform.Translation)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            if not self.windregion:
                self.windregion = self.Space.CreateAtPosition("WindRegion", self.Owner.Transform.Translation)
            if self.Owner:
                self.windregion.Transform.Translation = self.Owner.Transform.Translation
        else:
            if self.windregion:
                self.windregion.Destroy()
        
    def Destroyed(self):
        if self.windregion:
            self.windregion.Destroy()
        
    

Zero.RegisterComponent("CanSpawnWind", CanSpawnWind)