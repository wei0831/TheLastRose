import Zero
import Events
import Property
import VectorMath
import Action
class ValuePresenter:
    CollectibleTable = Property.ResourceTable("CollectibleTable")
    RegisterTo = Property.Cog()
    
    def Initialize(self, initializer):
        self.hudmanager = self.Space.FindObjectByName("LevelSettings").HUDManager
        self.hudmanager.RegisterScoreObserver(self.OnUpdateScore)
        
        if self.RegisterTo:
            self.RegisterTo.ValuePresenter.RegisterObserver(self.Owner)
        
        self.EnsureObservers()
        
        seq = Action.Sequence(self.Owner.Actions)
        Action.Call(seq, lambda: self.OnUpdateScore(0))
        
        
    def UpdateMax(self):
        levelnum = self.hudmanager.GetParentSpace().CurrentLevel.Name[5]
        if levelnum in "123": 
            self.max = self.CollectibleTable.FindValue(self.hudmanager.GetParentSpace().CurrentLevel.Name[5])
            if self.Owner.SpriteText.Text == '-':
                self.Owner.SpriteText.Text = '0/' + self.max
        else:
            self.max = ""
            self.Owner.SpriteText.Text = '-'
            
            
        for child in self.observers:
            child.ValuePresenter.UpdateMax()
    def Null(self):
        pass
        
    def EnsureObservers(self):
        self.observers = []
        self.EnsureObservers = self.Null
    
    def RegisterObserver(self, observer):
        self.EnsureObservers()
        self.observers.append(observer)
    
    def OnUpdateScore(self, new_score):
        self.EnsureObservers()
        self.UpdateMax()
        if self.max:
            self.Owner.SpriteText.Text = str(new_score) + '/' + self.max
            for child in self.observers:
                child.ValuePresenter.OnUpdateScore(new_score)

        
        
    

Zero.RegisterComponent("ValuePresenter", ValuePresenter)