# Rulebook App

## Database Schema

### Rule
isEvergreen: Bool
rulePrefix: varchar (Str)
ruleNum: int
ruleHeadline: str
ruleText: str
hasBlueBox: bool
blueBoxText: str
violationStr: str
violationEnum: enum??
verbWar: bool
minFoul: bool
majFoul: bool
majFoulCond: list? enum?
yellowCard: bool
yellowCardCond: list? enum?
redCard: bool
redCardCond: list? enum?
roboDisable: bool
roboDisableCond: list? enum?
additionalNotes: str
tags/keywords: list?