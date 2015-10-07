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

            self.Owner.Destroy()
            self.Space.FindObjectByName("EndingWord1").FadeAnim.Active = True
            self.Space.FindObjectByName("EndingWord2").FadeAnim.Active = True
            
Zero.RegisterComponent("TreeSoulBehavior", TreeSoulBehavior)