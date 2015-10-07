import Zero
import Events
import Property
import VectorMath

class CreateBackgroundSpace:

    def Initialize(self, initializer):
        self.BackgroundSpace = Zero.Game.CreateNamedSpace("BackgroundLevel", "Space")
        self.BackgroundSpace.LoadLevel("BackgroundLevel")

Zero.RegisterComponent("CreateBackgroundSpace", CreateBackgroundSpace)