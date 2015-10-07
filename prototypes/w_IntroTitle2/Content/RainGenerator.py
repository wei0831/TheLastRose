import Zero
import Events
import Property
import VectorMath
import random

Vec3 = VectorMath.Vec3

class RainGenerator:
    Active = Property.Bool(True)
    
    CoolDown = Property.Float(0.25)
    AmountEachTime = Property.Int(10)
    Timer = 0

    Speed_DirX_Min = Property.Float(0)
    Speed_DirX_Max = Property.Float(2)
    Speed_DirY_Min = Property.Float(-2)
    Speed_DirY_Max = Property.Float(2)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.LowerLeft = self.Owner.Transform.WorldTranslation + Vec3(-self.Owner.Transform.WorldScale.x/2.0, -self.Owner.Transform.WorldScale.y/2.0, 0)
        self.UpperRight = self.Owner.Transform.WorldTranslation + Vec3(self.Owner.Transform.WorldScale.x/2.0, self.Owner.Transform.WorldScale.y/2.0, 0)
        
    def OnLogicUpdate(self, UpdateEvent):
        if not self.Active: return
        self.Timer += UpdateEvent.Dt
        
        if self.Timer > self.CoolDown:
            self.Timer = 0
            self.Rain()

        
    def Rain(self):
        for i in range(self.AmountEachTime):
            self.GenerateRain()
                
    def GenerateRain(self):
        creatAt = Vec3(random.uniform(self.LowerLeft.x, self.UpperRight.x), random.uniform(self.LowerLeft.y, self.UpperRight.y), 0)
        obj = self.Space.CreateAtPosition("Rain", creatAt)
        obj.RigidBody.Velocity = Vec3(random.randint(self.Speed_DirX_Min, self.Speed_DirX_Max), random.randint(self.Speed_DirY_Min, self.Speed_DirY_Max), 0)

Zero.RegisterComponent("RainGenerator", RainGenerator)