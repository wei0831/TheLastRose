import Zero
import Events
import Property
import VectorMath

class PhysSkillFire:
    Name = Property.String("PhysSkillFire")
    
    def Initialize(self, initializer):
        self.mouse = self.Space.FindObjectByName("MouseIndicator")
        
    def OnLogicUpdate(self, UpdateEvent):
        pass
        
    def Modify(self, obj):
        if not obj.CanBurn:
            obj.AddComponentByName("CanBurn")
        if not obj.BoxCollider and not obj.SphereCollider:
            obj.AddComponentByName("BoxCollider")
            obj.BoxCollider.Ghost = True
        if obj.WindSpawningPlant:
            obj.AddComponentByName("CanSpawnWind")
        
    def Perform(self, position):
        fire = self.Space.CreateAtPosition("FireParticle", self.mouse.Transform.Translation)

        fire.AddComponentByName("TimedDeath")
        fire.AddComponentByName("CanBurn")
        fire.AddComponentByName("BoxCollider")
        fire.AddComponentByName("ActionList")
        
        lifetime = 1
        fire.BoxCollider.Ghost = True
        fire.TimedDeath.LifeTime = lifetime
        fire.TimedDeath.Active = True
        fire.TimedDeath.DestroyAtTheEnd = True
        
        # TODO: Not working properly. Solution thought of. Implement later
        def shrink(self):
            self.Owner.LinearParticleAnimator.Force -= VectorMath.Vec3(0,0.1,0)
            if self.Owner.LinearParticleAnimator.Force.y < 0:
                self.Owner.LinearParticleAnimator.Force = VectorMath.Vec3(0,0,0)
                
        
        fire.ActionList.AddCallback(callback=shrink, has_self=True, blocking=True, countdown=None)
        
        
        
        
        

Zero.RegisterComponent("PhysSkillFire", PhysSkillFire)