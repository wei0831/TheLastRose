import Zero
import Events
import Property
import VectorMath
import datetime
import time
from time import gmtime, strftime

class SaveMyGame:
    
    SavedTime = Property.String("")
    Location = Property.String("")
    Ability = Property.Int(2)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        print(self.Owner.Name + " Created : " + "Position: " + str(self.Owner.SaveMyGame.Location) + " Ability: " + str(self.Owner.SaveMyGame.Ability))

    def OnLogicUpdate(self, UpdateEvent):
        if Zero.Keyboard.KeyIsPressed(Zero.Keys.Up):
            self.Ability+=1
        if Zero.Keyboard.KeyIsPressed(Zero.Keys.Down):
            self.Ability-=1

        if Zero.Keyboard.KeyIsPressed(Zero.Keys.P):
            print("------")
            print("Current time is : " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            print(self.Owner.Name + " at " + str(self.SavedTime))
            print("------")
            
        self.Location = str(int(self.Owner.Transform.WorldTranslation.x)) + ", " + str(int(self.Owner.Transform.WorldTranslation.y)) + ", " + str(int(self.Owner.Transform.WorldTranslation.z))
            
        if Zero.Keyboard.KeyIsPressed(Zero.Keys.K):
            self.SavedTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            Zero.ObjectStore.Store(self.Owner.Name, self.Owner)
            print("Saved : " + "Position: " + str(self.Owner.SaveMyGame.Location) + " Ability: " + str(self.Owner.SaveMyGame.Ability))

            
        if Zero.Keyboard.KeyIsPressed(Zero.Keys.L):
            print("Before Load : " + "Position: " + str(self.Owner.SaveMyGame.Location) + " Ability: " + str(self.Owner.SaveMyGame.Ability))
            self.Owner.Destroy()
            Zero.ObjectStore.Restore(self.Owner.Name, self.Space)

Zero.RegisterComponent("SaveMyGame", SaveMyGame)