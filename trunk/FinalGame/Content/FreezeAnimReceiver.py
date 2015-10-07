import Zero
import Events
import Property
import VectorMath

class FreezeAnimReceiver:
    AnimTable = Property.ResourceTable()
    
    def Initialize(self, initializer):
        self.Activated = False
        
        
    def Freeze(self):
        self.Activated = True
        self.Owner.Sprite.SpriteSource = self.AnimTable.FindValue("Frozen")
        
        #ice = self.Space.CreateAtPosition("IceParticle", self.Owner.Transform.WorldTranslation)
        #ice.TimedDeath.Active = True
        
    def IsActivated(self):
        return self.Activated
        
    
        

Zero.RegisterComponent("FreezeAnimReceiver", FreezeAnimReceiver)