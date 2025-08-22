# MES Shared Behaviors
MES Shared Behaviors or MSB is a behavior library for Modular Encounters Systems (MES) to allow Space Engineers modders to easily create complex encounters, while not having to set up that logic by themselves.

## How it works
Fundamentally, we differentiate between dynamic and static encounters. Static being ones consisting of static grids, dynamic being ones that move about. Some of the behaviors and systems contained within MSB make sense for static, some for dynamic encounters, but generally they are available to both.

When setting up an encounter with MSB - for example a Patrol - there are generally two important things that need to be defined, and upon whose distinction the entirety of MSB is built: Roles and CombatTypes. A dynamic encounter, in this case the Patrol encounter, will have one of each assigned to it and will switch back and forth between each of their logic, depending on whether it is in combat mode, or not. Static encounters generally do not have Roles, only CombatTypes, but there are some exceptions such as the Relay Role.

### Roles
[Roles](Content/Data/Behaviors/Roles) contain the logic of how an encounter behaves outside of combat. Generally, Roles can vary for the same prefab - i.e. a fighter prefab could be used with the Role Patrol, PatrolArea and Escort depending on the encounter. The currently available Roles are:
| Role | Status | Description |
| ---- | ---- | ---- |
| Cargoship | Working | Cargoship will have the encounter move in a straight line to a waypoint that is roughly 15km from their spawn, and then despawn. |
| DefensiveEscort | Working | Used for encounters that fly in formation with a leader but should not engage in combat as actively, such as cargoships in a convoy. |
| OffensiveEscort | Working | Used for encounters that fly in formation with a leader and should engage in combat actively and from further away. Used for escorting fighters, or members of a strike / task force. |
| Patrol | Working | Patrol will have the encounter move in a straight line to a waypoint that is roughly 15km from their spawn, and then despawn. |
| PatrolArea | Working | PatrolArea makes the encounter continuously create random waypoints in an area, to which it will move - and then create a new random waypoint. After between 10 and 15min, it will despawn. |
| Scout | Working | This encounter works in both space and gravity. Flies in a straight line to a despawn point roughly 15km away. Periodically, it stops and initiates a long range scan by charging up for a period of time (and indicating it in its GPS signal) and then extending its detection range to 5km. If it detects a player static grid, it approaches it to around 2.5km. Then it attempts to reach its original despawn point. If it reaches its despawn point, it creates a Known Player Area and activates a trigger tag allowing for an encounter with the Relay Role to be spawned. |
| Raider | Working | Only spawns within KnownPlayerAreas. Searches the area to find player grids and attacks them. Times out if it has not found anything after 10-15min. |
| Relay | Working | A role intended for **static** encounters. When it is destroyed, it clears the Known Player Area it is located in. |
| BountyHunter | Planned | If player reputation with a faction (except SPRT) drops to a low enough point, encounters with this role can spawn. They fly directly to the player and offer the player a chance to pay them off - else they will attack the player. |
| Merchant | Planned | Will fly in a straight line. If it detects a player static grid, it will land nearby and open its doors to give access to a store block. If the player approaches it while it's flying, it also stops to let the player board and trade. Despawns after reaching original waypoint roughly 15km from its spawn. |
| Guard | Planned |  |
| Salvager | Planned |  |
| Miner | Planned |  |

A Role is assigned to an encounter by referencing its triggergroup in the behavior: `[TriggerGroups:MSB_Cargoship_TriggerGroup]` (example for Cargoship)
An encounter cannot have more than one Role.

### CombatTypes
[CombatTypes](Content/Data/Behaviors/CombatTypes) contain the logic of how an encounter behaves during combat. Generally, the CombatType depends on the prefab - i.e. if you have a prefab of a SPRT freighter you would usually use the Freighter CombatType for all encounters that use this prefab. The currently available CombatTypes are:
| CombatType | Status | Description |
| ---- | ---- | ---- |
| Fighter | Working | The encounter will fly in a fighter plane style: Fast moving and attempting attack runs. It will also attempt to shake off any pursuers by doing various maneuvers. It will attempt to face its front towards its target and thus is ideal for encounters with front-facing weapons. |
| Freighter | Working | The encounter will attempt to continue to its waypoint but also try to evade if being fired upon. Only suitable for encounters with no or turreted weapons. |
| Gunship | Working | The encounter will attempt to chase its target, but not necessarily point its front at the target, making it more suitable for turret or mixed turret and front-facing weapons. |
| Capital | WIP |  |
| Nautical | WIP |  |
| Dropship | Planned |  |
| Rover | Planned |  |
| Hover | Planned |  |
| Static | WIP |  |

A CombatType is assigned to an encounter by referencing its triggergroup in the behavior: `[TriggerGroups:MSB_Freighter_TriggerGroup]` (example for Freighter)
An encounter cannot have more than one CombatType.

