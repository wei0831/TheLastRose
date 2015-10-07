import Zero
import Events
import Property
import VectorMath

class PrintMyPosition:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.Display = self.Owner.FindChildByName("Text")
        
    def OnLogicUpdate(self, UpdateEvent):
        self.Display.SpriteText.Text = "Pos: " + str(self.Owner.SaveMyGame.Location) + "\n" + "Ability: " + str(self.Owner.SaveMyGame.Ability)
        
        
Zero.RegisterComponent("PrintMyPosition", PrintMyPosition)