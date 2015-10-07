import Zero
import Events
import Property
import VectorMath

Vec4 = VectorMath.Vec4

class AbilityObserver:
    ObserveType = Property.String("")
    PicTable = Property.ResourceTable()
    
    def Initialize(self, initializer):
        self.now_ability = ""
        self.LevelName = ""
        self.parentspace = None
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def EnsureAbility(self):
        self.ability_status = self.parentspace.FindObjectByName("Player").AbilityStatus
        self.GetName = self.ability_status.GetTreeSkillName if self.ObserveType == "Tree" else self.ability_status.GetPhysSkillName        
        self.LevelName = self.parentspace.CurrentLevel.Name
        
    def EnsureSetting(self):
        self.parentspace = self.Space.FindObjectByName("LevelSettings").HUDManager.GetParentSpace()
        self.LevelName = self.parentspace.CurrentLevel.Name
        self.EnsureAbility()
        
        self.EnsureSetting = lambda: None
    
    def OnLogicUpdate(self, UpdateEvent):
        self.EnsureSetting()
        
        if not self.LevelName == self.parentspace.CurrentLevel.Name:
            self.EnsureAbility()
            
        
        if self.now_ability != self.GetName():
            c = self.Owner.Sprite.Color
            self.Owner.Sprite.Color *= Vec4(1,1,1,0.9)
            if self.Owner.Sprite.Color.a <= 0.01:
                self.Owner.Sprite.SpriteSource = self.PicTable.FindValue(self.GetName())
                self.now_ability = self.GetName()
        else:
            c = self.Owner.Sprite.Color
            self.Owner.Sprite.Color = VectorMath.Vec4(c.x, c.y, c.z, c.a * 0.9 + 0.1)

        
        

Zero.RegisterComponent("AbilityObserver", AbilityObserver)