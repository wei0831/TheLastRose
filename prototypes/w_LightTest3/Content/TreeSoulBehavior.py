import Zero
import Events
import Property
import VectorMath

class TreeSoulBehavior:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.CollisionStart)
        
    def CollisionStart(self, CollisionEvent):
        if CollisionEvent.OtherObject.Name == "Player":
            for item in self.Owner.Hierarchy.Children:
                print(item.Name)
                item.Destroy()
            self.Owner.Destroy()

Zero.RegisterComponent("TreeSoulBehavior", TreeSoulBehavior)