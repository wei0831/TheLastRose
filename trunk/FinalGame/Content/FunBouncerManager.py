import Zero
import Events
import Property
import VectorMath

class FunBouncerManager:
    def Initialize(self, initializer):
        self.position = VectorMath.Vec3(0.312, 0.206,0.012)
        self.flip_position = VectorMath.Vec3(-0.312, 0.206,0.012)
       
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        self.Owner.Transform.Translation = self.position if self.Owner.Parent.Sprite.FlipX else self.flip_position
        self.Owner.CanBounce.ForcedVx = 3 if self.Owner.Parent.Sprite.FlipX else -3
        self.Owner.CanBounce.ForcedVy = 2
        
            

Zero.RegisterComponent("FunBouncerManager", FunBouncerManager)