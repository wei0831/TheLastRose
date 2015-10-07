import Zero
import Events
import Property
import VectorMath

class QuitProhibiter:
    AllowQuit = Property.Bool(default = False)
    def Initialize(self, init):
        #listen for the game engine requesting quit
        Zero.Connect(Zero.Game, Events.GameRequestQuit, self.OnGameRequestQuit)
    
    def OnGameRequestQuit(self, gameEvent):
        #If you handle this event the game will not exit
        gameEvent.Handled = True
        #if we allow the request to quit to work, then quit the game
        if(self.AllowQuit):
            self.QuitGame()
    
    def QuitGame(self):
        #In editor mode, this will quit to the editor.
        #In an export this will quit the game.
        Zero.Game.Quit()
    
Zero.RegisterComponent("QuitProhibiter", QuitProhibiter)