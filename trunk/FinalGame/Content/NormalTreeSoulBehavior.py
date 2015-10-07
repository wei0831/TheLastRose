import Zero
import Events
import Property
import VectorMath
import Action
Vec4 = VectorMath.Vec4
Vec3 = VectorMath.Vec3
class NormalTreeSoulBehavior:
    DestinationObject = Property.Cog()
    VerticalDetect = Property.Bool(False)
    ExtendedDelay = Property.Bool(False)
    ShadingColor = Property.Color(VectorMath.Vec4(1,1,1,1))
    def Initialize(self, initializer):
        self.camera = self.Space.FindObjectByName("Camera")
        self.CurrentUpdater = self.Detecting
        self.Player = self.Space.FindObjectByName("Player")
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.CollisionStart)
        
        
    def CollisionStart(self, CollisionEvent):
        if CollisionEvent.OtherObject == self.Player:
            self.Player.CanHook.ForceUnhooked()
            self.CurrentUpdater = self.SlowAttracting
            
            
    def OnLogicUpdate(self, UpdateEvent):
        self.CurrentUpdater()
           
    def Detecting(self):
        if abs(self.Owner.Transform.Translation.x - self.Player.Transform.Translation.x) < 4:
            self.Owner.SphericalParticleEmitter.Active = True
            
    def SlowAttracting(self):
        self.Player.PlayerController.DontUpdateAnim = True
        self.Player.Sprite.SpriteSource = self.Player.PlayerController.AnimTable.FindValue("Attack")
        self.Player.RigidBody.Kinematic = True
        self.Owner.Transform.Translation = 0.996 *  self.Owner.Transform.Translation + 0.004 * self.Player.Transform.WorldTranslation
        self.Player.Transform.Translation += Vec3(0,0.003,0)
        if not self.VerticalDetect:
            condition = abs(self.Owner.Transform.Translation.x - self.Player.Transform.Translation.x) < 2
        else:
            condition = abs(self.Owner.Transform.Translation.y - self.Player.Transform.Translation.y) < 2
        if condition:
            #self.camera.CameraFunction.SetCameraFade(self.ShadingColor*Vec4(1, 1,1, 0), self.ShadingColor, .01, 0)
            self.CurrentUpdater = self.Attracting
    def Attracting(self):
        self.Owner.Transform.Translation = 0.98 *  self.Owner.Transform.Translation + 0.02* self.Player.Transform.WorldTranslation
        self.Player.Transform.Translation += Vec3(0,0.001,0)
        if not self.VerticalDetect:
            condition = abs(self.Owner.Transform.Translation.x - self.Player.Transform.Translation.x) < 0.1
        else:
            condition = abs(self.Owner.Transform.Translation.y - self.Player.Transform.Translation.y) < 0.1
        if condition:
            #self.camera.CameraFunction.SetCameraFade(self.ShadingColor*Vec4(1, 1,1, 0), self.ShadingColor, .01, 0)
            self.CurrentUpdater = self.Ending
            
    def Ending(self):
        
        
        self.Owner.SphericalParticleEmitter.Size *= 1.05
        self.Owner.SphericalParticleEmitter.EmitRate = 35
        if self.Owner.SphericalParticleEmitter.Size > 25:
            self.CurrentUpdater = self.Fading
            self.Player.Sprite.Visible = False
            for child in self.Player.Hierarchy.Children:
                if child.Sprite:
                    child.Sprite.Visible = False
            
            #d = self.DestinationObject.Transform.WorldTranslation
            #z = self.Player.Transform.WorldTranslation.z
            #self.Player.Transform.WorldTranslation = Vec3(d.x, d.y, z)
            
            #z = self.camera.Transform.WorldTranslation.z
            #self.camera.Transform.WorldTranslation = Vec3(d.x, d.y, z)
            
            
            
            
            #def showit():
            #    self.camera.CameraFunction.SetCameraFade(self.ShadingColor,self.ShadingColor*Vec4(1,1,1,0),0.005,0)
            #    self.Player.RigidBody.Kinematic = False
            
            #self.CurrentUpdater = self.Fading
                
            #if self.ExtendedDelay:
            #    self.camera.CameraFunction.SetCameraFade(self.ShadingColor, self.ShadingColor,2,0)
            #    self.Owner.DestroyInterface.Destroy()

            #    seq = Action.Sequence(self.Player.Actions)
            #    Action.Delay(seq, 2)
            #    Action.Call(seq, showit)
            #else:
            #    self.camera.CameraFunction.SetCameraFade(self.ShadingColor, self.ShadingColor*Vec4(1,1,1,0),0.0025,0)
            #    self.CurrentUpdater = self.Fading
            #    self.Player.RigidBody.Kinematic = False
            #    self.Owner.DestroyInterface.Destroy()
            
            #self.Space.FindObjectByName("EndingWeather").RainGenerator.Activatable = True
            #self.Space.SoundSpace.PlayCue("Thunder")

            
    def Fading(self):
        self.Owner.SpriteParticleSystem.Tint *= VectorMath.Vec4(1,1,1,0.95)
        for child in self.Owner.Hierarchy.Children:
            child.SpriteParticleSystem.Tint *= VectorMath.Vec4(1,1,1,0.95)
        
        if self.Owner.SpriteParticleSystem.Tint.a < 0.001:
            
            self.CurrentUpdater = self.Fading2
            self.Space.FindObjectByName("LevelSettings").LevelStart.HUDManager.ShowScores()
            self.Owner.DestroyInterface.Destroy()
            
        
    def Fading2(self):
        
        
        word1 = self.Space.FindObjectByName("EndingWord1")
        word2 = self.Space.FindObjectByName("EndingWord2")
        word3 = self.Space.FindObjectByName("EndingWord3")
        
        if 1 - word1.SpriteText.Color.a < 0.02:
            word1.FadeAnim.FadeDirection = -1
            word2.FadeAnim.FadeDirection = -1
            word1.FadeAnim.FadingDuration = 2
            word2.FadeAnim.FadingDuration = 2
            
            word1.FadeAnim.Active = True
            word2.FadeAnim.Active = True
            
            self.CurrentUpdater = self.Fading3
            
    def Fading3(self):
        word1 = self.Space.FindObjectByName("EndingWord1")
        word3 = self.Space.FindObjectByName("EndingWord3")
        if word1.SpriteText.Color.a < 0.02:
            word3.FadeAnim.Active = True

    def DestroyDelegate(self):
        if self.Owner.DestroyInterface:
            self.Owner.DestroyInterface.Destroy()
        else:
            self.Owner.Destroy()
            
Zero.RegisterComponent("NormalTreeSoulBehavior", NormalTreeSoulBehavior)