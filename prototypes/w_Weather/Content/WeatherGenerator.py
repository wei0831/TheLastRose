import Zero
import Events
import Property
import VectorMath
import random

Vec3 = VectorMath.Vec3

class RainGenerator:
    CoolDown = Property.Float(0.25)
    Timer = 0
    Amount = Property.Int(10)
    SpeedVariation = Property.Float(-10)
    Active = Property.Bool(True)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Space, Events.MouseMove, self.OnMouseMove)
        
        self.LowerLeft = self.Owner.Transform.WorldTranslation + Vec3(-self.Owner.Transform.WorldScale.x/2.0, -self.Owner.Transform.WorldScale.y/2.0, 0)
        self.UpperRight = self.Owner.Transform.WorldTranslation + Vec3(self.Owner.Transform.WorldScale.x/2.0, self.Owner.Transform.WorldScale.y/2.0, 0)
        
    def OnLogicUpdate(self, UpdateEvent):
        if not self.Active: return
        self.Timer += UpdateEvent.Dt
        
        if self.Timer > self.CoolDown:
            self.Timer = 0
            self.Rain()
        
    def OnMouseMove(self, MouseEvent):
        #print(MouseEvent.ToWorldZPlane(0.0))
        #self.Rain()
        pass
    
    def Rain(self):
        for i in range(self.Amount):
            self.GenerateRain()
                
    def GenerateRain(self):
        creatAt = Vec3(random.uniform(self.LowerLeft.x, self.UpperRight.x), random.uniform(self.LowerLeft.y, self.UpperRight.y), 0)
        obj = self.Space.CreateAtPosition("Rain", creatAt)
        obj.RigidBody.Velocity = Vec3(0, random.randint(self.SpeedVariation, 0), 0)

Zero.RegisterComponent("RainGenerator", RainGenerator)