import Zero
import Events
import Property
import VectorMath

class CanSpawnWind:
    Active = Property.Bool(True)
    Size = Property.Float(1)
    Force = Property.Float(1)
    def Initialize(self, initializer):
        self.windregion = self.Space.CreateAtPosition("WindRegion", self.Owner.Transform.WorldTranslation)
        self.windregion.Transform.Scale *= VectorMath.Vec3(1,self.Size,1)
        self.windregion.CanBlow.BlowForce *= self.Force
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Active:
            if not self.windregion:
                self.windregion = self.Space.CreateAtPosition("WindRegion", self.Owner.Transform.WorldTranslation)
            if self.Owner:
                self.windregion.Transform.WorldTranslation = self.Owner.Transform.WorldTranslation
        else:
            if self.windregion:
                self.windregion.Destroy()
        
    def Destroyed(self):
        if self.windregion:
            self.windregion.Destroy()
        
    

Zero.RegisterComponent("CanSpawnWind", CanSpawnWind)