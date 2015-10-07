import Zero
import Events
import Property
import VectorMath
import random
import Action
class BurnableVine:
    HurtRate = Property.Float(-80)
    CollisionToBe = Property.CollisionGroup()
    Delay = Property.Float(.1)
    def Initialize(self, initializer):
        if not self.Owner.CanHurt:
            self.Owner.AddComponentByName("CanHurt")
            self.Owner.CanHurt.HurtRate = self.HurtRate
            
        if not self.Owner.Burnable:
            self.Owner.AddComponentByName("Burnable")
            self.Owner.Burnable.PropagateDelay = .3
        
        self.BeginBurning = False
        
        Zero.Connect(self.Owner, "BurnEvent", self.OnBurn)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.disintegrated = False
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.BeginBurning:
            s = self.Owner.Sprite.Color 
            self.Owner.Sprite.Color = VectorMath.Vec4(s.x * 0.99, s.y * 0.99 , s.z * 0.99, 1)
            
            if s.x + s.y + s.z < 0.4:
                self.Owner.CanHurt.Active = False
                self.Owner.BurnAnim.GetAnim().SphericalParticleEmitter.EmitRate *= 0.98
            
            if s.x + s.y + s.z < 0.2 and not self.disintegrated:
                self.Owner.RigidBody.Static = False
                self.Owner.RigidBody.Kinematic = False
                self.disintegrated = True
                self.Owner.RigidBody.ApplyTorque(VectorMath.Vec3(0, 0,random.random()*5))
                self.Owner.Collider.CollisionGroup = self.CollisionToBe

            
            if s.x + s.y + s.z < 0.05:
                self.Owner.Sprite.Color *= VectorMath.Vec4(s.x, s.y, s.z, s.a * 0.9)
                
            if s.a < 0.05:
                if self.Owner.DestroyInterface:
                    self.Owner.DestroyInterface.Destroy()
                    Zero.Disconnect(self.Space, Events.LogicUpdate, self)
                else:
                     self.Owner.Destroy()
        
    def OnBurn(self, BurnEvent):
        self.BeginBurning = True
        #print(self.Owner.CanBurn)
        if not self.Owner.CanBurn:
            self.Owner.AddComponentByName("CanBurn")
            self.Owner.CanBurn.Active = False
        
            

Zero.RegisterComponent("BurnableVine", BurnableVine)