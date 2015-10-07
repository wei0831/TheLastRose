import Zero
import Events
import Property
import VectorMath
import Action
import math
import random
Vec3 = VectorMath.Vec3

class AbiltySoulBehavior:
    CurrentUpdate = 0
    InitalPosition = 0
    MoveSpeed = 0.3
    ReleaseToExplodeTime = 1
    Timer = 0
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.CurrentUpdate = self.InitalState
        self.InitalPosition = self.Owner.Transform.Translation
        self.hero = self.Space.FindObjectByName("Hero")
                
    def OnLogicUpdate(self, UpdateEvent):
        if(self.CurrentUpdate != 0):
            self.CurrentUpdate(UpdateEvent)
    
    def InitalState(self, UpdateEvent):
        self.Owner.RigidBody.ApplyLinearVelocity(Vec3(0, self.MoveSpeed, 0));
        self.Timer += UpdateEvent.Dt
        if(self.Timer > self.ReleaseToExplodeTime):
            self.Owner.RigidBody.Velocity = Vec3(0, 0, 0)
            Timer = 0
            self.CurrentUpdate = self.ExplodeState
        
    def ExplodeState(self, UpdateEvent):
        self.Owner.SphericalParticleEmitter.Size -= UpdateEvent.Dt * 2.5
        if(self.Owner.SphericalParticleEmitter.Size <= 0.1):
            self.CurrentUpdate = 0
            sequence = Action.Sequence(self.Owner.Actions)
            Action.Delay(sequence, 0.5)
            Action.Call(sequence, self.EndState)
    
    def EndState(self):
        pos = self.Owner.Transform.Translation
        pos.z = 0
        
        souls = []
        for x in range(10):
            souls.append(self.Space.CreateAtPosition("SoulEffect", pos))
            
        for item in souls:
            item.SoulBehavior.SetDelayedTarget(self.hero, 0.75)
            #item.SoulBehavior.SetDelayedIncreaseSpeed(15, 0.75)
            #item.SoulBehavior.SetHomeInAngle(1)

        self.Owner.Destroy()            

Zero.RegisterComponent("AbiltySoulBehavior", AbiltySoulBehavior)