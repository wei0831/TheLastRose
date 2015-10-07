import Zero
import Events
import Property
import VectorMath

import warnings

class gamelogic:
    def Initialize(self, initializer):
        self.score = 0
        self.Viewer = self.Space.FindObjectByName("Text")
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        def add_one_score():
            self.score += 1
            
        def destroy_viewer():
            self.Viewer.Destroy()
            self.Viewer = None

        self.Owner.ActionList.AddCurrentAction(destroy_viewer,blocking=False, countdown=4)
        self.Owner.ActionList.AddCallback(add_one_score, blocking=True, countdown=1)
        self.Owner.ActionList.AddCallback(add_one_score, blocking=False, countdown=1)
        self.Owner.ActionList.AddCallback(add_one_score, blocking=True, countdown=1)
        self.Owner.ActionList.AddCallback(add_one_score, blocking=False, countdown=1)
        self.Owner.ActionList.AddCallback(add_one_score, blocking=False, countdown=1)
        self.Owner.ActionList.AddCallback(add_one_score, blocking=True, countdown=1)
        
    def OnLogicUpdate(self, UpdateEvent):
        if self.Viewer:
            self.Viewer.SpriteText.Text = str(self.score)
        
Zero.RegisterComponent("gamelogic", gamelogic)