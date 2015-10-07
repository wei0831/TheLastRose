import Zero
import Events
import Property
import VectorMath
import random
import Color
Vec3 = VectorMath.Vec3

class RainGenerator:
    CoolDown = Property.Float(0.25)
    Timer = 0
    Amount = Property.Int(10)
    SpeedVariation = Property.Float(-10)
    Activatable = Property.Bool(True)
    RainArchetype = Property.Archetype("Rain")
    RainShader = Property.Color(Color.LightBlue)
    ResourceSaver = Property.Bool(True)
    
    def Initialize(self, initializer):
        self.Active = True
        self.Player = self.Space.FindObjectByName("Player")
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.LowerLeft = self.Owner.Transform.WorldTranslation + Vec3(-self.Owner.Transform.WorldScale.x/2.0, -self.Owner.Transform.WorldScale.y/2.0, 0)
        self.UpperRight = self.Owner.Transform.WorldTranslation + Vec3(self.Owner.Transform.WorldScale.x/2.0, self.Owner.Transform.WorldScale.y/2.0, 0)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Activatable:
            if self.ResourceSaver:
                self.Active = abs(self.Owner.Transform.Translation.x - self.Player.Transform.Translation.x) < 10
            else:
                self.Active = True
                 
            if self.Active:
                self.Timer += UpdateEvent.Dt
                
                if self.Timer > self.CoolDown:
                    self.Timer = 0
                    self.Rain()
             
    
    def Rain(self):
        tuple(self.GenerateRain() for _ in range(self.Amount))
            
                
    def GenerateRain(self):
        creatAt = Vec3(random.uniform(self.LowerLeft.x, self.UpperRight.x), random.uniform(self.LowerLeft.y, self.UpperRight.y), 0)
        created = self.RainArchetype if self.RainArchetype else "Rain"
        obj = self.Space.CreateAtPosition(created, creatAt)
        obj.RigidBody.Velocity = Vec3(0, random.randint(self.SpeedVariation, 0), 0)
        for child in obj.Hierarchy.Children:
            child.Sprite.Color = self.RainShader
            child.Sprite.Color *= VectorMath.Vec4(1,1,1,0.2)
        
            

Zero.RegisterComponent("RainGenerator", RainGenerator)