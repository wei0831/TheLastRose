import Zero
import Events
import Property
import VectorMath

class Freezeable:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "FreezeEvent", self.OnFreeze)
        
    def OnFreeze(self, FreezeEvent):
        pass
Zero.RegisterComponent("Freezeable", Freezeable)