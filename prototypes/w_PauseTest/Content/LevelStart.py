import Zero
import Events
import Property
import VectorMath

class LevelStart:
    LevelHUD = Property.Resource("Level")
    
    def Initialize(self, initializer):
        self.HUDSpace = Zero.Game.CreateNamedSpace("HUDLevel", "Space")
        self.HUDSpace.LoadLevel(self.LevelHUD)
        ls = self.HUDSpace.FindObjectByName("LevelSettings")
        ls.Pause.Parent = self.Space
        
    def Destoryed(self):
        self.HUDSpace.Destory()

Zero.RegisterComponent("LevelStart", LevelStart)