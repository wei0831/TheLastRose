import Zero
import Events
import Property
import VectorMath

class PhysSkillPoison:
    Name = Property.String("PhysSkillPoison")
    
    def Initialize(self, initializer):
        self.mouse = self.Space.FindObjectByName("MouseIndicator")
        
    def OnLogicUpdate(self, UpdateEvent):
        pass
        
    def Modify(self, obj):
        if not obj.CanFreeze:
            obj.AddComponentByName("CanPoison")
        if not obj.BoxCollider:
            obj.AddComponentByName("BoxCollider")
            obj.BoxCollider.Ghost = True
        
    def Perform(self, position):
        poison = self.Space.CreateAtPosition("PoisonParticle", self.mouse.Transform.Translation)

        poison.AddComponentByName("TimedDeath")
        poison.AddComponentByName("CanPoison")
        poison.AddComponentByName("BoxCollider")
        poison.AddComponentByName("ActionList")
        
        lifetime = 1
        poison.BoxCollider.Ghost = True
        poison.TimedDeath.LifeTime = lifetime
        poison.TimedDeath.Active = True
        poison.TimedDeath.DestroyAtTheEnd = True
        
        # TODO: Not working properly. Solution thought of. Implement later
        def shrink(self):
            self.Owner.LinearParticleAnimator.Force -= VectorMath.Vec3(0,0.1,0)
            if self.Owner.LinearParticleAnimator.Force.y < 0:
                self.Owner.LinearParticleAnimator.Force = VectorMath.Vec3(0,0,0)
                
        
        poison.ActionList.AddCallback(callback=shrink, has_self=True, blocking=True, countdown=None)

Zero.RegisterComponent("PhysSkillPoison", PhysSkillPoison)