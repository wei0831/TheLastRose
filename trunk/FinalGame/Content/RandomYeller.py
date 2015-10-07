import Zero
import Events
import Property
import VectorMath
import random


VectorMath.Vec4()
class RandomYeller:
    Xrange = Property.Float(5)
    Yrange = Property.Float(5)
    #Active = Property.Bool(False)
    
    def Initialize(self, initializer):
        self.random_string = ["What are you doing!?", "Stop it!", "Don't do that!", "No! No!", "No!", "Stop!!", "What!?", "No, Stop!!", "Stop!! Stop!!", "It hurts!!", "What have you done?!", "STOP!", "NO!!"]
        pass
        

        
    def CreateOne(self):
        #if self.Active:
        x = self.Owner.Transform.WorldTranslation.x + (random.random()-0.5) * self.Xrange * 2
        y = self.Owner.Transform.WorldTranslation.y + (random.random()-0.5) * self.Yrange * 2
        
        yt = self.Space.CreateAtPosition("YellingTemplate", VectorMath.Vec3(x,y,1))
        yt.TypeScript.String = self.random_string[random.randint(0,len(self.random_string)-1)]
            
            
        
    
Zero.RegisterComponent("RandomYeller", RandomYeller)