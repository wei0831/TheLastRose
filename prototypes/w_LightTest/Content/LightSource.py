import Zero
import Events
import Property
import VectorMath
import Action
import random

class LightSource:
    Min = 0
    Max = 0
    MinRange = 3
    MaxRange = 6
    MinVariation = 0.2
    MaxVariation = 1
    MinTimeMinVar = 0.5
    MinTimeMaxVar = 1
    MaxTimeMinVar = 0.2
    MaxTimeMaxVar = 0.75

    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, Events.MouseUpdate, self.OnMouseUpdate)
        self.Test()
        self.Test2()
        
    def OnLogicUpdate(self, LogicUpdate):
        LightStart = Zero.ScriptEvent()
        LightStart.Min = self.Min
        LightStart.Max = self.Max
        LightStart.Source = self.Owner
        LightStart.Center = self.Owner.Transform.Translation
        
        self.Owner.Region.DispatchEvent("LightStartEvent", LightStart)
        
    def OnMouseUpdate(self, MouseUpdate):
        mousePos = MouseUpdate.ToWorldZPlane(0.0)
        mousePos.z = 0
        self.Owner.Transform.Translation = mousePos
        
    def Test(self):
        self.Max = self.MaxRange + random.uniform(0, self.MaxVariation)
        self.Owner.SphereCollider.Radius = self.Max
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, random.uniform(self.MaxTimeMinVar, self.MaxTimeMaxVar))
        Action.Call(sequence, self.Test)
        
    def Test2(self):
        self.Min = self.MinRange + random.uniform(0, self.MinVariation)
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, random.uniform(self.MinTimeMinVar, self.MinTimeMaxVar))
        Action.Call(sequence, self.Test2)

Zero.RegisterComponent("LightSource", LightSource)