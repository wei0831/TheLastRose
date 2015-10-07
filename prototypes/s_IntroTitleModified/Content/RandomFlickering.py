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
    def OnLogicUpdate(self, UpdateEvent):
        self.sum += UpdateEvent.Dt * (random.random() + .5) * 1.3 + (random.random()-0.5) / 4 + (10 if random.randint(1,60) == 1 else 0)
        da = math.cos(self.sum)/4.  + 0.4
        for child in self.Owner.Hierarchy.Children:
            if not child.Name == "Door":
                c = child.Sprite.Color
                child.Sprite.Color = Vec4(c.x,c.y,c.z,.98*c.a + .02*da)
            if child.Hierarchy:
                for ch in child.Hierarchy.Children:
                    c = ch.Sprite.Color
                    ch.Sprite.Color = Vec4(c.x,c.y,c.z,.98*c.a + .02*da)
                
        
        
Zero.RegisterComponent("RandomFlickering", RandomFlickering)