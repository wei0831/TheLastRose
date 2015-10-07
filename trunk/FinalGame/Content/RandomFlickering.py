import Zero
import Events
import Property
import VectorMath
Vec4 = VectorMath.Vec4
import math
import random
class RandomFlickering:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.sum = random.random() * 10
        
        self.sudden_black_countdown = 0
        
    def OnLogicUpdate(self, UpdateEvent):
        self.sum += UpdateEvent.Dt * (random.random() + .5) * 1.2 + (random.random()-0.5) / 4 + (10 if random.randint(1,60) == 1 else 0)
        da = math.cos(self.sum)/3.2  + 0.4
        
        if int(random.random()*1500) == 1:
            self.sudden_black_countdown = 2
        self.sudden_black_countdown -= 1 if self.sudden_black_countdown > 0 else 0
        
        if self.Owner.Sprite:
            c = self.Owner.Sprite.Color
            if self.sudden_black_countdown == 0:
                if c.a < 0.05:
                    self.Owner.Sprite.Color = Vec4(c.x,c.y,c.z,0.25)
                else:
                    self.Owner.Sprite.Color = Vec4(c.x,c.y,c.z,.98*c.a + .02*da)
            else:
                c = self.Owner.Sprite.Color
                self.Owner.Sprite.Color = Vec4(c.x,c.y,c.z,.1*c.a)
        if self.Owner.Hierarchy:
            for child in self.Owner.Hierarchy.Children:
                #if not child.Name == "Door":
                if self.sudden_black_countdown == 0:
                    c = child.Sprite.Color
                    if c.a < 0.05:
                        child.Sprite.Color = Vec4(c.x,c.y,c.z,0.25)
                    else:
                        child.Sprite.Color = Vec4(c.x,c.y,c.z,.98*c.a + .02*da)
                else:
                    c = child.Sprite.Color
                    child.Sprite.Color = Vec4(c.x,c.y,c.z,.1*c.a)
                    
                if child.Hierarchy:
                    for ch in child.Hierarchy.Children:
                        if self.sudden_black_countdown == 0:
                            
                            c = ch.Sprite.Color
                            if c.a < 0.05:
                                ch.Sprite.Color = Vec4(c.x,c.y,c.z,0.25)
                            else:
                                ch.Sprite.Color = Vec4(c.x,c.y,c.z,.98*c.a + .02*da)
                        else:
                            c = child.Sprite.Color
                            child.Sprite.Color = Vec4(c.x,c.y,c.z,.1*c.a)
                    
        
        
Zero.RegisterComponent("RandomFlickering", RandomFlickering)