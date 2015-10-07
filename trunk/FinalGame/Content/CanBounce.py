import Zero
import Events
import Property
import VectorMath
import math
import Action


class CanBounce:
    Active = Property.Bool(True)
    ForcedVx = Property.Float(0)
    ForcedVy = Property.Float(0)
    UpdateBasedOnSprite = Property.Bool(False)
    TopModify = Property.Bool(False)
    
    def Initialize(self, initializer):
        self.InitialStrength = math.sqrt(self.ForcedVx**2 + self.ForcedVy**2)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
    
    def EnsureSoundEmitter(self):
        if not self.Owner.SoundEmitter:
            self.Owner.AddComponentByName("SoundEmitter")
        def Null():
            pass
            
        self.EnsureSoundEmitter = Null
    
    def OnCollision(self, CollisionEvent):
        if self.Active and CollisionEvent.OtherObject.Bounceable:
            
            self.EnsureSoundEmitter()
            self.Owner.SoundEmitter.PlayCue("BounceCue")
            self.Owner.SoundEmitter.Volume *= 0.9
            
            def RecoverVolume():
                self.Owner.SoundEmitter.Volume /= 0.9
            
            seq = Action.Sequence(self.Owner.Actions)
            Action.Delay(seq,2)
            Action.Call(seq, RecoverVolume)
            
            modifier = -1 if self.UpdateBasedOnSprite and self.Owner.Sprite.FlipX else 1
            adder = 0
            if self.TopModify:
                boxloc = self.Owner.Transform.Translation + self.Owner.BoxCollider.Offset
                
                boxdims = self.Owner.BoxCollider.Size
                angle = self.Owner.Transform.EulerAngles.z
                normal = VectorMath.Vec3.RotateVector(VectorMath.Vec3(0,1,0), VectorMath.Vec3(0,0,1), angle)
                
                shifter = (boxloc + boxdims * .5 * normal) - CollisionEvent.FirstPoint.WorldPoint
                
                adder = shifter.y if shifter.y > 0 else 0
                #if self.Owner.Name == "Mushroom":
                #    print(adder)
                ##rigid = CollisionEvent.OtherObject.RigidBody
                
                #def Modifying():
                #    rigid.Velocity += VectorMath.Vec3(0, shifter.y,0)
                    
                #seq = Action.Sequence(CollisionEvent.OtherObject.Actions)                
                #Action.Call(seq, Modifying)
                #Action.Delay(seq, 0.1)
                
            if CollisionEvent.OtherObject.Bounceable:
                impulseEvent = Zero.ScriptEvent()
                impulseEvent.ForcedVx = self.ForcedVx * modifier     
                impulseEvent.ForcedVy = self.ForcedVy + adder 
                CollisionEvent.OtherObject.DispatchEvent("BounceEvent", impulseEvent)
                
            
    def ToDirection(self, normal):
        
        self.ForcedVx = self.InitialStrength * normal.x
        self.ForcedVy = self.InitialStrength * normal.y
        
        
            
            

Zero.RegisterComponent("CanBounce", CanBounce)