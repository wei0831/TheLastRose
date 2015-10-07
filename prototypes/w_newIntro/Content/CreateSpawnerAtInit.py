import Zero
import Events
import Property
import VectorMath

class CreateSpawnerAtInit:
    Teleporter = Property.Cog()
    Delay = Property.Float(5)
    def Initialize(self, initializer):
        self.Teleporter = self.Space.CreateAtPosition("EnemySpawner", self.Owner.Transform.Translation)
        if not self.Owner.DestroyTeleport:
            self.Owner.AddComponentByName("DestroyTeleport")
        self.Teleporter.MonsterSpawner.RespawnDelay = self.Delay
        
        
        

Zero.RegisterComponent("CreateSpawnerAtInit", CreateSpawnerAtInit)