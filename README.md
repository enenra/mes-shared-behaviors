# MES Shared Behaviors
MES Shared Behaviors or MSB is a behavior library for Modular Encounters Systems (MES) to allow Space Engineers modders to easily create complex encounters, while not having to set up that logic by themselves.

## How it works
Fundamentally, we differentiate between dynamic and static encounters. Static being ones consisting of static grids, dynamic being ones that move about. Some of the behaviors and systems contained within MSB make sense for static, some for dynamic encounters, but generally they are available to both.

When setting up an encounter with MSB - for example a Patrol - there are generally two important things that need to be defined, and upon whose distinction the entirety of MSB is built: Roles and CombatTypes. An dynamic encounter, in this case the Patrol encounter, will have one of each assigned to it and will switch back and forth between their logics depending on whether it is in combat mode, or not. Static encounters generally do not have Roles, only CombatTypes.

### Roles
Roles contain the logic of how an encounter behaves outside of combat. The currently available Roles are:
| Role | Status | Description |
| ---- | ---- | ---- |
| Cargoship | Working | |
| Escort | Working | |
| Patrol | Working | |
| PatrolArea | Working | |
| ConvoyLeader | WIP |  |
| StrikeForceLeader | WIP |  |
| TaskForceLeader | WIP |  |
| BountyHunter | WIP |  |
| Guard | WIP |  |
| Hunter | WIP |  |
| Merchant | WIP |  |
| Raider | WIP |  |
| Salvager | WIP |  |
| Scout | WIP |  |


### CombatTypes
CombatTypes contain the logic of how an encounter behaves during combat. The currently available CombatTypes are:
| Role | Status | Description |
| ---- | ---- | ---- |
| Fighter | Working |  |
| Freighter | Working |  |
| Gunship | Working |  |
| Dropship | WIP |  |
| Rover | WIP |  |
| Static | WIP |  |


### Common TriggerGroups

### Systems


## How to use
Usage of MSB requires knowledge of the creation of MES config files. While it makes the creation of encounter mods much easier, it still requires users to know their way around setting up their own side and being able to understand the way MSB works enough to use it.
