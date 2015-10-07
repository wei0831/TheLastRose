import Zero
import Events
import Property
import VectorMath
import Action
class KeySpriteManager:
    SpriteTable = Property.ResourceTable()
    ShineDelay = Property.Float(1.7)
    def Initialize(self, initializer):
        self.shinesprite = self.SpriteTable.FindValue(self.Owner.Key.KeyValue + "Shine")
        self.seq = Action.Sequence(self.Owner.Actions)
        self.PlayShineAnim()
        
    def PlayShineAnim(self):
        self.Owner.Sprite.SpriteSource = self.shinesprite
        Action.Delay(self.seq, self.ShineDelay)
        Action.Call(self.seq, self.PlayShineAnim)
        
        

Zero.RegisterComponent("KeySpriteManager", KeySpriteManager)