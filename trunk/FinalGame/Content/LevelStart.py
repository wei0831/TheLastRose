import Zero
import Events
import Property
import VectorMath
import Action
Vec4 = VectorMath.Vec4
import random
class LevelStart:
    
    HUDLevel = Property.Resource("Level")
    HUDManager = Property.Cog()
    AbilityOverrideTable = Property.ResourceTable("AbilityTimeOverrideTable")
    def Initialize(self, initializer):
        
        
        self.HUDSpace = Zero.Game.FindSpaceByName("HUDSpace")
        if not self.HUDSpace:
            self.HUDSpace = Zero.Game.CreateNamedSpace("HUDSpace", "Space")
            self.HUDSpace.LoadLevel(self.HUDLevel)
        
        self.HUDManager = self.HUDSpace.FindObjectByName("LevelSettings").HUDManager
        self.HUDManager.SetParentSpace(self.Space)
        self.HUDManager.ShowBoxes()
        
        
        self.HUDManager.HideScores()
        found = self.AbilityOverrideTable.FindValue(self.Space.CurrentLevel.Name)
        if found:
            override_time = float(found)
            player = self.Space.FindObjectByName("Player")
            player.AbilityStatus.PlantTimeOverride = override_time
        
        if self.Space.CurrentLevel.Name[0:3] == "Hub":
            self.HUDManager.ResetScores()
           
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)        
        
        self.HUDManager.UpdateMax()
        
        
        self.HUDManager.PlayMusicFor(self.Space.CurrentLevel.Name)
        #elif self.Space.CurrentLevel.Name == "Level3":
        #    self.Space.SoundSpace.PlayMusic("Cave")
        #    self.sequence = Action.Sequence(self.Owner.Actions)
        #    self.PlayAmbient()
        #elif self.Space.CurrentLevel.Name == "Level4" or self.Space.CurrentLevel.Name == "Level5":
        #    self.Space.SoundSpace.PlayMusic("SwampLoop")
            
            
        self.player = self.Space.FindObjectByName("Player")
        self.camera = self.Space.FindObjectByName("Camera")
        self.CurrentUpdate = self.UpdateCamera
        
        pt = self.player.Transform.WorldTranslation
        ct = self.camera.Transform.WorldTranslation
        self.camera.Transform.WorldTranslation = VectorMath.Vec3(pt.x, pt.y + 2.5, ct.z)
    
    def EnsureAbility(self):
        self.HUDManager.GetBackSkill()
        def Null():
            pass
        self.EnsureAbility = Null

    def PlayAmbient(self):
        sound = "DripCue" if random.randint(0,1) == 1 else "DripCue2"
        self.Space.SoundSpace.PlayCue(sound)
        
        Action.Delay(self.sequence,random.random()*7 + 7)
        Action.Call(self.sequence, self.PlayAmbient)
        
    def UpdateCamera(self):
        self.camera.CameraFunction.SetCameraFade(Vec4(1,1,1,1),Vec4(1,1,1,0),0.03,0)
        self.CurrentUpdate = self.UpdateKey
        
    def UpdateKey(self):
        pass
        #if Zero.Keyboard.KeyIsDown(Zero.Keys.Six):
        #    self.Space.LoadLevel("Level1")
        #elif Zero.Keyboard.KeyIsDown(Zero.Keys.Seven):
        #    self.Space.LoadLevel("Level2")
        #elif Zero.Keyboard.KeyIsDown(Zero.Keys.Eight):
        #    self.Space.LoadLevel("Level3")
        #elif Zero.Keyboard.KeyIsDown(Zero.Keys.Nine):
        #    self.Space.LoadLevel("Level4")
        #elif Zero.Keyboard.KeyIsDown(Zero.Keys.Zero):
        #    self.Space.LoadLevel("Level5")
        #elif Zero.Keyboard.KeyIsDown(Zero.Keys.Equal):
        #    self.player.HealthStatus.ResetHealth()
        #    self.player.HealthStatus.ResetRegen()
        #    self.player.BlinkAnim.Active = False
        #    self.player.HealthStatus.Updatable = False
        #elif Zero.Keyboard.KeyIsDown(Zero.Keys.Minus):
        #    self.player.HealthStatus.Updatable = True
            
    def OnLogicUpdate(self, UpdateEvent):
        print(self.GetCollectibleCount(), self.GetHugeCollectibleCount())
        self.EnsureAbility()
        self.CurrentUpdate()
        
        #self.GetCollectibleCount()
        #Zero.Disconnect(self.Space, Events.LogicUpdate, self)
        
    def GetCollectibleCount(self):
        return len(list(self.Space.FindAllObjectsByName("Gold")))
    def GetHugeCollectibleCount(self):
        return len(list(self.Space.FindAllObjectsByName("HugeGold")))
    def RemoveHUD(self):
        self.HUDSpace.Destroy()
Zero.RegisterComponent("LevelStart", LevelStart)
