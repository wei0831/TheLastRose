import Zero
import Events
import Property
import VectorMath

class ProtectiveAnimal:
    def Initialize(self, initializer):
        particle = self.Space.CreateAtPosition("ProtectiveParticles", self.Owner.Transform.WorldTranslation)
        particle.AttachToRelative(self.Owner)

Zero.RegisterComponent("ProtectiveAnimal", ProtectiveAnimal)