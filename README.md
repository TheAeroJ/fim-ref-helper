# FIM Referee Helper

## Roadmap
- [ ] SQLAlchemy wrapper to handle database management on this application
- [ ] User registration + profile service
- [ ] User event history
- [ ] Michigan event history
- [ ] Historical event referee rosters
- [ ] Opt-in referee directory (secured)
- [ ] Event request/election system
- [ ] Event assignment swaps
- [ ] Calendar
- [ ] Training Links

## CS50 Final Project walkthrough + report

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

#### Authentication, Secrets, and APIs, oh my!
One of the other slightly more time-consuming pieces of this project has been learning how to actually integrate with a web API. And, like my experience with `Database` and `SQLAlchemy`, I had to do this twice, as well. I started by spending time reading through and learning the basics of the [Requests Python library](https://pypi.org/project/requests/) hosted on PyPi. While I had _some_ experience using `cURL` in the past from a Linux Command Line environment for one-off purposes, I hadn't really tried to integrate this with Python. Through some amount of trial and error, I did some testing and built some minor prototypes using `Requests` to ensure I knew what I was doing. Once I felt like I had a solid grasp on the _requests_ library, I set about to look into the APIs themselves.

I began by requesting access to the [FIRST Robotics Competition Events API](https://frc-api-docs.firstinspires.org). I spent the time to read through the API documentation, mock up my code, and test my API requests. When I was satisfied I had wrapped my head around the FIRST Events API, I went to work implementing my code to begin querying events and setting up the machinery to automate updates, caching, and data retention. Before long, I realized I had a problem: the FIRST events API was giving me 500 responses for any season prior to 2020! This would have constituted a significant impediment to my ability to complete the project as designed and planned. I needed to be able to query events going back all the way to the first ever FIRST Robotics Competition event in Michigan, which took place in 2001. Once again (this is a theme in this project, and perhaps is teaching me an _important_ lesson about development in general!), this meant I needed to start over. I decided to eschew the official FIRST API and, instead, rely upon the The Blue Alliance API. The Blue Alliance (TBA) is a website which exists to be a community tool for FIRST Robotics Competition participants to keep records and statistics about FIRST Robotics Competition game results over the years. Generously, they expose _much_ of the data they maintain in their own database(s) to the public. I then set to work understanding and implementing logic I wanted to use the FIRST API to accomplish but, instead, using the TBA APIs. I found that a clause I had read as part of the FIRST Developers' agreement nagged at me - that is, the section that covered prohibited usage of the FIRST Events API. Specifically, I was worried about the fact that any sort of publicly-hosted or shared project was absolutely *prohibited* from containing API keys or other credentials. This made sense! But I had, in fact, done exactly that. My repository contained, hard-coded in my files, my API access credentials for both the FIRST website _and_ for The Blue Alliance. I realized quickly that this meant I had two problems. For one thing, I couldn't *possibly* turn in a project that didn't work (which it wouldn't have, without including some keys to access the FIRST and/or TBA APIs). For another thing, even if I *removed* the hard-coded credentials from my repository somehow, those credentials would still exist _in my git history_. To resolve this, I had to solve two problems:
- How do I authenticate against an API in my application without exposing my secrets and credentials to the world, if I wanted my project's source code to be open and public?
- Once I've figured out how to do the first part, how do I now *fix* the fact that I have credentials in my Git history, freely available in my project's commit history?

For the second point, a simple solution would have been merely to solve (1) and then create a brand new repository with the credentials obfuscated, but that didn't satisfy me. I wanted to do this _properly_. That meant that I couldn't simply blow away all of my commit history, or _merely_ change my credentials. I felt like the former did me a disservice by erasing my project and work history, which could serve a valuable clue in the future when I was expanding upon this project by helping me recall certain pitfalls or successes in development, *and* would erase the evidence of the _process_ I had to follow in order to make as much progress as I did. The latter, on the other hand, felt like it was still risky. While I don't think anyone is particularly intenting to expend the effort to reverse-engineer FIRST or The Blue Alliance's credential-generaton system, it didn't sit right to me that any sort of credentials (deactivated or no!) would be there in the open for anyone to see.

My solution was twofold, here. In order to accomplish the first goal of authentication in a codebase without exposing hard-coded credentials, I turned to [python-dotenv](https://pypi.org/project/python-dotenv/). This allowed me to familiarize myself with the ways in which Environment Variables can be used by Python (a concept with which I was previously acquainted, but about which I knew almost nothing!), and to leverage them (via a `.env` file in my local repo and, importantly, included in my `.gitignore`) to not only store sensitive data in a place accessible to the application on my local machine but _not_ available or even visible via GitHub, but also allowed me to specify a space for my application's database to reside which was, additionally, outside of the repository. Once my authentication problem was solved and my application had access to resources that would and should _not_ live in the main code repository, I then needed to eliminate my sloppy work from prior commits in my repository, but _without_ compromising my repo's history. To do this, I spent some time reviewing the documentation for `git-filter-repo`, which once again felt like some cruel punishment for mistake with the rather esoteric api reference. Fortunately, I discovered the [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) project which aimed to provide someone like me exactly what I needed.

#### Conclusion and Repo walkthrough
After facing the reality of having to build and rebuild my repo and project several times after encountering some rather significant (at least, for someone of my knowledge and skill level!) setbacks, I have...far less to show than I was hoping. What I have, in fact, is basically the beginnings of a library which builds the database I need for my application, and implements several functions necessary for storing, managing, and retrieving data from my SQLite database, plus _numerous_ valuable lessons about development, reliance upon third-party projects, Python and development best-practices, and, perhaps most importantly, a healthy appreciation for the importance of doing strong design work up-front before selecting an approach and setting-off to build a solution.

##### Files in the Repo:
- `.gitignore` - Set up upon creation of the new Git repository for my project. I am using it to exclude my `__pycache__` directory, as well as my `.env` file which stores some paths and credentials necessary to use the application on my local machine
- `.python-version`, a file set up by `uv` in the course of establishing Python version and package management with UV
- `README.md`: the file you're currently reading!
- `app.py`: An empty file which (should) have been where the bulk of my Flask app logic was stored
- `db_operate.py`: A script (usable as a library!) to wrap SQLAlchemy capabilities into a small library of functions of particular use to my specific project in order to build and interact with my app's database
- `db-setup-notebook.ipynb`: After getting discouraged by the API debacle, I decided to spend time setting up a Jupyter notebook to (relatively) quickly gather the necessary data to seed my database directly from the FIRST (then, later, The Blue Alliance) database. I also used this as a ground for prototyping small snippets of code for the rest of my project. Were this an actual production application, I would absolutely not keep this in my repo; as it is, however, I felt it useful to capture exactly what had gone into my project.
- `first-event-getter.py`: The remnants of my initial (doomed) effort to get the event data I needed from the FIRST events API
- `pyproject.toml`: A small markup file created by UV to document my project. Still WIP
- `tba_event_getter.py`: The file I began to work on which did the necessary work of interacting with The Blue Alliance's API, and functions as a module to be used in the application. In the short term the work that would have gone here is living in my Jupyter notebook.
- `tba_handler.py`: The script/module I began to write to replace the (myopic) vision of the `tba_event_getter.py` and instead build a more robust and future-proof module for interacting with TBA
- `uv.lock`: A file generated by UV to capture dependencies and project versioning