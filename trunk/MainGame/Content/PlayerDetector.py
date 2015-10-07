import Zero
import Events
import Property
import VectorMath

class PlayerDetector:
    def Initialize(self, initializer):
        self.Player = self.Space.FindObjectByName("Player")
        self.WithInRange = False
        self.length = 0
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnd)
        
    def OnCollision(self, CollisionEvent):
        self.WithInRange = True
        
    def OnCollisionEnd(self, CollisionEvent):
        self.WithInRange = False
    def GetDirection(self):
        return self.Player.Transform.Translation - self.Owner.Transform.WorldTranslation
    def GetRange(self):
        return (self.Player.Transform.Translation - self.Owner.Transform.WorldTranslation).length()
    def InRange(self):
        if self.Player.CanFancyDie and not self.Player.CanFancyDie.Immune():
            return self.WithInRange
        else:
            return False
        
Zero.RegisterComponent("PlayerDetector", PlayerDetector)