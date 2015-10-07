import Zero
import Events
import Property
import VectorMath
Vec4 = VectorMath.Vec4
class HotFixTouchSummoner:
    def Initialize(self, initializer):
        self.player = self.Space.FindObjectByName("Player")
        #self.Space.FindObjectByName("LastWall").Summoned.RegisterTo(self.Owner)
        healthparticle = self.Space.CreateAtPosition("HealthParticle", self.player.Transform.Translation)
        healthparticle.SphericalParticleEmitter.EmitCount = 0
        healthparticle.SphericalParticleEmitter.ResetCount()
        
        self.Space.FindObjectByName("Camera").CameraFunction.SetCameraFade(Vec4(0,0,0,0),Vec4(0,0,0,0.9),0.00075,0)
        self.Space.FindObjectByName("DumbHelper").SphericalParticleEmitter.Active = True
        
        mi = self.Space.FindObjectByName("MouseIndicator")
        ds = self.Space.CreateAtPosition("DumbSoul", mi.Transform.WorldTranslation)
        ds.AttachToRelative(mi)
        
        
        
        hl = self.Space.FindObjectByName("LevelSettings").LevelStart.HUDManager.Space
        pb1 = hl.FindObjectByName("pbox_big")
        pb2 = hl.FindObjectByName("pbox_small")
        
        hl.CreateAtPosition("DumbSoul", pb1.Transform.WorldTranslation)
        hl.CreateAtPosition("DumbSoul", pb2.Transform.WorldTranslation)
        
        
        
        pass
        
   
        

Zero.RegisterComponent("HotFixTouchSummoner", HotFixTouchSummoner)