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
        if self.Active:
            if self.Owner.Teleportable:
                self.Owner.Teleportable.Active = False
            self.Owner.AttachToRelative(target)
            self.Owner.RigidBody.Static = True
            
    def UnHook(self):
        self.Owner.RigidBody.Static = False
        self.Owner.DetachRelative()
        if self.Owner.Teleportable:
                self.Owner.Teleportable.Active = True
        
Zero.RegisterComponent("Hookable", Hookable)
