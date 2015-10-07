import Zero
import Events
import Property
import VectorMath
Vec3 = VectorMath.Vec3
class SimpleMouseMover:
    
    def Initialize(self, initializer):
        Zero.Mouse.Cursor = Zero.Cursor.Invisible
        Zero.Connect(self.Space, Events.MouseMove, self.OnMouseUpdate)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollision)
        
                
        self.MousePos = Vec3(0,0,0)
        self.menu = self.Space.FindObjectByName("MenuInitial")
        
    def OnLogicUpdate(self, UpdateEvent):
        self.Owner.Transform.WorldTranslation = self.MousePos
        
    def OnMouseUpdate(self, MouseUpdateEvent):
        self.MousePos = MouseUpdateEvent.ToWorldZPlane(0)
        self.Owner.Transform.WorldTranslation = self.MousePos
        self.menu.Menu.ResumeMouseSelect()

    def OnCollision(self, CollisionEvent):
        if CollisionEvent.OtherObject.MenuItem:
            CollisionEvent.OtherObject.Parent.Menu.DirectSelect(CollisionEvent.OtherObject, IsMouse = True)

    
        
Zero.RegisterComponent("SimpleMouseMover", SimpleMouseMover)