### Common TriggerGroups
There are two Common TriggerGroups - [`MSB_DynamicCommon_TriggerGroup`](https://github.com/enenra/mes-shared-behaviors/blob/f03f2df58cdb390fbabacea91656dd339ff351a1/Content/Data/Behaviors/_Common/_DynamicCommon.sbc#L8) and [`MSB_StaticCommon_TriggerGroup`](https://github.com/enenra/mes-shared-behaviors/blob/f03f2df58cdb390fbabacea91656dd339ff351a1/Content/Data/Behaviors/_Common/_StaticCommon.sbc#L8). They contain various logic that other parts of MSB rely on, including Roles and CombatTypes. Either of the two must be added to all encounters that use other MSB logic. They also provide useful places for logic inside your own mod to hook into.

### Systems
[Systems](Content/Data/Behaviors/Systems) contain various additional logic that can be referenced in encounters. They tie in with Roles and CombatTypes, and extend them in some cases.

| System | Status | Description |
| ---- | ---- | ---- |
| AreaRestriction | Done | Allows for setting restricted areas around encounters. If the player enters the defined range, they will first receive a warning. After 10s they will then lose rep every 10s with the owner faction for as long as they stay within the restricted range. |
| CommandChain | Working | Used to handle escorts and lead grids in an encounter that uses escorts. It's added to both the leader and the escorts and handles the logic for them joining up, the rename of the leader and notifications when the leader is destroyed. |
| Communication | Working | Allows encounters to send out SOS signals when entering battle. Other encounters who also have this system set up can then respond to those SOS signals and partake in combat. After combat has ended, both the sender and the responders return to their original Roles. |
| EngagementRange | Done | Defines the range to a target below which the encounter actively initiates combat and thus switches to its CombatType logic. |
| Environment | Working | Offers various options to make the encounter react to its environment, for example via Timer blocks with specific names being triggered or swapping a skin for another if spawning on specific voxels. |
| Dialogue | Working | Triggers various dialogue cues based on what is happening with and around the encounter. Must define DialogueBanks with corresponding cues in the behavior. |
| UniqueEncounters | Working | Manages unique and persistent dynamic encounters and ensures no two of them exist at the same time. Does not spawn a new encounter should the encounter be destroyed or removed by trash cleanup. |
| Defense | Working | Allows a static encounter to spawn guards to defend itself. |
| Crash | WIP |  |
| Despawn | WIP |  |
| Disabled | WIP |  |
| DynamicTarget | WIP |  |
| Health | WIP |  |
| Morale | WIP |  |
| PlayerKnownLocation | WIP |  |
| Terminate | WIP |  |

A System is assigned to an encounter by referencing its triggergroup in the behavior. Depending on the system, there may be multiple TriggerGroups available though, so be sure to read up on the description within its SBC file and reference the right one. Example for AreaRestriction: `[TriggerGroups:MSB_System_AreaRestriction_TriggerGroup_1000]` (establishes a restricted area of 1000m radius around the encounter)

## How to use
Usage of MSB requires knowledge of the creation of MES config files. While it makes the creation of encounter mods much easier, it still requires users to know their way around setting up their own side and being able to understand the way MSB works enough to use it.

### Autopilots
MSB does provide some [autopilot profiles](https://github.com/enenra/mes-shared-behaviors/tree/main/Content/Data/Behaviors/Autopilot) for your to use, but they are by no means obligatory. Note that there are autopilots for each Role and CombatType, as encounters with the Role currently active will use their primary autopilot, but once they swith to CombatType, they will be using the secondary (and in some cases tertiary) autopilot.

### TargetProfiles
MSB provides default [TargetProfiles](https://github.com/enenra/mes-shared-behaviors/tree/main/Content/Data/TargetProfiles), but those do not have to be used by encounters. The profiles included make detection work in the same way as the detection works for Reavers.

### TriggerEvents
TriggerEvents are triggered everywhere in MSB code, and can be used to hook additional logic into the existing one. For example, you can set up a dialogue system that listens to specific trigger tags to then play the corresponding chat lines.

### Utilities
[Utilities](https://github.com/enenra/mes-shared-behaviors/tree/main/Content/Data/Behaviors/Utilities) are lower-level logic packages used by Systems. They generally are not referenced within encounter mods, but logic could be written utilizing them.

### Interactions
[Interactions](Content/Data/Behaviors/Interactions) require the [MES Interactions Module](https://steamcommunity.com/sharedfiles/filedetails/?id=3547952468) mod. It allows players to send out interactions from antennas to encounters in broadcast range. Encounters set up to respond to them, can then initiate logic. An interaction in MSB is such a logic package.

| Interaction | Status | Description |
| ---- | ---- | ---- |
| TradeRequest | Working |  |
| VisitPlayerBase | WIP |  |

## Example Mods
* [GFA - Mining Guild Faction (MES)](https://github.com/enenra/gfa/tree/main/GFA%20-%20Mining%20Guild%20Faction/Content) - It's built entirely upon MSB and also extends MSB logic in multiple ways - for example by spawning AiEnabled crew.
* [GFA - MES Utilities](https://github.com/enenra/gfa/tree/main/GFA%20-%20MES%20Utilities/Content) - Supporting MES bits that are shared between multiple GFA encounter mods. Hooks into MSB to play jump-in and jump-out effects on spawn and despawn of dynamic encounters in space.
