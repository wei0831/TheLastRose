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
        pass
        if not obj.CanBurn:
            obj.AddComponentByName("CanBurn")
        if not obj.BoxCollider and not obj.SphereCollider:
            obj.AddComponentByName("BoxCollider")
            obj.BoxCollider.Ghost = True
        if obj.WindSpawningPlant:
            obj.AddComponentByName("CanSpawnWind")
        if not obj.GotLight:
            obj.AddComponentByName("GotLight")
            obj.GotLight.ChangeSize(0.1)
        
    def Perform(self, position):
        fire = self.Space.CreateAtPosition("FireParticle", self.mouse.Transform.Translation)
        
        fire.AddComponentByName("ActionList")
        fire.AddComponentByName("GotLight")
        fire.GotLight.ChangeSize(0.1)
        def shrink(self):            
            self.Owner.SpriteParticleSystem.Tint -= VectorMath.Vec4(0,0,0,0.003)
            if self.Owner.SpriteParticleSystem.Tint.a < 0.005:
                self.Owner.Destroy()
        
        fire.ActionList.AddCallback(callback=shrink, has_self=True, blocking=True, countdown=None)


Zero.RegisterComponent("PhysSkillFire", PhysSkillFire)