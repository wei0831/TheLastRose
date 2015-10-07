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
        if obj.TransferEffectToChild and obj.Hierarchy:
            target_name = obj.TransferEffectToChild.ChildName
            for child in obj.Hierarchy.Children:
                if child.Name == target_name:
                    obj = child
                    break
        if not obj.CanFreeze:
            obj.AddComponentByName("CanFreeze")
        if not obj.BoxCollider and not obj.SphereCollider:
            obj.AddComponentByName("BoxCollider")
            obj.BoxCollider.Ghost = True
        if obj.CanBounce:
            obj.CanBounce.Active = False
        if not obj.IsSentry:
            obj.AddComponentByName("IsSentry")
        if not obj.Bounceable:
            obj.AddComponentByName("Bounceable")
        if obj.Blowable:
            obj.Blowable.Active = False
        if obj.GravityEffect:
            obj.GravityEffect.Active = False
        if obj.DragEffect:
            obj.DragEffect.Active = False
        if obj.Hookable:
            obj.Hookable.NonActivatable = True
            for child in obj.Hierarchy.Children:
                if child.Name == "Preventer":
                    child.Collider.Ghost = True
                    child.DetachRelative()
                    child.Destroy()
        if obj.RigidBody:
            obj.RigidBody.RotationLocked = False
        if obj.Sprite:
            obj.Sprite.AnimationActive = False
        
    def Perform(self, position):
        ice = self.Space.CreateAtPosition("IceParticle", self.mouse.Transform.Translation)
        ice.AddComponentByName("ActionList")
        ice.Transform.Translation += VectorMath.Vector3(0,0,1)
        
        
        def shrink(self):            
            self.Owner.SpriteParticleSystem.Tint -= VectorMath.Vec4(0,0,0,0.01)
            if self.Owner.SpriteParticleSystem.Tint.a < 0.01:
                self.Owner.Destroy()
            

        
        ice.ActionList.AddCallback(callback=shrink, has_self=True, blocking=True, countdown=None)
        
                
Zero.RegisterComponent("PhysSkillIce", PhysSkillIce)