import Zero
import Events
import Property
import VectorMath
import random

class gamelogic:
    def Initialize(self, initializer):
        self.player = self.Space.FindObjectByName("Player")
        self.select_phys = 0
        self.select_tree = 0
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if Zero.Keyboard.KeyIsPressed(Zero.Keys.One):
            skillnames = (None, "PhysSkillFire", "PhysSkillIce")
            self.player.AbilityStatus.SwapPhysSkill(skillnames[self.select_phys])
            self.select_phys = (self.select_phys + 1) % 3

        if Zero.Keyboard.KeyIsPressed(Zero.Keys.Two):
            skillnames = (None, "TreeSkillMushroom", "TreeSkillWhirlingnut")
            self.player.AbilityStatus.SwapTreeSkill(skillnames[self.select_tree])
            self.select_tree = (self.select_tree + 1) % 3


Zero.RegisterComponent("gamelogic", gamelogic)