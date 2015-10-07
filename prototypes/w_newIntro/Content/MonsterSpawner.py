import Zero
import Events
import Property
import VectorMath
import Action
class MonsterSpawner:
    RespawnDelay = Property.Float(1.0)
    def Initialize(self, initializer):
        pass
    def HideDestroy(self, target):
        target.Sprite.Visible = False
        print (target.AIMovementInterface)
        
        if target.AIMovementInterface:
            target.AIMovementInterface.Deactivate()
            
        target.Transform.Translation = VectorMath.Vec3(0,0,-100)
        target.Collider.Ghost = True
        
        if not target.RigidBody.Static and not target.RigidBody.Kinematic:
            target.RigidBody.Static = True
        if target.HealthStatus:
            target.HealthStatus.ResetHealth()
    
    def PerformRespawn(self, target):
        
        if not target.FadeAnim:
            target.AddComponentByName("FadeAnim")

        target.FadeAnim.FadeIn()
        target.Transform.Translation = self.Owner.Transform.Translation
        target.Collider.Ghost = False
        target.Sprite.Visible = True
        if target.RigidBody.Static:
            target.RigidBody.Static = False
        if target.AIMovementInterface:
            target.AIMovementInterface.Activate()
            
    def Respawn(self, target):
        self.Owner.Actions.Clear()
        seq = Action.Sequence(self.Owner)
        
        seq = Action.Sequence(self.Owner)
        Action.Delay(seq, self.RespawnDelay)
        Action.Call(seq, self.PerformRespawn, (target,))
        
            
            
    
           
            

Zero.RegisterComponent("MonsterSpawner", MonsterSpawner)