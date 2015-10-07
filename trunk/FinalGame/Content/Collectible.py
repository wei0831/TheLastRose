import Zero
import Events
import Property
import VectorMath

class Collectible:
    def Initialize(self, initializer):
        pass
    def Collected(self):
        
        if not self.Owner.Name == "Secret":
            self.Space.CreateAtPosition("GoldParticle", self.Owner.Transform.Translation)
            self.Space.SoundSpace.PlayCue(self.Owner.Name + "Cue")
        
        
        if self.Owner.DestroyInterface:
            self.Owner.DestroyInterface.Destroy()
        else:
            self.Owner.Destroy()
    def GetType(self):
        if self.Owner.Name == "Gold":
            return 0
        elif self.Owner.Name == "HugeGold":
            return 1
        elif self.Owner.Name == "Secret":
            return 2
        else: 
            return None
            
            
Zero.RegisterComponent("Collectible", Collectible)