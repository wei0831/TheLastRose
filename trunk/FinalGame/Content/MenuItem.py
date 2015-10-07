import Zero
import Events
import Property
import VectorMath

class MenuItem:
    ActionCode = Property.String("")
    def Initialize(self, initializer):
        if not self.Owner.Collider:
            self.Owner.AddComponentByName("BoxCollider")
            pos0 = self.Owner.SpriteText.GetCharacterPosition(0)
            pos_end = self.Owner.SpriteText.GetCharacterPosition(len(self.Owner.SpriteText.Text)-1)
            
            width = 9
            self.Owner.BoxCollider.Size = VectorMath.Vec3(width, 0.6, 300)
            self.Owner.BoxCollider.Offset = VectorMath.Vec3(width/2,-0.3,0)
            
            if not self.Owner.RigidBody:
                self.Owner.AddComponentByName("RigidBody")
                self.Owner.RigidBody.Static = True
                self.Owner.RigidBody.AllowSleep = False
            

Zero.RegisterComponent("MenuItem", MenuItem)