# Created by Nick N. Zinovenko
# This code is freely distributable under the terms of the [MIT license]


from d3 import *

registry = subsystems.getSystem(SockPuppetSystem).registry
uidManager = UidManager.get()


def getCurrentTrackTime():
    return guisystem.player.tCurrent


def _createDmxLayer(moduleType, personality, name, universe, channel, at, length):
    if not personality:
        personality = registry.getPersonality(moduleType.__name__)

    layer = guisystem.track.addNewLayer(moduleType, at, length, name)
    layer.controlPatch = DmxPatch.make(channel, universe, personality)
    layer.activate()

    return layer


def createNewLayer(type, iver, name, universe, channel, at, length):
    MODULES = {'Colour': ColourModule, 'Video': SockPuppetVideoModule}
    moduleType = MODULES.get(type)
    if moduleType is None:
        return

    className = moduleType.__name__
    personality = (
        registry.getPersonality(moduleType.__name__)  # default version
        if iver is None
        else registry.personalityVersion(className, iver)
    )

    layer = _createDmxLayer(moduleType, personality, name, universe, channel, at, length)
    return layer.uid


def groupLayers(layerUIDs, groupName):
    layers = [uidManager.getResource(int(uid)) for uid in layerUIDs]
    guisystem.track.groupLayers(layers, groupName, False)


def getPersonality(className):
    item = registry.getPersonality(className)
    return {
        'iver': registry.iVersionSelected(className),
        'ver': item.vmapVersion,
        'dmx': DmxPatch.staticTotalChannels(item),
    }


def getPersonalityList(className):
    return [
        {
            'iver': idx,
            'ver': item.vmapVersion,
            'dmx': DmxPatch.staticTotalChannels(item),
        }
        for item, idx in (
            (registry.personalityVersion(className, idx), idx)
            for idx in reversed(range(registry.nVersions(className)))
        )
    ]


def resetDmxPatch():
    for item in resourceManager.allResources(type=DmxPatch):
        layer = item.parent  # type: Layer
        layer.controlPatch = None


__all__ = [
    'createNewLayer',
    'getCurrentTrackTime',
    'getPersonality',
    'getPersonalityList',
    'groupLayers',
    'resetDmxPatch',
]
