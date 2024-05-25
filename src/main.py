import creep_roles
import math
import random
# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from defs import *

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


#This sets up "memhack", which saves CPU by remembering the contents of Memory between ticks.
my_memory = Memory
my_memory = RawMemory._parsed


#This keeps track of every time your script experiences a global reset, which means that the server reloaded it fresh. It happens every time you push your code, and also happens occasionally without your input.
if my_memory.reset_log == None:
    my_memory.reset_log = []
if my_memory.last_reset != None:
    print(' ======= Global reset! Time of reset: ' + Game.time + ' Time since last reset: ' + (Game.time - my_memory.last_reset) + ' ======= ')
    my_memory.reset_log.append(Game.time - my_memory.last_reset)
    while len(my_memory.reset_log) > 10:
        my_memory.reset_log.pop(0)
my_memory.last_reset = Game.time


#This sets up Cache, which is lost on global reset, but takes no Memory space and is cheaper on CPU than Memory. If it doesn't matter for something to be forgotten sometimes, it's better to put it in Cache than Memory.
Cache = {}
creep_roles.init_cache()
Cache.rooms = {}


#This sets up some parts of Memory if they're not set yet.
if my_memory.creeps == None:
    my_memory.creeps = {}
if my_memory.rooms == None:
    my_memory.rooms = {}
if my_memory.spawns == None:
    my_memory.spawns = {}


#This function turns the long creep body array into a shorter form for readability in the console
def body_shorthand(body):
    body_count = {}
    for part in body:
        if body_count[part] == None:
            body_count[part] = 1
        else:
            body_count[part] += 1
    outstring = ''
    for part_type in Object.keys(body_count):
        outstring += '' + body_count[part_type] + part_type + ' '
    return outstring

        
