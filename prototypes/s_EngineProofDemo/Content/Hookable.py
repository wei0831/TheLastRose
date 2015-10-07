import Zero
import Events
import Property
import VectorMath

class Hookable:
    Active = Property.Bool(False)
    NonActivatable = Property.Bool(False)
    def Initialize(self, initializer):
        if self.NonActivatable:
            self.Active = False
        
    def Hook(self, target):
        if self.Owner.TimedDeath:
            self.Owner.TimedDeath.Active = False
        if self.Active:
            if self.Owner.Teleportable:
                self.Owner.Teleportable.Active = False
            self.Owner.AttachToRelative(target)
            self.Owner.RigidBody.Static = True
            if not self.Owner.CanCollect:
                self.Owner.AddComponentByName("CanCollect")

            
    def UnHook(self):
        self.Owner.RigidBody.Static = False
        self.Owner.DetachRelative()
        if self.Owner.Teleportable:
                self.Owner.Teleportable.Active = True
        if self.Owner.TimedDeath:
            self.Owner.TimedDeath.Active = True
        if self.Owner.CanCollect:
            self.Owner.RemoveComponentByName("CanCollect")
        
Zero.RegisterComponent("Hookable", Hookable)
