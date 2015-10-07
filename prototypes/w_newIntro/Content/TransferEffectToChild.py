import Zero
import Events
import Property
import VectorMath

class TransferEffectToChild:
    ChildName = Property.String("")
    def Initialize(self, initializer):
        pass

Zero.RegisterComponent("TransferEffectToChild", TransferEffectToChild)