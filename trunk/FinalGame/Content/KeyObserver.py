import Zero
import Events
import Property
import VectorMath

class KeyObserver:
    PicTable = Property.ResourceTable()
    
    def Initialize(self, initializer):
        self.LevelName = ""
        self.parentspace = None
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def EnsureKey(self):
        self.LevelName = self.parentspace.CurrentLevel.Name
        self.key_status = self.parentspace.FindObjectByName("Player").KeyRing
        
    def EnsureSetting(self):
        self.parentspace = self.Space.FindObjectByName("LevelSettings").HUDManager.GetParentSpace()
        self.EnsureKey()
        
        self.EnsureSetting = lambda: None
    
    def OnLogicUpdate(self, UpdateEvent):
        self.EnsureSetting()
        
        if not self.LevelName == self.parentspace.CurrentLevel.Name:
            self.EnsureKey()
            
        sets = self.key_status.GetKeySet()
        has_key = False
        
        for child in self.Owner.Hierarchy.Children:
            child.Sprite.Color *= VectorMath.Vec3(1,1,1,0.9)
            
        for key, child in zip(sets, self.Owner.Hierarchy.Children):
            has_key = True
            c = child.Sprite.Color
            child.Sprite.Color = VectorMath.Vec3(c.x, c.y, c.z, c.a + 0.1)
            child.Sprite.SpriteSource = self.PicTable.FindResource(key)
            

Zero.RegisterComponent("KeyObserver", KeyObserver)