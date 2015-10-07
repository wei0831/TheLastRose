import Zero
import Events
import Property
import VectorMath
import Action
class Bounceable:
    Decay = Property.Float(1)
    Active = Property.Bool(True)
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "BounceEvent", self.OnBounce)
        
    def OnBounce(self, BounceEvent):
        if self.Active:
            
            if self.Owner.PlayerController:
                self.Owner.PlayerController.TriggerBounced()
            Vx = BounceEvent.ForcedVx
            Vy = BounceEvent.ForcedVy
            
            self_v = self.Owner.RigidBody.Velocity
            self_v.x = self_v.x if Vx == 0 else Vx
            self_v.y = self_v.y if Vy == 0 else Vy
            self.Owner.RigidBody.Velocity = self_v * self.Decay

            if self.Owner.PlayerController and abs(Vx) > (Vy) * .9:
                self.Owner.PlayerController.LockHorizontal()
                
                seq = Action.Sequence(self.Owner.Actions)
                Action.Delay(seq, .35)
                Action.Call(seq, self.Owner.PlayerController.UnlockHorizontal)
        
Zero.RegisterComponent("Bounceable", Bounceable)