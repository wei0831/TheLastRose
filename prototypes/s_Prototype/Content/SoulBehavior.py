import Zero
import Events
import Property
import VectorMath
import math
import random
import Action
Vec3 = VectorMath.Vec3

class SoulBehavior:
    SoulMoveSpeed = Property.Float(10)
    AngleChangeRate = Property.Float(0.025)
    WillDecay = Property.Bool(False)
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        self.Target = None
        self.FrontDirection = Vec3(random.uniform(-10, 10), random.uniform(-10, 10), 0)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Target:
            towardVector = self.Target.Transform.Translation - self.Owner.Transform.Translation
            towardVector.z = 0
            length = towardVector.length()

            if(length < 8):
                self.AngleChangeRate = 0.05
            if(length < 6):
                self.AngleChangeRate = 0.075
            if(length < 4):
                self.AngleChangeRate = 0.1
            if(length < 2):
                self.AngleChangeRate = 0.5
            if(length < 0.05):
                self.Owner.Destroy()

            towardVector.normalize()
            self.FrontDirection.normalize()
            cosTheta = self.FrontDirection.dot(towardVector)
            cosTheta = 1 if cosTheta > 1 else cosTheta
            cosTheta = -1 if cosTheta < -1 else cosTheta
            theta = math.acos(cosTheta)

            zDir = self.FrontDirection.cross(towardVector)
            if(zDir.z > 0):
                self.FrontDirection = Vec3.RotateVector(self.FrontDirection, Vec3(0, 0, 1), theta * self.AngleChangeRate)
            else:
                self.FrontDirection = Vec3.RotateVector(self.FrontDirection, Vec3(0, 0, -1), theta * self.AngleChangeRate)
                
        self.ApplyMovement()        
        
        if self.WillDecay:
            if self.Owner.SphericalParticleEmitter.Size > 0:
                self.Owner.SphericalParticleEmitter.Size -= 0.01
            elif self.Owner.SphericalParticleEmitter.Size < 0:
                self.Owner.SphericalParticleEmitter.Size = 0
            

    def ApplyMovement(self):
        self.FrontDirection.normalize()
        self.Owner.RigidBody.Velocity = (self.FrontDirection * self.SoulMoveSpeed) * 0.4 + self.Owner.RigidBody.Velocity * 0.6
        self.Owner.LinearParticleAnimator.Force = self.FrontDirection * -10
        self.Owner.LinearParticleAnimator.RandomForce = self.FrontDirection * -10
            
    def OnCollision(self, CollideEvent):
        if CollideEvent.OtherObject == self.Target:
            self.Owner.Destroy()
            self.Space.CreateAtPosition("SoulHitEffect", CollideEvent.FirstPoint.WorldPoint)
        
    def SetTarget(self, target):
        self.Target = target
        
    def SetDelayedTarget(self, target, delaytime):
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, delaytime)
        Action.Call(sequence, self.SetTarget, target)
    
    def SetHomeInAngle(self, angle):
        self.AngleChangeRate = angle
    
    def SetSpeed(self, speed):
        self.SoulMoveSpeed = speed
    
    def SetDelayedIncreaseSpeed(self, speed, delaytime):
        sequence = Action.Sequence(self.Owner.Actions)
        Action.Delay(sequence, delaytime)
        Action.Call(sequence, self.SetSpeed, speed)
        
            
Zero.RegisterComponent("SoulBehavior", SoulBehavior)