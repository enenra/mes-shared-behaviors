# MES Shared Behaviors
MES Shared Behaviors or MSB is a behavior library for Modular Encounters Systems (MES) to allow Space Engineers modders to easily create complex encounters, while not having to set up that logic by themselves.

## How it works
Fundamentally, we differentiate between dynamic and static encounters. Static being ones consisting of static grids, dynamic being ones that move about. Some of the behaviors and systems contained within MSB make sense for static, some for dynamic encounters, but generally they are available to both.

When setting up an encounter with MSB - for example a Patrol - there are generally two important things that need to be defined, and upon whose distinction the entirety of MSB is built: Roles and CombatTypes. An dynamic encounter, in this case the Patrol encounter, will have one of each assigned to it and will switch back and forth between their logics depending on whether it is in combat mode, or not. Static encounters generally do not have Roles, only CombatTypes.

### Roles
Roles contain the logic of how an encounter behaves outside of combat. Generally, Roles can vary for the same prefab - i.e. a fighter prefab could be used with the Role Patrol, PatrolArea and Escort depending on the encounter. The currently available Roles are:
| Role | Status | Description |
| ---- | ---- | ---- |
| Cargoship | Working | |
| Escort | Working | |
| Patrol | Working | |
| PatrolArea | Working | |
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
CombatTypes contain the logic of how an encounter behaves during combat. Generally, the CombatType depends on the prefab - i.e. if you have a prefab of a SPRT freighter you would usually use the Freighter CombatType for all encounters that use this prefab. The currently available CombatTypes are:
| Role | Status | Description |
| ---- | ---- | ---- |
| Fighter | Working |  |
| Freighter | Working |  |
| Gunship | Working |  |
| Dropship | WIP |  |
| Rover | WIP |  |
| Static | WIP |  |

A CombatType is assigned to an encounter by referencing its triggergroup in the behavior: `[TriggerGroups:MSB_Freighter_TriggerGroup]` (example for Freighter)

### Common TriggerGroups

### Systems


## How to use
Usage of MSB requires knowledge of the creation of MES config files. While it makes the creation of encounter mods much easier, it still requires users to know their way around setting up their own side and being able to understand the way MSB works enough to use it.
