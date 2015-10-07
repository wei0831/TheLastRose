import Zero
import Events
import Property
import VectorMath
import Action
Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4

class HUDManager:
    MusicTable = Property.ResourceTable("MusicTable")
    CollectibleTable = Property.ResourceTable("CollectibleTable")
    Menu = Property.Cog()
    Indicator = Property.Cog()
    ScoreUI = Property.Cog()
    PairUI = Property.Cog()
    SoundEmitter = Property.Cog()
    
    PBoxSmall = Property.Cog()
    PBoxLarge = Property.Cog()
    PBoxSmallBack = Property.Cog()
    PBoxLargeBack = Property.Cog()
    
    ForcedTreeSkill = Property.ResourceTable("ForcedTreeSkill")
    ForcedPhysSkill = Property.ResourceTable("ForcedPhysSkill")
    LevelJumpTable = Property.ResourceTable("LevelJumpTable")
    
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
         
        self.hiding_boxes = False
         
        self.Player = None
        self.skillnames =None

        self.final_alpha = 0
        
        self.EnsureReloadObserver()
        self.EnsureScores()
        self.EnsureScoreObservers()
    
        self.is_showing_credits = False
    
        self.PauseDisabled = False
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
    
    def RegisterReloadObserver(self, callback):
        self.reload_observers.append(callback)
    
    def Null(self):
        pass
    
    def EnsureReloadObserver(self):
        self.reload_observers = []
        self.EnsureReloadObserver = self.Null
    
    def ShowScores(self):
        self.cached_loc = self.ScoreUI.Transform.WorldTranslation
        self.PauseDisabled = True
        #self.ScoreUI.Transform.WorldTranslation = Vec3(3.5, 0.496,0)
        self.ScoreUI.HiderScript.Hide()
        self.HideBoxesSmooth()
        
    def HideScores(self):
        if self.ScoreUI:
            self.PauseDisabled = False
            self.ScoreUI.HiderScript.Unhide()
            #self.ScoreUI.Transform.WorldTranslation = self.cached_loc
            self.ShowBoxesSmooth()
    
    def PlayMusicFor(self, LevelName):
        mn = self.MusicTable.FindValue(LevelName)
        print(LevelName, mn, self.MusicName)
        
        if mn != self.MusicName:
            self.SoundEmitter.SoundEmitter.Stop()
            self.PlayMusic(mn)
            pass
            
    def EnsureScoreObservers(self):
        self.score_observers = []
        self.EnsureScoreObservers = self.Null
        
    def EnsureScores(self):
        self.scores = [0,0,0]
        self.EnsureScores = self.Null
        
    def AddScore(self, score, type):
        self.EnsureScores()
        self.scores[type] += score
        
        
        self.PairUI.PairManager.OnUpdateScore(self.scores[type], type)
        
    def UpdateMax(self):
        self.PairUI.PairManager.UpdateMax()
    
        
    def GetScore(self, score, type):
        return self.scores[type]
    
    def ResetScores(self):
        self.scores = [0,0,0]
    
    def RegisterScoreObserver(self, callback):
        self.EnsureScoreObservers()
        self.score_observers.append(callback)
    
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
        if MusicName:
            self.MusicActive = True
            self.MusicName = MusicName
            #self.Space.SoundSpace.PlayCue(self.MusicName)
            
            self.SoundEmitter.SoundEmitter.PlayCue(self.MusicName)
            #self.Space.SoundSpace.Volume = 0
        
    
    def GetMusicName(self):
        return self.MusicName
        
    def MusicActive(self):
        return self.MusicActive
        
    def StopMusic(self):
        self.MusicActive = False
        self.SoundEmitter.SoundEmitter.Stop()
    
    def SetHiderAlpha(self, final_alpha):
        c = self.Hider.Sprite.Color
        self.Hider.Sprite.Color = Vec4(c.x, c.y, c.z, c.a * 0.9 + final_alpha * 0.1)
        
        if abs(final_alpha - c.a) > 0.05:
            Action.Call(self.sequence, self.SetHiderAlpha, final_alpha)
        else:
            self.Hider.Sprite.Color = Vec4(c.x,c.y,c.z,final_alpha)
            

            
            
        
    def OnLogicUpdate(self, UpdateEvent):            
        
        if not self.PauseDisabled and Zero.Keyboard.KeyIsPressed(Zero.Keys.Escape):
            if self.ParentSpace.TimeSpace.Paused:
                self.Space.FindObjectByName("CreditShower").FadeAnim.FadeOut()
                self.is_showing_credits = False
                self.ResumeGame()
            else:
                self.PauseGame()
        
        self.final_alpha = .8 if self.ParentSpace.TimeSpace.Paused else 0
        c = self.Hider.Sprite.Color
        if abs(self.final_alpha - c.a) > 0.05:
            self.Hider.Sprite.Color = Vec4(c.x, c.y, c.z, c.a * 0.6 + self.final_alpha * 0.4)
        else:
            self.Hider.Sprite.Color = Vec4(c.x,c.y,c.z,self.final_alpha)
            
        if self.ParentSpace.TimeSpace.Paused:
            keypressed = Zero.Keyboard.KeyIsPressed(Zero.Keys.Space) or Zero.Keyboard.KeyIsPressed(Zero.Keys.Enter)
            buttonpressed = Zero.Mouse.IsButtonDown(Zero.MouseButtons.Left)
            
            if self.is_showing_credits:
                #pass
                if keypressed or buttonpressed:
                    self.ShowBoxes()
                    self.ScoreUI.Transform.WorldTranslation = self.score_UI_position
                    self.Menu.FadeAnim.FadeIn()
                    self.Indicator.FadeAnim.FadeIn()
                    self.Space.FindObjectByName("CreditShower").FadeAnim.FadeOut()
                    self.is_showing_credits = False
            
            elif not self.is_showing_credits:
                if Zero.Keyboard.KeyIsPressed(Zero.Keys.W) or Zero.Keyboard.KeyIsPressed(Zero.Keys.Up):
                    self.Menu.Menu.Increment()
                if Zero.Keyboard.KeyIsPressed(Zero.Keys.S) or Zero.Keyboard.KeyIsPressed(Zero.Keys.Down):
                    self.Menu.Menu.Decrement()
                    
                
                
                if keypressed or buttonpressed:
                    code = self.Menu.Menu.GetActionCode()
                    
                    if code == "RestartCheckPoint":
                        self.ResumeGame()
                        self.Player.CanFancyDie.Die()
                    elif code == "RestartLevel":
                        self.HideBoxes()
                        def reload_callback():
                            for callback in self.reload_observers:
                                callback()
                        
                        self.ResumeGame()
                        
                        self.ParentSpace.FindObjectByName("Camera").CameraFunction.SetCameraFade(Vec4(1,1,1,0),Vec4(1,1,1,1),.04,0)
                        self.Player.RigidBody.Kinematic = True
                        sequence = Action.Sequence(self.Owner.Actions)            
                        
                        Action.Delay(sequence, .8)
                        Action.Call(sequence, lambda:self.ParentSpace.LoadLevel(self.ParentSpace.CurrentLevel))
                        Action.Delay(sequence, .801)
                        Action.Call(sequence, reload_callback)
                    elif code == "ExitLevel":
                        self.ResumeGame()
                        
                        self.Player.RigidBody.Kinematic = True
                        self.ParentSpace.FindObjectByName("Camera").CameraFunction.SetCameraFade(Vec4(0,0,0,0),Vec4(0,0,0,1),.04,0)
                        sequence = Action.Sequence(self.ParentSpace.Actions)            
                        
                        Action.Delay(sequence, .8)
                        Action.Call(sequence, lambda:self.ParentSpace.LoadLevel("MenuScreen"))
                        
                        self.Space.Destroy()
                    elif code == "Credits":
                        self.Space.FindObjectByName("CreditShower").FadeAnim.FadeIn()
                        self.HideBoxesSmooth()
                        self.score_UI_position = self.ScoreUI.Transform.Translation 
                        self.ScoreUI.Transform.Translation = Vec3(7.836,0,0)
                        self.Menu.FadeAnim.FadeOut()
                        self.Indicator.FadeAnim.FadeOut()
                        
                        self.is_showing_credits = True
                        
                    elif code == "Exit":
                        self.ResumeGame()
                        self.Player.RigidBody.Kinematic = True
                        self.ParentSpace.FindObjectByName("Camera").CameraFunction.SetCameraFade(Vec4(0,0,0,0),Vec4(0,0,0,1),.06,0)
                        sequence = Action.Sequence(self.Owner.Actions)            
                        
                        Action.Delay(sequence, .5)
                        Action.Call(sequence, lambda:Zero.Game.Quit())
                    elif code == "Skip":
                        levelname = self.LevelJumpTable.FindValue(self.ParentSpace.CurrentLevel.Name)
                        if levelname:
                            
                            self.HideBoxes()
                            def reload_callback():
                                for callback in self.reload_observers:
                                    callback()
                            
                            self.ResumeGame()
                            self.CacheSkills()
                            self.ParentSpace.FindObjectByName("Camera").CameraFunction.SetCameraFade(Vec4(1,1,1,0),Vec4(1,1,1,1),.04,0)
                            self.Player.RigidBody.Kinematic = True
                            sequence = Action.Sequence(self.Owner.Actions)            
                            
                            Action.Delay(sequence, .8)
                            Action.Call(sequence, lambda:self.ParentSpace.LoadLevel(levelname))
                            Action.Delay(sequence, .801)
                            Action.Call(sequence, reload_callback)
                        
                        
                    elif code == "Resume":
                        self.ResumeGame()
                    
    def SetBoxVisible(self, visible):
        self.PBoxLarge.Sprite.Visible = visible
        self.PBoxSmall.Sprite.Visible = visible
        self.PBoxLargeBack.Sprite.Visible = visible
        self.PBoxSmallBack.Sprite.Visible = visible
        
    
    def HideBoxes(self):
        self.SetBoxVisible(False)
    def ShowBoxes(self):
        self.SetBoxVisible(True)
        
    def ResumeGame(self):
        if self.ParentSpace.TimeSpace.Paused:
            self.ParentSpace.TimeSpace.TogglePause()
            self.Menu.FadeAnim.FadeOut()
            self.Indicator.FadeAnim.FadeOut()
            self.ScoreUI.Transform.Translation = Vec3(7.836,0,0)
            
            
    def PauseGame(self):
        if not self.ParentSpace.TimeSpace.Paused:
            self.PairUI.PairManager.ResetAllPosition()
            self.ParentSpace.TimeSpace.TogglePause()
            self.Menu.FadeAnim.FadeIn()
            self.Indicator.FadeAnim.FadeIn()
            self.ScoreUI.Transform.Translation = Vec3(-4.902,2,0)
        
    def CacheSkills(self):
        
        ts = self.Player.AbilityStatus.GetTreeSkillName()
        ps = self.Player.AbilityStatus.GetPhysSkillName()
        self.skillnames = (ts, ps)
        
    def GetBackSkill(self):
        fts = self.ForcedTreeSkill.FindValue(self.ParentSpace.CurrentLevel.Name)
        fps = self.ForcedPhysSkill.FindValue(self.ParentSpace.CurrentLevel.Name)
        
        if self.skillnames:
            if not fts:
                fts = self.skillnames[0]
            if not fps:
                fps = self.skillnames[1]
            
        self.Player.AbilityStatus.SwapTreeSkill(fts)
        self.Player.AbilityStatus.SwapPhysSkill(fps)

    def HideBoxesSmooth(self):
        self.PBoxLarge.HiderScript.Hide()
        self.PBoxSmall.HiderScript.Hide()
        self.PBoxLargeBack.HiderScript.Hide()
        self.PBoxSmallBack.HiderScript.Hide()
        
    def ShowBoxesSmooth(self):
        self.PBoxLarge.HiderScript.Unhide()
        self.PBoxSmall.HiderScript.Unhide()
        self.PBoxLargeBack.HiderScript.Unhide()
        self.PBoxSmallBack.HiderScript.Unhide()
Zero.RegisterComponent("HUDManager", HUDManager)