import Zero
import Events
import Property
import VectorMath
import Action
import math
import random
import Color
Vec3 = VectorMath.Vec3

class AbilitySoulBehavior:
    MoveSpeed = Property.Float(10)
    ReleaseToExplodeTime = Property.Float(0.05)
    NoMoving = Property.Bool(False)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.CurrentUpdate = self.InitialState
        self.InitialPosition = self.Owner.Transform.Translation
        self.TrackingTarget = self.Space.FindObjectByName("Player")

        self.Timer = 0
                
    def OnLogicUpdate(self, UpdateEvent):
        if self.CurrentUpdate:
            self.CurrentUpdate(UpdateEvent)
    
    def InitialState(self, UpdateEvent):
        self.Owner.RigidBody.ApplyLinearVelocity(Vec3(0, self.MoveSpeed, 0));
        self.Timer += UpdateEvent.Dt
        if self.Timer > self.ReleaseToExplodeTime:
            self.Owner.RigidBody.Velocity = Vec3(0, 0, 0)
            self.CurrentUpdate = self.ExplodeState
        
    def ExplodeState(self, UpdateEvent):
        #self.Owner.SphericalParticleEmitter.Size -= UpdateEvent.Dt * 10
        #if self.Owner.SphericalParticleEmitter.Size <= 1:
        self.CurrentUpdate = None
        sequence = Action.Sequence(self.Owner)
        Action.Delay(sequence, 0.5)
        
        def SetState():
            self.CurrentUpdate = self.EndState
        Action.Call(sequence, SetState)
    
    def EndState(self, UpdateEvent):
        pos = self.Owner.Transform.Translation
        pos.z = 0
        if not self.NoMoving:
            self.Owner.Transform.Translation = pos * 0.9 + self.TrackingTarget.Transform.Translation * 0.1
        self.Owner.SphericalParticleEmitter.Size *= 0.9
            
        if self.Owner.SphericalParticleEmitter.Size < 0.1 and self.Owner.CanTransferAbility.IsActivated():
            souls = tuple(self.Space.CreateAtPosition("SoulEffect", self.TrackingTarget.Transform.Translation) for _ in range(20))
            for item in souls:
                item.SphericalParticleEmitter.Size = 0.3
                item.SoulBehavior.WillDecay = True
                item.SpriteParticleSystem.Tint = self.Owner.SpriteParticleSystem.Tint
            self.Owner.Destroy()
            

        #self.Owner.Destroy()            

Zero.RegisterComponent("AbilitySoulBehavior", AbilitySoulBehavior)