screeps_starter_python
======================
This is my updated and streamlined version of daboross's screeps-starter-python repo. This is very much built on his work, but I added a bit of stuff on top that will hopefully make things much nicer for those interested in playing Screeps with Python.

## Contact

If you hop into the #python channel in the Screeps official Discord, I'll be happy to answer any questions there.

## Setup Guide

The first thing you need to do is to install Python 3.13 (includeing IDLE, which is bundled with it by default on Windows) and Node.js 17.9.1 (Including NPM, which is bundled with it). Those listed versions are the newest versions that will work, newer versions than that are known to not work. Older version than those may work in many cases.

Next, copy the repository to your local device one of a number of ways. My recommended way would probably be to install the GitHub desktop app and pull it that way, I've found it to be quite easy and convenient. The second method (and the one recommended by the original creator of the starter) is to install Git normally and run `git clone https://github.com/DroidFreak36/screeps_starter_python.git` in the folder you want to clone the repository into. If you want, you could also download the repository as a zip and unzip it locally.

Next, you have to set up the config file. To push code to the official server, make a copy of `config.default.json` and name it `config.json`, then insert your auth token (generated through "Manage Account" in-game). For a private server, copy `config.private-server-example.json` into `config.json` instead and set up the settings as needed.

Once the config is set up, open the `build.py` through IDLE (by right-clicking and selecting "Edit with IDLE" or by opening IDLE directly and opening the file through its menus. Once you have the file open in IDLE, use the run menu to run it. It will set up everything for you, and if it runs into any errors, it will tell you what they are in a useful format.

Once you have the build working, take a look at the source code in the `src` subfolder, and start editing it into whatever you want. :3

## Changes

In the version I forked from, it's often necessary to use Transcrypt pragmas to tell it to treat certain lines of code as raw Javascript, since those lines get removed or otherwise don't work otherwise. In my edited build.py, it pre-patches your code before Transcrypt to add those lines where it thinks you will need them. This may cause unexpected behavior in some cases, but it should make things much less clunky in the majority of cases. If you run into any cases where it doesn't work properly, let me know and I'll see what I can do about fixing that.

In addition to that pre-patching, it also patches up the JS code that Transcrypt produces, replacing some bad monkeypatches (edits to built-in objects) with ones that are formatted better. With the original bad monkeypatches, it caused some of Screep's own built-in methods to malfunction. It also unifies the global variable "Cache" across the two modules of the example bot. This unification code can be extended to apply to additional globals and modules, but I left it at just Cache for the starter.

The actual starter bot itself is replaced as well, being slightly more advanced, but still very much a starter. It will spawn three creep roles - miners, haulers, and workers. It will not place any structures, but it will build and maintain ones you place, as well as using extensions and source containers.

## Tips

Be sure to check the syntax changes part of [The Book](https://daboross.gitbooks.io/screeps-starter-python/). Some of the other sections may be useful to read as well. In particular, keep in mind that the keys to all objects you create should be in quotes so that they properly get interpreted as strings rather than variables. Again, I can help in the #python channel of the Screeps Discord if you run into any issues.

## Original Docs Follow:

[![MIT licensed][mit-badge]][mit-url]
[![Slack Chat][slack-badge]][slack-url]
[![Docs Built][docs-badge]][docs-url]

This repository is a starter Python AI written for the JavaScript based MMO
game, [screeps](https://screeps.com).


While code uploaded to the server must be in JavaScript, this repository is
written in Python. We use the [Transcrypt](https://github.com/QQuick/Transcrypt)
transpiler to transpile the python programming into JavaScript.

Specifically, it uses [my fork of
transcrypt](https://github.com/daboross/Transcrypt) built with [a few
modifications](https://github.com/daboross/Transcrypt/commits/screeps-safe-modifications)
intended to reduce the overhead of running Python in the Screeps
environment. Nothing against Transcrypt itself, and you're free to change the
installed fork my modifying `requirements.txt`! I've just found a few changes
useful that I've tested in node.js and the screeps environment, but that I don't
have time to generalize enough to include in the main transcrypt codebase.

This repository is intended as a base to be used for building more complex AIs,
and has all the tooling needed to transpile Python into JavaScript set up.

## Docs

For a documentation index, see [The
Book](https://daboross.gitbooks.io/screeps-starter-python/), and for the
main differences between Python and Transcrypt-flavored-Python, see [Syntax
Changes](https://daboross.gitbooks.io/screeps-starter-python/syntax-changes/).

## Community

Join us on the [Screeps Slack][slack-url]! We're in
[#python](https://screeps.slack.com/archives/C2FNJBGH0) (though you need to sign
up with the first link first :).

[mit-badge]: https://img.shields.io/badge/license-MIT-blue.svg
[mit-url]: https://github.com/daboross/screeps-starter-python/blob/master/LICENSE
[slack-badge]: https://img.shields.io/badge/chat-slack-2EB67D
[slack-url]: https://chat.screeps.com/

[docs-badge]: https://img.shields.io/badge/docs-built-blue
[docs-url]: https://daboross.gitbook.io/screeps-starter-python/logistics/setup
