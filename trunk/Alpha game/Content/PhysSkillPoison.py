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
        if not obj.Collider:
            obj.AddComponentByName("BoxCollider")
            obj.Collider.Ghost = True
        
    def Perform(self, position):
        poison = self.Space.CreateAtPosition("PoisonParticle", self.mouse.Transform.Translation)
        poison.AddComponentByName("ActionList")
        
        def shrink(self):            
            self.Owner.SpriteParticleSystem.Tint -= VectorMath.Vec4(0,0,0,0.003)
            if self.Owner.SpriteParticleSystem.Tint.a < 0.005:
                self.Owner.Destroy()
        
        poison.ActionList.AddCallback(callback=shrink, has_self=True, blocking=True, countdown=None)

Zero.RegisterComponent("PhysSkillPoison", PhysSkillPoison)