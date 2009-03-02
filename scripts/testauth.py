﻿#!/usr/bin/env python
# -*- coding: utf-8
import Ice, sys

Ice.loadSlice('Murmur.ice') 
import Murmur

class ServerAuthenticatorI(Murmur.ServerUpdatingAuthenticator):
    def __init__(self, server, adapter):
      self.server = server
      
    def authenticate(self, name, pw, current=None):
      if (name == "One"):
        if (pw == "Magic"):
          return (1, "One", None)
        else:
          return (-1, None, None)
      elif (name == "Two"):
        if (pw == "Mushroom"):
          return (2, "twO", None)
        else:
          return (-1, None, None)
      return (-2, None, None)
      
      
    def nameToId(self, name, current=None):
      if (name == "One"):
        return 1
      elif (name == "Twoer"):
        return 2
      else:
        return -2;

    def idToName(self, id, current=None):
      if (id == 1):
        return "One"
      elif (id == 2):
        return "Two"
      else:
        return None
        
    def idToTexture(self, id, current=None):
      return None
      
    # The expanded methods from UpdatingAuthenticator. We only implement a subset for this example, but
    # a valid implementation has to define all of them
    def registerPlayer(self, name, current=None):
      print "Someone tried to register " + name
      return -2
      
    def unregisterPlayer(self, id, current=None):
      return -2
      
    def getRegistration(self, id, current=None):
      return (-2, None, None)
    
if __name__ == "__main__":
    global contextR

    print "Creating callbacks...",
    ice = Ice.initialize(sys.argv)
    
    meta = Murmur.MetaPrx.checkedCast(ice.stringToProxy('Meta:tcp -h 127.0.0.1 -p 6502'))

    adapter = ice.createObjectAdapterWithEndpoints("Callback.Client", "tcp -h 127.0.0.1")
    adapter.activate()

    for server in meta.getBootedServers():
      serverR=Murmur.ServerUpdatingAuthenticatorPrx.uncheckedCast(adapter.addWithUUID(ServerAuthenticatorI(server, adapter)))
      server.setAuthenticator(serverR)
#      server.registerPlayer("TestPlayer")

    print "Done"

    for server in meta.getBootedServers():
      ids= server.getPlayerIds(["TestPlayer"])
      for name,id in ids.iteritems():
        server.unregisterPlayer(id)
      server.registerPlayer("TestPlayer")

    print 'Script running (press CTRL-C to abort)';
    try:
        ice.waitForShutdown()
    except KeyboardInterrupt:
        print 'CTRL-C caught, aborting'

    meta.removeCallback(metaR)
    ice.shutdown()
    print "Goodbye"