import Zero
import Events
import Property
import VectorMath
import math
class CanBeRooted:
    ShouldRoot = Property.Bool(True)
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        self.normal = VectorMath.Vec3(0,0,0)
        
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.GrowableGround or CollisionEvent.OtherObject.PlantAnnihilator:
            
            self.normal = - CollisionEvent.FirstPoint.WorldNormalTowardsOther
            self.normal.z = 0
            
            self.Owner.Transform.Translation += self.normal * CollisionEvent.FirstPoint.Penetration
            if self.ShouldRoot:
                #self.Owner.Transform.RotateByAngles(VectorMath.Vec3(0,0,self.normal.angleZ()-math.pi/2))
                #CollisionEvent.OtherObject.Transform.Rotation
                self.Owner.RigidBody.Kinematic = True
                
            #if self.Owner.CanBounce:
                #self.Owner.CanBounce.ToDirection(self.normal)
                
            Zero.Disconnect(self.Owner, Events.CollisionStarted, self)
            
    def GetNormal(self):
        return self.normal
            

Zero.RegisterComponent("CanBeRooted", CanBeRooted)