import Zero
import Events
import Property
import VectorMath

class CanTrigger:
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        pass

Zero.RegisterComponent("CanTrigger", CanTrigger)