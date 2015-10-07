import Zero
import Events
import Property
import VectorMath

class CannotBeFrozen:
    def Initialize(self, initializer):
        pass

Zero.RegisterComponent("CannotBeFrozen", CannotBeFrozen)