# MES Shared Behaviors
MES Shared Behaviors or MSB is a behavior library for Modular Encounters Systems (MES) to allow Space Engineers modders to easily create complex encounters, while not having to set up that logic by themselves.

## How it works
Fundamentally, we differentiate between dynamic and static encounters. Static being ones consisting of static grids, dynamic being ones that move about. Some of the behaviors and systems contained within MSB make sense for static, some for dynamic encounters, but generally they are available to both.

When setting up an encounter with MSB - for example a Patrol - there are generally two important things that need to be defined, and upon whose distinction the entirety of MSB is built: Roles and CombatTypes. An dynamic encounter, in this case the Patrol encounter, will have one of each assigned to it and will switch back and forth between their logics depending on whether it is in combat mode, or not. Static encounters generally do not have Roles, only CombatTypes.

### Roles
[Roles](Content/Data/Behaviors/Roles) contain the logic of how an encounter behaves outside of combat. Generally, Roles can vary for the same prefab - i.e. a fighter prefab could be used with the Role Patrol, PatrolArea and Escort depending on the encounter. The currently available Roles are:
| Role | Status | Description |
| ---- | ---- | ---- |
| Cargoship | Working | Cargoship will have the encounter move in a straight line to a waypoint that is roughly 15km from their spawn, and then despawn. |
| DefensiveEscort | Working |  |
| OffensiveEscort | Working |  |
| Patrol | Working | Patrol will have the encounter move in a straight line to a waypoint that is roughly 15km from their spawn, and then despawn. |
| PatrolArea | Working | PatrolArea makes the encounter continuously create random waypoints in an area, to which it will move - and then create a new random waypoint. After between 10 and 15min, it will despawn. |
| ConvoyLeader | WIP |  |
| StrikeForceLeader | WIP |  |
| TaskForceLeader | WIP |  |
| BountyHunter | Planned |  |
| Guard | Planned |  |
| Hunter | Planned |  |
| Merchant | Planned |  |
| Raider | Planned |  |
| Salvager | Planned |  |
| Scout | Planned |  |

A Role is assigned to an encounter by referencing its triggergroup in the behavior: `[TriggerGroups:MSB_Cargoship_TriggerGroup]` (example for Cargoship)

### CombatTypes
[CombatTypes](Content/Data/Behaviors/CombatTypes) contain the logic of how an encounter behaves during combat. Generally, the CombatType depends on the prefab - i.e. if you have a prefab of a SPRT freighter you would usually use the Freighter CombatType for all encounters that use this prefab. The currently available CombatTypes are:
| CombatType | Status | Description |
| ---- | ---- | ---- |
| Fighter | Working | The encounter will fly in a fighter plane style: Fast moving and attempting attack runs. It will also attempt to shake off any pursuers by doing various maneuvers. It will attempt to face its front towards its target and thus is ideal for encounters with front-facing weapons. |
| Freighter | Working | The encounter will attempt to continue to its waypoint but also try to evade if being fired upon. Only suitable for encounters with no or turreted weapons. |
| Gunship | Working | The encounter will attempt to chase its target, but not necessarily point its front at the target, making it more suitable for turret or mixed turret and front-facing weapons. |
| Dropship | WIP |  |
| Rover | WIP |  |
| Static | WIP |  |

A CombatType is assigned to an encounter by referencing its triggergroup in the behavior: `[TriggerGroups:MSB_Freighter_TriggerGroup]` (example for Freighter)

### Common TriggerGroups
There are two Common TriggerGroups - [`MSB_DynamicCommon_TriggerGroup`](https://github.com/enenra/mes-shared-behaviors/blob/f03f2df58cdb390fbabacea91656dd339ff351a1/Content/Data/Behaviors/_Common/_DynamicCommon.sbc#L8) and [`MSB_StaticCommon_TriggerGroup`](https://github.com/enenra/mes-shared-behaviors/blob/f03f2df58cdb390fbabacea91656dd339ff351a1/Content/Data/Behaviors/_Common/_StaticCommon.sbc#L8). They contain various logic that other parts of MSB rely on, including Roles and CombatTypes. Either of the two must be added to all encounters that use other MSB logic.

### Systems
[Systems](Content/Data/Behaviors/Systems) contain various additional logic that can be referenced in encounters. They tie in with Roles and CombatTypes, and extend them in some cases.

| System | Status | Description |
| ---- | ---- | ---- |
| AreaRestriction | Done | Allows for setting restricted areas around encounters. If the player enters the defined range, they will first receive a warning. After 10s they will then lose rep every 10s with the owner faction for as long as they stay within the restricted range. |
| CommandChain | Working | Used to handle escorts and lead grids in an encounter that uses escorts. It's added to both the leader and the escorts and handles the logic for them joining up, the rename of the leader and notifications when the leader is destroyed. |
| Communication | Working | Allows encounters to send out SOS signals when entering battle. Other encounters who also have this system set up can then respond to those SOS signals and partake in combat. After combat has ended, both the sender and the responders return to their original Roles. |
| EngagementRange | Done | Defines the range to a target below which the encounter actively initiates combat and thus switches to its CombatType logic. |
| Environment | Working | Offers various options to make the encounter react to its environment, for example via Timer blocks with specific names being triggered or swapping a skin for another if spawning on specific voxels. |
| Crash | WIP |  |
| Despawn | WIP |  |
| Disabled | WIP |  |
| DynamicTarget | WIP |  |
| Health | WIP |  |
| Morale | WIP |  |
| PlayerKnownLocation | WIP |  |
| Terminate | WIP |  |

A System is assigned to an encounter by referencing its triggergroup in the behavior. Depending on the system, there may be multiple TriggerGroups available though, so be sure to read up on it and reference the right one. Example for AreaRestriction: `[TriggerGroups:MSB_System_AreaRestriction_TriggerGroup_1000]` (establishes a restricted area of 1000km radius around the encounter)

## How to use
Usage of MSB requires knowledge of the creation of MES config files. While it makes the creation of encounter mods much easier, it still requires users to know their way around setting up their own side and being able to understand the way MSB works enough to use it.

### Autopilots

### TargetProfiles

### TriggerEvents

### Utilities

## Example Mods
* [GFA - Mining Guild Faction (MES)](https://github.com/enenra/gfa/tree/main/GFA%20-%20Mining%20Guild%20Faction/Content) - It's built entirely upon MSB and also extends MSB logic in multiple ways - for example by spawning AiEnabled crew, and implementing an extensive dialogue system based on the TriggerEvents MSB provides.
