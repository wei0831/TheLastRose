import Zero
import Events
import Property
import VectorMath
import Action
import random

class LightSource:
    Min = 0
    Max = 0
    MinRange = 1
    MaxRange = 5
    MinVariation = 0.2
    MaxVariation = 1
    MinTimeMinVar = 0.5
    MinTimeMaxVar = 1
    MaxTimeMinVar = 0.2
    MaxTimeMaxVar = 0.75
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        #Zero.Connect(self.Space, Events.MouseUpdate, self.OnMouseUpdate)
        self.sequence = Action.Sequence(self.Owner.Actions)


        self.LightStart = Zero.ScriptEvent()
        self.LightStart.Min = self.Min
        self.LightStart.Max = self.Max
        self.LightStart.Source = self.Owner
        self.LightStart.Center = self.Owner.Transform.Translation
        
        self.Test()
        self.Test2()
        
    def OnLogicUpdate(self, LogicUpdate):
        if not self.Active: return
        self.Owner.Region.DispatchEvent("LightStartEvent", self.LightStart)
                
    #def OnMouseUpdate(self, MouseUpdate):
    #    mousePos = MouseUpdate.ToWorldZPlane(0.0)
    #    mousePos.z = 0
    #    self.Owner.Transform.Translation = mousePos
        
    def Test(self):
        self.Max = self.MaxRange + random.uniform(0, self.MaxVariation)
        self.Owner.SphereCollider.Radius = self.Max
        

        self.LightStart.Min = self.Min
        self.LightStart.Max = self.Max
        self.LightStart.Source = self.Owner
        self.LightStart.Center = self.Owner.Transform.Translation

        Action.Delay(self.sequence, random.uniform(self.MaxTimeMinVar, self.MaxTimeMaxVar))
        Action.Call(self.sequence, self.Test)        
        
    def Test2(self):
        self.Min = self.MinRange + random.uniform(0, self.MinVariation)
        sequence = Action.Sequence(self.Owner.Actions)

        self.LightStart.Min = self.Min
        self.LightStart.Max = self.Max
        self.LightStart.Source = self.Owner
        self.LightStart.Center = self.Owner.Transform.Translation
        
        Action.Delay(self.sequence, random.uniform(self.MinTimeMinVar, self.MinTimeMaxVar))
        Action.Call(self.sequence, self.Test2)
        

Zero.RegisterComponent("LightSource", LightSource)