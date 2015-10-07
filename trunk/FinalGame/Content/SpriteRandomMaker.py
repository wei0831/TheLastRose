import Zero
import Events
import Property
import VectorMath
import random
import math
Vec4 = VectorMath.Vec4

class SpriteRandomMaker:
    def Initialize(self, initializer):
        self.Owner.Transform.Scale *= random.random()*.7 + 0.5
        
        color_shader = random.random()*.7 + 0.3
        self.Owner.Sprite.Color *= Vec4(color_shader, color_shader, color_shader,1)
        self.Owner.Sprite.FlipX = random.random() > 0.5
        
        self.Owner.Transform.RotateByAngles(VectorMath.Vec3(0,0,math.pi / 6 * (random.random()-.5)))
        

Zero.RegisterComponent("SpriteRandomMaker", SpriteRandomMaker)