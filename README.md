# flat
A Python multiplayer game

Flat is a project that I created to experiment with sockets and multithreading in python.

The goal is to create a "perfect" game server which transmits exactly what clients need and nothing else. This will be accomplished with dictionary-like objects which track all changes to the data they hold, and are responsible for communicating these changes to remote duplicates of themselves using minimally-sized data packets.

These sync-responsible dictionaries, or DataHandlers, should also work when nested. That is, if a Datahandler currently tracking changes is the child of another DataHandler, and the parent DataHandler is asked for a summary of recent changes to be encoded and sent, it will ask its child DataHandler for a summary of changes, and nest this summary in the data to be sent.
The same should work in reverse; when a remote DataHandler recieves this data, it should decode the data into a pool of changes to apply, but give the nested summary to its child DataHandler.



here is an example of how DataHandlers might communicate a single attribute of a single player changing.

#The server and client both have this data:

players = DataHandler({
  1:DataHandler({"name":"notch","pos":(2,2),"hp":8}),
  2:DataHandler({"name":"jeb","pos":(2,3),"hp":1}),
  3:DataHandler({"name":"c418","pos":(2,4),"hp":7})
})

#and then c418 takes a hitpoint of damage. because the game modifies this value with the DataHandlers' local access methods, the DataHandlers track the change... "hp" is added to the change list for c418's DataHandler. c418's DataHandler is added to the change list for the players DataHandler.

#in the next tick, the server will send ask its nested DataHandlers for an update to send to the clients. they will produce this:

{3:{"hp":6}}

#which the server will encode and send.



Certain classes may extend the DataHandler class to add custom encoding formats for refreshes or updates. An object such as the game board, which consists of a large list of bytes or numbers, would normally be encoded by the DataHandler using __str__. But this more than doubles the size of the information to be sent, by including the commas and other symbols denoting the primative list. It would be better to send all the squares as a single concatenated string.
To accomplish this, a specialized class to handle uniform-length objects is created. It inherits most of its methods from the DataHandler, but overrides getRefresh and putRefresh with new definitions which use concatenated strings to represent the source in a refresh.

To-do:
* Break out encoding methods into a new class.
* Make DataHandler and then ByteHandler work, in a predictable and explainable manner.
* Make children of DataHandlers register themselves in the changes pool when they change themselves.
* Make game data sync correctly, and make client draw opponents.
* Create some sort of type-monitoring overviewer to help with debugging.
* Add my Dig debugger to the project, but enhance it to collapse near-duplicate outputs.
* Make server send updates to client without blocking to wait for a response.
* Separate the server into distinct game-responsible and network-responsible components.
* Add an intelligent filter to remove unnecessary update/refresh info for each client.
* Tile individual boards into a larger world.
* Make clients search for servers on LAN.
* Catch OS-thrown exceptions.
* Remake this all in Javascript.



This project's development has been slowed by outside forces.
