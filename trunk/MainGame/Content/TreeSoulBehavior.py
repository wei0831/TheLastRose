import Zero
import Events
import Property
import VectorMath

class TreeSoulBehavior:
    def Initialize(self, initializer):
        
        self.CurrentUpdater = self.Detecting
        self.Player = self.Space.FindObjectByName("Player")
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.CollisionStart)
        
    def CollisionStart(self, CollisionEvent):
        if CollisionEvent.OtherObject == self.Player:
            self.Player.CanHook.ForceUnhooked()
            self.CurrentUpdater = self.Attracting
            
            
    def OnLogicUpdate(self, UpdateEvent):
        self.CurrentUpdater()
           
    def Detecting(self):
        if abs(self.Owner.Transform.Translation.x - self.Player.Transform.Translation.x) < 4:
            self.Owner.SphericalParticleEmitter.Active = True
            
    
                
    def Attracting(self):
        self.Player.RigidBody.Kinematic = True
        self.Player.Transform.Translation = 0.97 *  self.Player.Transform.Translation + 0.03 * self.Owner.Transform.Translation
        if abs(self.Owner.Transform.Translation.x - self.Player.Transform.Translation.x) < 0.1:
            self.CurrentUpdater = self.Ending
            
    def Ending(self):
        self.Owner.SphericalParticleEmitter.Size *= 1.05
        self.Owner.SphericalParticleEmitter.EmitRate = 35
        if self.Owner.SphericalParticleEmitter.Size > 20:
            
            for child in self.Player.Hierarchy.Children:
                child.Sprite.Visible = False
            self.Player.Sprite.Visible = False
            self.Player.Collider.Ghost = True
            self.CurrentUpdater = self.Fading
            
            #self.Space.FindObjectByName("EndingWeather").RainGenerator.Activatable = True
            #self.Space.SoundSpace.PlayCue("Thunder")

            
    def Fading(self):
        
        self.Owner.SpriteParticleSystem.Tint *= VectorMath.Vec4(1,1,1,0.95)
        for child in self.Owner.Hierarchy.Children:
                child.SpriteParticleSystem.Tint *= VectorMath.Vec4(1,1,1,0.95)
                
        if self.Owner.SpriteParticleSystem.Tint.a < 0.001:
            self.Space.SoundSpace.PlayCue("Rain")
            self.Space.SoundSpace.PlayCue("RavenCue")

            
            self.Space.FindObjectByName("EndingWord1").FadeAnim.Active = True
            self.Space.FindObjectByName("EndingWord2").FadeAnim.Active = True
            self.CurrentUpdater = self.Fading2

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
            
Zero.RegisterComponent("TreeSoulBehavior", TreeSoulBehavior)