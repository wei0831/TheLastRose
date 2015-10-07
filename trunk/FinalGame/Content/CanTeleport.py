import Zero
import Events
import Property
import VectorMath
import math
Vec3=VectorMath.Vec3
class CanTeleport:
    Active = Property.Bool(True)
    SpriteDependentOffset = Property.Bool(False)
    Offset = Property.Float(3.5)
    
    def Initialize(self, initializer):
        pass
        
    def Teleport(self, target):
        if self.Active:
            canberooted = self.Owner.FindRoot().CanBeRooted
            if canberooted:
                if not self.SpriteDependentOffset:
                    target.Transform.Translation += canberooted.GetNormal() * self.Offset
                else:
                    for child in self.Owner.Parent.Hierarchy.Children:
                        if child.Name == "surfroot":
                            break
                    target.Transform.WorldTranslation = child.Transform.WorldTranslation + canberooted.GetNormal()*.1 + Vec3(0,0.2,0)
                if target.RigidBody:
                    target.RigidBody.ApplyLinearVelocity(canberooted.GetNormal()*10)
                    if not target.RigidBody.RotationLocked:
                        target.RigidBody.ApplyAngularVelocity(Vec3(0,0,10))
                    
            else:
                target.Transform.Translation += Vec3(0,self.Offset,0)
            
        

Zero.RegisterComponent("CanTeleport", CanTeleport)