import Zero
import Events
import Property
import VectorMath
import Action
Vec3 = VectorMath.Vec3
class PairManager:
    GoldPair = Property.Cog()
    HugeGoldPair = Property.Cog()
    SecretPair = Property.Cog()
    
    OriginalPlace = Property.Vector3(Vec3(-8,3,0))
    NewPlace = Property.Vector3(Vec3(-5,3,0))
    
    def Initialize(self, initializer):
        self.target = None
        self.childlist = (self.GoldPair,self.HugeGoldPair,self.SecretPair)
        self.seq = Action.Sequence(self.Owner.Actions)
        
        self.ResetAllPosition()
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def ResetAllPosition(self):
        self.target = None
        for child in self.childlist:
            child.Transform.WorldTranslation = self.OriginalPlace
            
    def OnLogicUpdate(self, UpdateEvent):
        
        for child in self.childlist:
            t = child.Transform.WorldTranslation
            place = self.OriginalPlace if not child is self.target else self.NewPlace
            child.Transform.WorldTranslation = 0.95 * t + 0.05 * place
            
    def ShowTarget(self, select):
        self.target = self.childlist[select] if not select is None else None
            
    def ShowOnce(self, select):
        self.ShowTarget(select)
        self.seq.Cancel()
        
        self.seq = Action.Sequence(self.Owner.Actions)
        Action.Delay(self.seq,2)
        Action.Call(self.seq, lambda:self.ShowTarget(None))
        
    def OnUpdateScore(self, score, type):
        self.ShowOnce(type)
        for child in self.childlist[type].Hierarchy.Children:
            if child.ValuePresenter:
                child.ValuePresenter.OnUpdateScore(score)
        
    def UpdateMax(self):
        for child in self.childlist:
            for c in child.Hierarchy.Children:
                if c.ValuePresenter:
                    c.ValuePresenter.UpdateMax()
Zero.RegisterComponent("PairManager", PairManager)