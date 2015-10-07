import Zero
import Events
import Property
import VectorMath
import Action

class AnimationOnce:
    Frame = Property.Int(4)
    MaxLife = Property.Float(0.5)

    def Initialize(self, initializer):
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, self.MaxLife)
        Action.Call(sequence, self.Death)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)

        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Owner.Sprite.CurrentFrame >= self.Frame:
            self.Death()
    
    def Death(self):
        self.Owner.Destroy()       

Zero.RegisterComponent("AnimationOnce", AnimationOnce)