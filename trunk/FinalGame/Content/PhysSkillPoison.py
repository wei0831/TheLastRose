import Zero
import Events
import Property
import VectorMath

class PhysSkillPoison:
    Name = Property.String("PhysSkillPoison")
    
    def Initialize(self, initializer):
        self.mouse = self.Space.FindObjectByName("MouseIndicator")
        
    def Modify(self, obj):
        if obj.TransferEffectToChild and obj.Hierarchy:
            target_name = obj.TransferEffectToChild.ChildName
            for child in obj.Hierarchy.Children:
                if child.Name == target_name:
                    obj = child
                    break
        
        if not obj.CanPoison:
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