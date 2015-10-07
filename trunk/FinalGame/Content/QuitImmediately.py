import Zero
import Events
import Property
import VectorMath

class QuitImmediately:
    def Initialize(self, initializer):
        Zero.Game.Quit()

Zero.RegisterComponent("QuitImmediately", QuitImmediately)