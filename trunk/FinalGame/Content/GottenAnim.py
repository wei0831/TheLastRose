import Zero
import Events
import Property
import VectorMath

class GottenAnim:
    def Initialize(self, initializer):
        self.Owner.DestroyInterface.RegisterObserver(self.Play)
        
    def Play(self):
        shooted = self.Space.CreateAtPosition("GottenAnimDummy", self.Owner.Transform.Translation + VectorMath.Vec3(0,0,3))
        shooted.Sprite.SpriteSource = self.Owner.Sprite.SpriteSource
        shooted.Transform.Scale = self.Owner.Transform.Scale
        

Zero.RegisterComponent("GottenAnim", GottenAnim)