# FIM Referee Helper
#### Video Demo:  <URL HERE>
#### Description:
This project consists of a web application designed to assist FIRST in Michigan FIRST Robotics Competition Head Referees with their responsibilities. The initial version (my "MVP") is intended to do the following:
- Show a schedule of events for the upcoming season (at the time of this writing, the 2026 FIRST Robotics Competition district season)
- Show a history of _all_ prior FIRST Robotics Competition events in the state of Michigan, which detail:
    - Dates of the events
    - Location of the events
    - Head Referee for the events
- Provide a user registration and profile service aimed at FIRST in Michigan Head Referees including:
    - User event history
- Seed a database of the current (as of December 2025) FIRST in Michigan Head Referees
- Allow existing referees to "claim" their accounts, set up a username and password, and then act on their own behalf for future seasons
- Allow site admin(s) to manually trigger an update to the site to pull the next year's list of events and add them to the events database
- Allow head referees to provide elections for their event preferences, factoring in the following:
    - "Incumbency" (i.e. the head referee from the prior year's iteration of an event)
    - A multi-round process which ensures that all (Active) users have an opportunity to provide their elections before second (or third, etc) preferences are elected
- An assignment system to allow super-users (i.e. FIM Lead Head Referees) to confirm assignments, make changes, etc
- A resources page which hosts shortcuts to relevant documentation, such as:
    - FIRST game manuals
    - FIRST referee and Head Referee training materials
    - FIRST Head Referee community materials and distributed materials (e.g. "cheat sheets")

_Stretch_ goals include the following:
- Interactive trackers (accessible by the assigned head referee for an event) to digitally replicate the "warning" system and allow annotations from head referees
- A Rulebook section which allows for quick review and access to game critical materials in a format that is friendly for any device size or profile


## Roadmap
- [ ] User registration + profile service
- [ ] User event history
- [ ] Michigan event history
- [ ] Historical event referee rosters
- [ ] Opt-in referee directory (secured)
- [ ] Event request/election system
- [ ] Event assignment swaps
- [ ] Calendar
- [ ] Training Links