#!/usr/bin/env python

class Channel:
    def __init__(self, name, modes, ts):
        self.name = name
        self.modes = modes
        self.topic = ''
        self.clients = []
        self.ts = ts

    def joined(self, client):
        self.clients.append(client)
        for c in self.clients:
            if c.conn:
                if c == client:
                    c._joined(self)
                else:
                    c._userJoined(client, self)

    def _left(self, client, message):
        for c in self.clients:
            if c.conn:
                if c == client:
                    c._left(self)
                else:
                    c._userLeft(client, self, message)
        self.clients.remove(client)

    def modeset(self, src, modes):
        print '%s modes %s' % (self, modes)

    def tschange(self, newts, modes):
        print '%s ts change %d %s' % (self, newts, modes)
        self.ts = newts

    def __str__(self):
        return self.name

    def _privmsg(self, source, dest, message):
        """ distribute messages to local clients """
        for  c in self.clients:
            if c.conn:
                if c != source:
                    c._privmsg(source, dest, message)

    def _noticed(self, source, dest, message):
        """ distribute notices to local clients """
        for c in self.clients:
            if c.conn:
                if c != source:
                    c._noticed(source, dest, message)

    def kick(self, kicker, kickee, message):
        """ distribute kick notifications """
        self.clients.remove(kickee)
        for c in self.clients:
            if c.conn:
                c._userKicked(kickee, self, kicker, message)
        kickee._kickedFrom(self, kicker, message)
