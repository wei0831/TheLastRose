import Zero
import Events
import Property
import VectorMath
import Action
Vec4 = VectorMath.Vec4
class TreeSkillWorldtree:
    Name = Property.String("TreeSkillWorldtree")
    
    
    
    def Initialize(self, initializer):
        self.clickcounter = 0
        self.cached_particle = None
        self.shrink_enough = False
                                          
                                          
        self.temp_counter = 0
    
    def Perform(self, position, physeffect = None):
        
        self.Space.FindObjectByName("RandomYeller").RandomYeller.CreateOne()
        
        
        if self.clickcounter < 5:
            self.Space.FindObjectByName("Camera").CameraFunction.SetCameraFade(Vec4(1,1,1,0),Vec4(1,1,1,0),1,0)
            
            self.Space.SoundSpace.PlayCue("RootCue")
            self.clickcounter += 0.2
            
            particle = self.Space.CreateAtPosition("WorldTreeParticle", position)
            particle.SphericalParticleEmitter.EmitterSize *= self.clickcounter/1.5
            particle.SphericalParticleEmitter.EmitRate *= self.clickcounter * 5
            particle.SphericalParticleEmitter.EmitCount = int(100 * self.clickcounter)
            particle.SphericalParticleEmitter.ResetCount()
            
            if int(self.clickcounter) == 5:
                self.cached_particle = particle
                particle.SphericalParticleEmitter.EmitRate = 1200
                particle.SphericalParticleEmitter.EmitCount = 0
                particle.SphericalParticleEmitter.ResetCount()
                particle.TimedDeath.Active = False
                
            self.Space.FindObjectByName("Camera").CameraFunction.SetCameraShake(True, .1, True, .1, 0.1, 0)
        elif self.clickcounter >= 5 and self.clickcounter <= 15:
            
            self.clickcounter += 1
            self.cached_particle.SphericalParticleEmitter.EmitRate *= 1.2
            particle = self.cached_particle
            self.Space.FindObjectByName("Camera").CameraFunction.SetCameraShake(True, .1, True, .1, 0.1, 0)
            if int(self.clickcounter) == 15:
                Zero.Connect(self.Space, Events.LogicUpdate, self.BeginShrink)
                
            
        else:
            particle = None
            
        
        #if physeffect:
        #    physeffect.Modify(mushroom)
        
        return particle
        
    def BeginShrink(self, UpdateEvent):
        self.cached_particle.SphericalParticleEmitter.EmitterSize *= 0.99
        self.Space.FindObjectByName("Camera").CameraFunction.SetCameraShake(True, .35, True, .35, 0.1, 0)
        
        
        self.temp_counter += 1
        if self.temp_counter > 10:
            self.temp_counter = 0
            self.Space.FindObjectByName("RandomYeller").RandomYeller.CreateOne()
        if self.cached_particle.SphericalParticleEmitter.EmitterSize.x < 2.5 and not self.shrink_enough:
            self.shrink_enough = True
            self.Space.FindObjectByName("Camera").CameraFunction.SetCameraFade(VectorMath.Vec4(1,1,1,0),VectorMath.Vec4(1,1,1,1),0.05,0)
            seq = Action.Sequence(self.Owner.Actions)
            Action.Delay(seq, 2)
            Action.Call(seq, lambda:self.Space.LoadLevel("CreditLevel"))
            Action.Call(seq, lambda:self.Space.FindObjectByName("LevelSettings").LevelStart.RemoveHUD())
        #if mushroom.TimedDeath:
        #    def DeactivateBounce(self):
        #        self.Owner.CanBounce.Active = False
                
        #    mushroom.TimedDeath.SetCallback(DeactivateBounce)
        #    mushroom.TimedDeath.Active = True
        #return mushroom

Zero.RegisterComponent("TreeSkillWorldtree", TreeSkillWorldtree)