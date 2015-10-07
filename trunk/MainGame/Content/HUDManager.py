import Zero
import Events
import Property
import VectorMath
import Action
Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class HUDManager:
    MusicTable = Property.ResourceTable()
    
    def Initialize(self, initializer):
        self.ParentSpace = None
        
        self.MusicActive = False
        self.MusicName = ""
        self.Camera = self.Space.FindObjectByName("Camera")
        
        self.Hider = self.Space.CreateAtPosition("Sprite", self.Camera.Transform.Translation)
        self.Hider.AttachToRelative(self.Camera)
        self.Hider.Transform.Translation -= Vec3(0,0,50)
        self.Hider.Sprite.Color = Vec4(0,0,0,0)
        self.Hider.Transform.Scale = Vec3(100,100,1)
         
        self.Player = None

        self.skillnames =None
        
        self.final_alpha = 0
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    
    def PlayMusicFor(self, LevelName):
        mn = self.MusicTable.FindValue(LevelName)
        if mn != self.MusicName:
            self.PlayMusic(mn)
        
    
    def GetParentSpace(self):
        return self.ParentSpace
        
    def SetParentSpace(self,space):
        self.ParentSpace = space
        self.Player = self.ParentSpace.FindObjectByName("Player")
    
    def HideAll(self):
        self.Owner.CameraViewport.Layer = -1
        
    def ShowAll(self):
        self.Owner.CameraViewport.Layer = 1
        
    def PlayMusic(self, MusicName):
        self.MusicActive = True
        self.MusicName = MusicName
        self.Space.SoundSpace.PlayMusic(self.MusicName)
    
    def GetMusicName(self):
        return self.MusicName
        
    def MusicActive(self):
        return self.MusicActive
        
    def StopMusic(self):
        self.MusicActive = False
        self.Space.SoundSpace.StopMusic()
    
    def SetHiderAlpha(self, final_alpha):
        c = self.Hider.Sprite.Color
        self.Hider.Sprite.Color = Vec4(c.x, c.y, c.z, c.a * 0.9 + final_alpha * 0.1)
        
        if abs(final_alpha - c.a) > 0.05:
            Action.Call(self.sequence, self.SetHiderAlpha, final_alpha)
        else:
            self.Hider.Sprite.Color = Vec4(c.x,c.y,c.z,final_alpha)
            
        
        
    def OnLogicUpdate(self, UpdateEvent):            
        
        if Zero.Keyboard.KeyIsPressed(Zero.Keys.Escape):
            if self.ParentSpace:
                self.ParentSpace.TimeSpace.TogglePause()
                self.final_alpha = .8 if self.ParentSpace.TimeSpace.Paused else 0
        
        c = self.Hider.Sprite.Color
        if abs(self.final_alpha - c.a) > 0.05:
            self.Hider.Sprite.Color = Vec4(c.x, c.y, c.z, c.a * 0.6 + self.final_alpha * 0.4)
        else:
            self.Hider.Sprite.Color = Vec4(c.x,c.y,c.z,self.final_alpha)
            
    def CacheSkills(self):
        
        ts = self.Player.AbilityStatus.GetTreeSkillName()
        ps = self.Player.AbilityStatus.GetPhysSkillName()
        self.skillnames = (ts, ps)
        
    def GetBackSkill(self):
        if self.skillnames:
            self.Player.AbilityStatus.SwapTreeSkill(self.skillnames[0])
            self.Player.AbilityStatus.SwapPhysSkill(self.skillnames[1])
        
    
Zero.RegisterComponent("HUDManager", HUDManager)