import Zero
import Events
import Property
import VectorMath
import math
import random
Vec3 = VectorMath.Vec3

class SoulBehavior:
    SoulMoveSpeed = 10
    FrontDirection = Vec3(0, 0, 0)
    AngleChangeRate = 0.03
    MinRange = 10
    MaxAngleDelta = 1.0
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        self.Target = 0
        self.FrontDirection = Vec3(random.uniform(-10, 10), random.uniform(-10, 10), 0)
        
    def OnLogicUpdate(self, UpdateEvent):
        if(self.Target != 0):
            towardVector = self.Target.Transform.Translation - self.Owner.Transform.Translation
            towardVector.z = 0
            length = towardVector.length()
            
            if(length < self.MinRange):
                self.AngleChangeRate = self.MaxAngleDelta

            towardVector.normalize()
            self.FrontDirection.normalize()
            cosTheta = self.FrontDirection.dot(towardVector)
            cosTheta = 1.0 if cosTheta > 1 else cosTheta
            theta = math.acos(cosTheta)

            zDir = self.FrontDirection.cross(towardVector)
            if(zDir.z > 0):
                self.FrontDirection = Vec3.RotateVector(self.FrontDirection, Vec3(0, 0, 1), theta * self.AngleChangeRate)
            else:
                self.FrontDirection = Vec3.RotateVector(self.FrontDirection, Vec3(0, 0, -1), theta * self.AngleChangeRate)
                
        self.ApplyMovement()        

    def ApplyMovement(self):
        self.FrontDirection.normalize()
        self.Owner.RigidBody.Velocity = (self.FrontDirection * self.SoulMoveSpeed)
        self.Owner.LinearParticleAnimator.Force = self.Owner.RigidBody.Velocity * -1
        self.Owner.LinearParticleAnimator.RandomForce = self.Owner.RigidBody.Velocity * -1
            
    def OnCollision(self, CollideEvent):
        if(self.Target != 0 and CollideEvent.OtherObject == self.Target):
            self.Owner.Destroy()
            self.Space.CreateAtPosition("SoulHitEffect", CollideEvent.FirstPoint.WorldPoint)
        
    def SetTarget(self, target):
        self.Target = target
        
            

Zero.RegisterComponent("SoulBehavior", SoulBehavior)