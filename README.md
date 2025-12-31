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

#### Design Choices + Considerations
##### Scope was _significantly_ reduced because early ambitions were enormous

Initially my primary focus was going to be dealing with the FIRST game manual. This presented several issues: for one, I struggled with definition of the data model for storing what is (at least today) published on the FIRST website as a PDF, and then being able to slice aned present it in a cohesive manner in a way that was extensible. I wanted to be able to:

- Represent the _entire_ game manual as, effectively, a mirror of the original PDF files directly from FIRST
- Create an interactive glossary system that would allow the user to get tooltip "peeks" at critical game terms and not only show the text found in the Glossary but also provide links to the precise text in the game manual where the term was originally defined (since precision in wording is *VERY* important to the FIRST Robotics Competition)
- Create a table of rules which would achieve a few key goals:
    - Condensing the rules into a shorthand which was meaningful and easily visually-scannable, particularly on a phone or a tablet
    - Symbolically indicate penalties and represent any additional conditions, exceptions, or stipulations graphically (again, for simplicity and speed of visual scanning)
    - Allow for filtration by tags or search terms (e.g. a search bar that let the user see all rules that dealt with Game Pieces, or Damage, or specific regions of the FIELD as defined in the manual)
    - Allow for some user preferences to highlight specific rules (via some favorites system, perhaps)
    - Present, upon interaction, popup "cards" which would show the complete detail of the rule as presented in the manual exactly
- Build system for intelligently querying event information to populate a team list and table for rules which have a warning provision before cards are asessed
- Build a system for highlighting changes in the manual line-by-line when Team Updates were released
- Ensure the data model was modular enough to _also_ be used to generate markdown files which could then be assembled into a document to generate the complete manual documents, so that I could pitch the system to FIRST.


I quickly realized that the above was large enough to be a project all its own, and between analysis paralysis on the data model plus the many additional questions and consideraions inherent with all of these features demonstrated to me that I needed to start smaller. As a result, I decided to pivot.

After dismissing the initial concept (although keeping it as a potential future exercise!) I decided to re-focus on one basic functionality that is useful for FIRST in Michigan head referees, a group of which I am a member. Given that it is currently the "off-season," prior to the next (2026) FIRST Robotics Competition season, I decided that a scheduling assistant tool would be most helpful. The current solution used by our crew is a simple spreadsheet, which contains a list of events for the upcoming season as well as the past events and their Head Referees. Where this becomes a problem is that the spreadsheet is fully manually maintained and updated. This presents some challenges:
- Events are _generally_ consistent from year-to-year; however, there are times during which events which share a code or name change venue, or maintain a consistent venue but change name and/or code. There are also cases of events being paused and then being "resurrected" later. This is clunky to manage manually in a spreadsheet
- Data reliability is poor because it is manually copied from year-to-year
- Maintenance of the tracker is extremely tedious given that it is fully manual
- When schedules change (which, at times, they do!), the custodian of the sheet must manually be made aware of the changes and then make the associated updates.
- Maintaining good etiquette is completely managed by the honor system; anyone and everyone in the group is able to modify the sheet in whatever manner they choose. While this is...OK, it's not scalable or repeatable. 

My vision is to create a tool which takes all of the manual steps out of this process and, importantly, maintains a platform upon which I can build additional features and potentially even evolve into more advanced projects in the future.

I toyed with the idea of building a React application, with the goal of eventually creating native Android and iOS applications out of my web app. I began down that path; however, quickly realized that the investment of time into learning NodeJS and React was overkill compared with my need to actually create something upon which I could build. I then investigated using Django as a slightly more feature-rich and expandable version of what we learned with Flask. Once I began working on implementing my backend data store/database management system, however, I realized that I would not have been able to "roll my own" implementation for data management _and_ learn a new framework (in Django). As a result, I decided to stick with a basic Flask app.

##### A _lot_ of time was lost to learning and handling the SQLAlchemy connections to manage the backend of my database

While I understood that the CS50 libraries significantly simplified interaction with a SQLite database, I _significantly_ underestimated the extent to which that was true. I began reading through the documentation for SQLAlchemy, and quickly started to feel a bit overwhelmed by the amount of detail and the number of Python idioms were, apparently, required to grok the documentation there. I set out in search of something _similar_ to the CS50 library, but which was more of an industry standard. I quickly stumbled across [Dataset](https://dataset.readthedocs.io/en/latest/index.html#), which seemed perfect! I began to write my database manipulation and creation logic using Dataset as a base. Before long, though, in testing my code I discovered some interesting errors, and while investigating discovered a section in the Dataset documentation I had missed (read: not gotten all the way to reading)...

> Some of the specific aspects of SQL that are not exposed in dataset, and are considered out of scope for the project, include:
> - Foreign key relationships between tables, and expressing one-to-many and many-to-many relationships in idiomatic Python.

...Oops. My database schema, even with a significant reduction in project scope, *depended* on the ability to establish a foreign key relationship! After a respectable amount of time setting up my database schema using the Dataset framework, I realized I had to start over from scratch and would, after all, need to invest the time to learn how SQLAlchemy worked under the covers and could be utilized for a project like mine.


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