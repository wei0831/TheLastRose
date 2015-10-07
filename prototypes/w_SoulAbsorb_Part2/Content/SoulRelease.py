import Zero
import Events
import Property
import VectorMath

class SoulRelease:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.target = self.Space.FindObjectByName("Hero")
        
    def OnLogicUpdate(self, UpdateEvent):
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.Space)):
            self.ReleaseSoul(self.target)
    
    def ReleaseSoul(self, Target):
        newSoul = self.Space.CreateAtPosition("AbilitySoul", self.Owner.Transform.Translation)

    

Zero.RegisterComponent("SoulRelease", SoulRelease)