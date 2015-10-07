import Zero
import Events
import Property
import VectorMath
import Action
class CreateSpawnerAtInit:
    Teleporter = Property.Cog()
    Delay = Property.Float(5)
    def Initialize(self, initializer):
        self.Teleporter = self.Space.CreateAtPosition("EnemySpawner", self.Owner.Transform.WorldTranslation)
        
        seq = Action.Sequence(self.Owner.Actions)
        def EnsureDestroyTeleport():
            if not self.Owner.DestroyTeleport:
                self.Owner.AddComponentByName("DestroyTeleport")
        Action.Call(seq, EnsureDestroyTeleport)        
                
        self.Teleporter.MonsterSpawner.RespawnDelay = self.Delay
        
        
        

Zero.RegisterComponent("CreateSpawnerAtInit", CreateSpawnerAtInit)