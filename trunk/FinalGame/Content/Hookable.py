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
    
    def UpdatePosition(self, UpdateEvent):
        destination = VectorMath.Vec3(.2,.59,0) if not self.Owner.Parent.Sprite.FlipX else VectorMath.Vec3(-.2,.59,0)
        
        self.Owner.Transform.Translation = 0.95 * self.Owner.Transform.Translation + 0.05 * destination
        #if self.Owner.Parent.Sprite.FlipX = True
        #self.Owner.Transform.Translation
    def Hook(self, target):
        self.Space.SoundSpace.PlayCue("GrabCue")
        if self.Owner.TimedDeath:
            self.Owner.TimedDeath.Active = False
        if self.Active:
            if self.Owner.Teleportable:
                self.Owner.Teleportable.Active = False
            
            self.Owner.AttachToRelative(target)
            self.Owner.RigidBody.Static = True
            if not self.Owner.CanCollect:
                self.Owner.AddComponentByName("CanCollect")
                
            Zero.Connect(self.Space, Events.LogicUpdate, self.UpdatePosition)
        
    def UnHook(self):
        self.Owner.RigidBody.Static = False
        self.Owner.DetachRelative()
        if self.Owner.Teleportable:
            self.Owner.Teleportable.Active = True
        if self.Owner.TimedDeath:
            self.Owner.TimedDeath.Active = True
        if self.Owner.CanCollect:
            self.Owner.RemoveComponentByName("CanCollect")
            
        Zero.Disconnect(self.Space, Events.LogicUpdate, self)
            
    
        
        
Zero.RegisterComponent("Hookable", Hookable)
