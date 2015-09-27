#!/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = "1.0"

print("JeDaBot {}\nThe smart people are the ones who fails. Without fails, people are morons.\n".format(__version__))

try:
    from conf.configuration import *
except ImportError:
    print('JeDaBot cannot found configuration.py - Please rename configuration.py.example to configuration.py on the conf folder and edit it.')
    sys.exit(1)
except Exception as err:
    print('JeDaBot cannot load the configuration: {}'.format(err))
    sys.exit(1)
from bin.client import IRCClient
import random
import re
import signal
import sys
import time

irc = IRCClient()

def ctcphandler(cli, ev):
    if ev.arguments[0] == "PING":
        cli.ctcp_reply(ev.source, "PING " + ev.arguments[1])
    elif ev.arguments[0] == "USERINFO":
        cli.ctcp_reply(ev.source, "USERINFO {}, a bot with JeDaBot's brain.".format(cli.nickname))
    elif ev.arguments[0] == "VERSION":
        cli.ctcp_reply(ev.source, "VERSION JeDaBot {}".format(__version__))

def welcomehandler(cli, ev):
    if PASS != "":
        if USERNAME == "":
            authuser = NICK
        else:
            authuser = USERNAME
        cli.privmsg("NickServ", "identify {} {}".format(authuser, PASS))
    for val in CHANNELS:
        cli.join(val)

def invited(cli, ev):
    cli.join(ev.arguments[0])
    
def _iscommand(ev):
    if ev.type == "pubmsg":
        try:
            x = PREFIX
            if isinstance(x, list):
                for i in x:
                    p1 = re.compile("^" + re.escape(i) +
                        "(\S{1,52})[ ]?(.*)", re.IGNORECASE)
                    m1 = p1.search(ev.arguments[0])
                    if m1 is not None:
                        return m1
            elif isinstance(x, str):
                p1 = re.compile("^" + re.escape(x) +
                    "(\S{1,52})[ ]?(.*)", re.IGNORECASE)
                m1 = p1.search(ev.arguments[0])
                if m1 is not None and x != "":
                    return m1
        except:
            pass
        p1 = re.compile("^" + re.escape("!") +
            "(\S{1,52})[ ]?(.*)", re.IGNORECASE)
    else:
        p1 = re.compile("^(?:" + re.escape("!") +
            ")?(\S{1,52})[ ]?(.*)", re.IGNORECASE)
    m1 = p1.search(ev.arguments[0])
    return m1

def is_staff(nick):
    if nick == OWNER:
        return True
    elif nick in ADMINS:
        return True
    else:
        return False

def commandhandler(cli, ev):
    m1 = _iscommand(ev)

    p2 = re.compile("^" + re.escape(cli.nickname) +
        "[:, ]? (\S{1,52})[ ]?(.*)", re.IGNORECASE)
    m2 = p2.search(ev.arguments[0])
    if not m1 is None:
        try:
            del ev.splitd[0]
        except:
            pass  # ???
        com = m1.group(1)
    elif not m2 is None:
        del ev.splitd[0]
        del ev.splitd[0]
        com = m2.group(1)

    if not m1 is None or not m2 is None:
        if com == "raw":
            if is_staff(ev.source):
                cli.send(" ".join(ev.splitd))
            else:
                cli.msg(ev.target, ev.source + ": STOP DREAMING YOU FREAK?!?!??!?!??!?!?")
        elif com == "join":
            if is_staff(ev.source):
                cli.send("JOIN " + ev.splitd[0])
            else:
                cli.msg(ev.target, ev.source + ": STOP DREAMING YOU FREAK?!?!??!?!??!?!?")
        elif com == "part":
            if is_staff(ev.source):
                cli.send("PART " + ev.splitd[0])
            else:
                cli.msg(ev.target, ev.source + ": STOP DREAMING YOU FREAK?!?!??!?!??!?!?")
        elif com == "disconnect" or com == "quit":
            if is_staff(ev.source):
                cli.disconnect(" ".join(ev.splitd))
                sys.exit(0)
            else:
                cli.msg(ev.target, ev.source + ": STOP DREAMING YOU FREAK?!?!??!?!??!?!?")
        elif com == "reconnect":
            if is_staff(ev.source):
                cli.quit(" ".join(ev.splitd))
            else:
                cli.msg(ev.target, ev.source + ": STOP DREAMING YOU FREAK?!?!??!?!??!?!?")
        elif com == "msg":
            if is_staff(ev.source):
                cli.privmsg(ev.splitd[0], " ".join(ev.splitd).replace(ev.splitd[0] + " ", ""))
            else:
                cli.msg(ev.target, ev.source + ": STOP DREAMING YOU FREAK?!?!??!?!??!?!?")
        elif com == "notice":
            if is_staff(ev.source):
                cli.notice(ev.splitd[0], " ".join(ev.splitd).replace(ev.splitd[0] + " ", ""))
            else:
                cli.msg(ev.target, ev.source + ": STOP DREAMING YOU FREAK?!?!??!?!??!?!?")
        elif com == "meow":
            cli.msg(ev.target, random.choice(["“I’m trying to translate what my cat says and put it in a book, but how many homonyms are there for meow?” ― Jarod Kintz", "“I want to start a business making mint-flavored sunshine that comes in a can half full of meow-free rainbows. (Leprechauns sold separately.)” ― Jarod Kintz", "“Chairs have legs. Four of them, like my father. Meow.” ― Jarod Kintz", "“Be honest because you stole it, not because blue/green/yell a little yellow. Dandelions just don’t meow like regular lions.” ― Jarod Kintz", "“I have a bedroom rug that I feed. It’s not very flat, and it meows when I step on it.” ― Jarod Kintz", "“I bought you a box of karate chops, but it could be dangerous to open it with a knife. And cats are masters at getting into boxes, so here, try opening it with my portable meow maker. ” ― Jarod Kintz", "“Some dogs look like giant mustaches. I shaved mine off because it was barking too much. My love life has improved by leaps and meows.” ― Jarod Kintz"]))

def signal_handler(signum, frame):
    signals = dict((getattr(signal, n), n) for n in dir(signal) if n.startswith('SIG') and '_' not in n )
    print('\nReceived {}\n'.format(signals[signum]))
    irc.disconnect('Received {}'.format(signals[signum]))
    sys.exit(0)

irc.addhandler("ctcp", ctcphandler)
irc.addhandler("invite", invited)
irc.addhandler("privmsg", commandhandler)
irc.addhandler("pubmsg", commandhandler)
irc.addhandler("privnotice", commandhandler)
irc.addhandler("pubnotice", commandhandler)
irc.addhandler("welcome", welcomehandler)
try:
    irc.connect(HOST, PORT, NICK, IDENT, REALNAME)
except:
    print("\nError trying to connect. Exiting...")
    sys.exit(1)
            
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

while True:
    time.sleep(0.1) 

