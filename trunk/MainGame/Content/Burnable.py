import Zero
import Events
import Property
import VectorMath
import Action
import Color
import Action
class Burnable:
    PropagateBurn = Property.Bool(True)
    HurtRate = Property.Float(0)
    Amplifier = Property.Float(1)
    PropagateDelay = Property.Float(0)
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, "BurnEvent", self.OnBurn)
        self.sequence = None
        
    def OnBurn(self, BurnEvent):
        if not self.Owner.BurnAnim:
            self.Owner.AddComponentByName("BurnAnim")
            self.Owner.BurnAnim.Active = True
            self.Owner.BurnAnim.Amplifier = self.Amplifier
        if self.PropagateBurn and not self.Owner.CanBurn:
            self.Owner.AddComponentByName("CanBurn")
            def BurnFriends():
                burnevent = Zero.ScriptEvent()
                for ch in self.Owner.Collider.Contacts:
                    ch.OtherObject.DispatchEvent("BurnEvent",burnevent)
            if not self.PropagateDelay:
                BurnFriends()
            else:
                seq = Action.Sequence(self.Owner.Actions)
                Action.Delay(seq, self.PropagateDelay)
                Action.Call(seq, BurnFriends)
             
        if self.HurtRate:
            if self.Owner.HealthStatus:    
                self.sequence = Action.Sequence(self.Owner.Actions)
                self.ContinueHurt()
                
        
    def ContinueHurt(self):
        self.Owner.HealthStatus.AddHealth(self.HurtRate)

        
        if not self.Owner.HealthStatus.IsDead():
        
            Action.Delay(self.sequence,0.2)
            Action.Call(self.sequence,self.ContinueHurt)
            if self.Owner.Sprite.Color == Color.Red:
                self.Owner.Sprite.Color = Color.White
            else:
                self.Owner.Sprite.Color = Color.Red
        else:        
            self.Owner.ClickReceiver.PerformDie()
            self.Owner.BurnAnim.Active = False
            self.Owner.CanBurn.Active = False
            self.Owner.Sprite.Color = Color.White
        
        
        
        


Zero.RegisterComponent("Burnable", Burnable)