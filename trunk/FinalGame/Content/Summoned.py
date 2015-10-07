import Zero
import Events
import Property
import VectorMath

class Summoned:
    Summoner = Property.Cog()
    def Initialize(self, initializer):
        self.HideAll()
        if self.Summoner:
            self.Summoner.TouchSummon.RegisterObserver(self.Owner)
    def RegisterTo(self, accepter):
        self.Summoner = accepter
        accepter.TouchSummon.RegisterObserver(self.Owner)
    def HideAll(self):
        for child in self.Owner.Hierarchy.Children:
            child.Sprite.Visible = False
            
    def ShowAll(self):
        for child in self.Owner.Hierarchy.Children:
            child.Sprite.Visible = True
            
Zero.RegisterComponent("Summoned", Summoned)