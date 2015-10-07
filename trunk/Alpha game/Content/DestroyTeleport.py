import Zero
import Events
import Property
import VectorMath

class DestroyTeleport:
    TeleportTarget = Property.Cog()
    def Initialize(self, initializer):
        if not self.Owner.DestroyInterface:
            self.Owner.AddComponentByName("DestroyInterface")
    def Destroy(self):
        
        if not self.TeleportTarget:
            self.TeleportTarget = self.Owner.CreateSpawnerAtInit.Teleporter
        self.TeleportTarget.MonsterSpawner.HideDestroy(self.Owner)
        self.TeleportTarget.MonsterSpawner.Respawn(self.Owner)
        
Zero.RegisterComponent("DestroyTeleport", DestroyTeleport)