def main():
    """
    Main game logic loop.
    """
    
    
    #This is the in-loop part of memhack.
    __pragma__ ('js', '{}', 'delete global.Memory;')
    __pragma__ ('js', '{}', 'global.Memory = my_memory;')
    __pragma__ ('js', '{}', 'RawMemory._parsed = my_memory;')
    
    
    #This catalogues your owned rooms.
    Cache.owned_rooms = []
    for room_name in Object.keys(Game.rooms):
        room = Game.rooms[room_name]
        if room.controller != None and room.controller.my:
            if Cache.rooms[room_name] == None:
                Cache.rooms[room_name] = {}
            Cache.owned_rooms.append(room_name)
            Cache.rooms[room_name].current_work_parts = 0
            Cache.rooms[room_name].current_carry_parts = 0
    
    
    #This clears out memory of creeps, rooms, and spawns that no longer exist.
    for name in Object.keys(Memory.creeps):
        if Game.creeps[name] == None:
            print('RIP ' + name)
            del Memory.creeps[name]
    for name in Object.keys(Memory.rooms):
        if Game.rooms[name] == None:
            del Memory.rooms[name]
    for name in Object.keys(Memory.spawns):
        if Game.spawns[name] == None:
            del Memory.spawns[name]
    
    
    #This runs the action function for each creep, as defined in the creep_roles.py module.
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if not creep.spawning:
            creep_roles.do_action(creep)
    
    
    #This tries to activate safe mode if your spawn gets damaged.
    for spawn_name in Object.keys(Game.spawns):
        spawn = Game.spawns[spawn_name]
        if spawn.hits < spawn.hitsMax and spawn.room.controller.my:
            spawn.room.controller.activateSafeMode()
    
    
    #All spawning related code runs every 3 ticks, because creep spawning duration is always a mutliple of 3 ticks.
    if Game.time % 3 == 0:
        #This prepares for unique creep names (because having multiple creeps with the same name is not allowed).
        timestamp = Game.time.toString().split("")
        timecode = 'snek '
        for i in range(4):
            char = timestamp[i + len(timestamp) - 4]
            if char == '0':
                timecode += '--'
            if char == '1':
                timecode += '-~'
            if char == '2':
                timecode += '~-'
            if char == '3':
                timecode += '~~'
            if char == '4':
                timecode += '=-'
            if char == '5':
                timecode += '-='
            if char == '6':
                timecode += '=='
            if char == '7':
                timecode += '=~'
            if char == '8':
                timecode += '~='
            if char == '9':
                timecode += '<>'
        timecode += ':3'
    
    
        #This catalogues how many active work parts our workers have and how many active carry parts our haulers have.
        for name in Object.keys(Game.creeps):
            creep = Game.creeps[name]
            if creep.memory.role == 'worker' and Cache.rooms[creep.memory.target_room] != None:
                Cache.rooms[creep.memory.target_room].current_work_parts += creep.getActiveBodyparts(WORK)
            if creep.memory.role == 'hauler' and (creep.ticksToLive > 150 or creep.spawning) and Cache.rooms[creep.memory.target_room] != None:
                Cache.rooms[creep.memory.target_room].current_carry_parts += creep.getActiveBodyparts(CARRY)
        
        #This number tracks how many total creeps have been spawned so far on this tick.
        num_spawns = 0
        
        for room_name in Cache.owned_rooms:
            room = Game.rooms[room_name]
            
            #This finds all of your spawns in the room.
            spawns = room.find(FIND_MY_SPAWNS)
            
            #This keeps track of how much energy we've used on spawning creeps so far this tick (for cases where we have multiple spawns in a room)
            used_energy = 0
            
            for spawn in spawns:
                if not spawn.isActive():
                    continue
                if spawn.spawning:
                    if spawn.spawning.remainingTime <= 1:
                        creeps = spawn.pos.findInRange(FIND_MY_CREEPS, 1)
                        for creep in creeps:
                            creep.moveTo(room.controller)
                    continue
                #This constructs a creep name from the timecode we made earlier, adding an 's' to the front for every previous creep we've spawned on this tick.
                name = ''
                for i in range(num_spawns):
                    name += 's'
                name += timecode
                
                
                #This creates a list of all of our creeps with this room as their target room, which we can filter later.
                creep_names = filter(lambda n: Game.creeps[n].memory.target_room == room.name, Object.keys(Game.creeps))
                current_creeps = []
                for creep_name in creep_names:
                    current_creeps.append(Game.creeps[creep_name])
                
                #Check how many miners we have, because we might have to spawn smaller miners if we don't have any.
                num_miners = len(filter(lambda c: c.memory.role == 'miner', current_creeps))
                
                
                #Spawn miners if we have at least one hauler.
                sources = room.find(FIND_SOURCES)
                if Cache.rooms[room_name].current_carry_parts > 0:
                    spawned = False
                    for source in sources:
                        current_miners = filter(lambda c: c.memory.role == 'miner' and c.memory.target == source.id and (c.spawning or (c.ticksToLive > 50)), current_creeps)
                        if len(current_miners) == 0:
                            energy_to_use = room.energyCapacityAvailable
                            if room.memory.no_miner_ticks > 20:
                                energy_to_use = room.energyAvailable
                            miner_multiple = min(3, math.floor(energy_to_use / 250))
                            body = []
                            cost = 0
                            for i in range(miner_multiple):
                                body.append(WORK)
                                body.append(WORK)
                                cost += 200
                            for i in range(miner_multiple):
                                body.append(MOVE)
                                cost += 50
                            if room.energyAvailable - used_energy >= cost:
                                result = spawn.spawnCreep(body, name, {'memory': {'target_room': room.name, 'role': "miner", 'target': source.id}})
                                if result == OK:
                                    room.memory.no_miner_ticks = 0
                                    num_spawns += 1
                                    used_energy += cost
                                elif result == ERR_NOT_ENOUGH_ENERGY and len(current_miners) == 0:
                                    if room.memory.no_miner_ticks == None:
                                        room.memory.no_miner_ticks = 0
                                    room.memory.no_miner_ticks += 1
                            spawned = True
                            break
                    if spawned:
                        continue
                
                
                #This calculates the income based on the number of sources and the size of our miners. That is used to scale our hauler and worker spawning.
                miner_multiple = min(3, math.floor(room.energyCapacityAvailable / 250))
                income = len(sources) * min(10, 4 * miner_multiple)
                
                
                #Spawn haulers if we have less carry parts than three times our income.
                if Cache.rooms[room_name].current_carry_parts < income * 3:
                    #Use the current energy available in the room rather than the maximum if there are no haulers currently.
                    energy_to_use = spawn.room.energyCapacityAvailable
                    if Cache.rooms[room_name].current_carry_parts == 0:
                        energy_to_use = spawn.room.energyAvailable
                    hauler_multiple = min(16, math.floor(energy_to_use / 150))
                    part_change = 0
                    body = []
                    cost = 0
                    for i in range(hauler_multiple):
                        body.append(CARRY)
                        body.append(CARRY)
                        body.append(MOVE)
                        part_change += 2
                        cost += 150
                    if room.energyAvailable - used_energy >= cost:
                        result = spawn.spawnCreep(body, name, {'memory': {'target_room': room.name, 'role': "hauler"}})
                        if result == OK:
                            num_spawns += 1
                            used_energy += cost
                            Cache.rooms[room_name].current_carry_parts += part_change
                            print(spawn.room.name + ' spawned hauler ' + name + ' with body ' + body_shorthand(body))
                    continue
                
                
                #Spawn workers if we have less work parts than our income.
                if Cache.rooms[room_name].current_work_parts < income:
                    worker_multiple = min(16, math.floor(spawn.room.energyCapacityAvailable / 200))
                    body = []
                    cost = 0
                    part_change = 0
                    for i in range(worker_multiple):
                        body.append(WORK)
                        part_change += 1
                        cost += 100
                    for i in range(worker_multiple):
                        body.append(CARRY)
                        cost += 50
                    for i in range(worker_multiple):
                        body.append(MOVE)
                        cost += 50
                    if room.energyAvailable - used_energy >= cost:
                        result = spawn.spawnCreep(body, name, {'memory': {'target_room': room.name, 'role': "worker"}})
                        if result == OK:
                            num_spawns += 1
                            used_energy += cost
                            Cache.rooms[room_name].current_work_parts += part_change
                            print(spawn.room.name + ' spawned worker ' + name + ' with body ' + body_shorthand(body))
                    continue
                
                
                #If we got here without trying to spawn anything, skip the remaining spawns.
                break

    
    
    
    #It's likely that you won't fully utilize your CPU when starting out, so this will use your excess CPU to generate pixels that you can sell later.
    if Game.cpu.generatePixel and Game.cpu.bucket == 10000 and Game.cpu.getUsed() < Game.cpu.limit and ['shard0', 'shard1', 'shard2', 'shard3'].includes(Game.shard.name):
        if Game.cpu.generatePixel() == OK:
            print(' ======= Generating pixel! Press F to pay respects to your bucket! ======= ')

module.exports.loop = main