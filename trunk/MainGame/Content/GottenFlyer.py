import Zero
import Events
import Property
import VectorMath
import Action
class GottenFlyer:
    FlyingDelay = Property.Float(.5)
    def Initialize(self, initializer):
        self.CurrentUpdate = self.UpUpdate
        self.camera = self.Space.FindObjectByName("Camera")
        Zero.Connect(self.Space,Events.LogicUpdate,self.OnLogicUpdate)
        
    def UpUpdate(self):
        self.Owner.Transform.Scale *= 1.02
        if self.Owner.RigidBody.Velocity.y < 0:
            self.CurrentUpdate = self.WaitUpdate
            
            seq = Action.Sequence(self.Owner.Actions)
            Action.Delay(seq, self.FlyingDelay)
            def ToDown():
                self.CurrentUpdate = self.DownUpdate
            Action.Call(seq, ToDown)
                
    def WaitUpdate(self):
        self.Owner.RigidBody.AngularVelocity *= 0.95
        self.Owner.RigidBody.Velocity = VectorMath.Vec3(0,0,0)
        
        
    def DownUpdate(self):
        self.Owner.Sprite.Color *= VectorMath.Vec4(1,1,1,0.9)
        for child in self.Owner.Hierarchy.Children:
            if child.Sprite:
                child.Sprite.Color *= VectorMath.Vec4(1,1,1,0.92)
        
        self.Owner.Transform.Scale *= 0.95
        destination = self.camera.Transform.Translation + VectorMath.Vec3(8,-2.2,0)
        
        
        t = self.Owner.Transform.Translation
        kept_ratio = 0.95
        self.Owner.Transform.Translation = t * kept_ratio + destination * (1-kept_ratio)
    
    def OnLogicUpdate(self, UpdateEvent):
        self.CurrentUpdate()
        


Zero.RegisterComponent("GottenFlyer", GottenFlyer)