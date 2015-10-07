import Zero
import Events
import Property
import VectorMath

class DoorEnterer:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnd)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.current_door = None
        
    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.KeyHoleDoor and CollisionEvent.OtherObject.KeyHoleDoor.IsOpened():
            self.current_door = CollisionEvent.OtherObject
            if self.current_door.KeyHoleDoor.SimpleTeleport:
                self.current_door.KeyHoleDoor.TeleportThis(self.Owner)
            
    def OnLogicUpdate(self, UpdateEvent):
        if Zero.Keyboard.KeyIsPressed(Zero.Keys.W):
            if self.current_door:
                self.current_door.KeyHoleDoor.TeleportThis(self.Owner)
                self.Owner.RigidBody.Velocity = VectorMath.Vec3(0,0,0)
                if self.current_door.KeyHoleDoor.Teleport:
                    self.current_door = self.current_door.KeyHoleDoor.Teleport
            
    def OnCollisionEnd(self, CollisionEvent):
        if CollisionEvent.OtherObject == self.current_door:
            self.current_door = None
        
        
        
        
Zero.RegisterComponent("DoorEnterer", DoorEnterer)