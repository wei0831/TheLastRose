import Zero
import Events
import Property
import VectorMath


class PhysSkillIce:
    Name = Property.String("PhysSkillIce")
    
    def Initialize(self, initializer):
        self.mouse = self.Space.FindObjectByName("MouseIndicator")
        
    def OnLogicUpdate(self, UpdateEvent):
        pass
        
    def Modify(self, obj):
        if not obj.CanFreeze:
            obj.AddComponentByName("CanFreeze")
        if not obj.BoxCollider and not obj.SphereCollider:
            obj.AddComponentByName("BoxCollider")
            obj.BoxCollider.Ghost = True
        if obj.CanBounce:
            obj.CanBounce.Active = False
        if not obj.IsSentry:
            obj.AddComponentByName("IsSentry")
            
        if obj.Blowable:
            obj.Blowable.Active = False
        if obj.GravityEffect:
            obj.GravityEffect.Active = False
        if obj.DragEffect:
            obj.DragEffect.Active = False
        if obj.Hookable:
            obj.Hookable.NonActivatable = True
        
    def Perform(self, position):
        ice = self.Space.CreateAtPosition("IceParticle", self.mouse.Transform.Translation)

        ice.AddComponentByName("TimedDeath")
        ice.AddComponentByName("CanFreeze")
        ice.AddComponentByName("BoxCollider")
        ice.AddComponentByName("ActionList")
        
        lifetime = 1
        ice.BoxCollider.Ghost = True
        ice.TimedDeath.LifeTime = lifetime
        ice.TimedDeath.Active = True
        ice.TimedDeath.DestroyAtTheEnd = True
        
        # TODO: Not working properly. Solution thought of. Implement later
        def shrink(self):
            self.Owner.LinearParticleAnimator.Force -= VectorMath.Vec3(0,0.1,0)
            if self.Owner.LinearParticleAnimator.Force.y < 0:
                self.Owner.LinearParticleAnimator.Force = VectorMath.Vec3(0,0,0)
                
        
        ice.ActionList.AddCallback(callback=shrink, has_self=True, blocking=True, countdown=None)
        
                
Zero.RegisterComponent("PhysSkillIce", PhysSkillIce)