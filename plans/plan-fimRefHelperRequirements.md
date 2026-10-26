## Plan: FIM Ref Helper, gaps and MVP requirements

You chose a production tool for FiM head referees (HRs) with about 50 or fewer users. Referee history is entered manually by an admin. Login is email and password against admin-seeded profiles that referees claim. The election system is in the MVP, and the rulebook is parked. The gaps below are based on your README and the current code.

### 1. Holes in the plan

**Product and scope**
1. **The election system is the core of the product, but it has no rules.** The README gives two hints (incumbency, multi-round) and nothing else. Without concrete rules it can't be built or tested. See the open questions in section 3.
2. **The README has three different scopes.** There is a spreadsheet replacement (history and schedule), a profile and directory service, and an election and assignment engine. Only the first is close to feasible, so the MVP needs an order of delivery.
3. **The roadmap and the "MVP" list disagree.** The roadmap has an opt-in referee directory, swaps and a calendar. The MVP list has none of them but adds a resources page. Pick one list.
4. **The dates are inconsistent.** The README says "2027 season" and "December 2025", and the notebook loops to 2026. The current date is October 2026, so the next season to schedule is probably 2027. State that explicitly and make the season a parameter.
5. **There are no success criteria.** You haven't said what replaces the spreadsheet, who uses it first, or what "done" means for one season.
6. **Event identity over time is the hard problem, and nothing is modeled for it.** You describe events that move venues, rename, change codes, pause and come back. TBA keys like `2024miken` are per-year, so you need an abstract "event series" that links yearly instances. Incumbency depends on this.
7. **Incumbent, backup and multiple HRs per event.** The README implies one HR per event. Do events have a Head Referee only, or also Assistant HRs and Volunteer Coordinators? The `volunteer_assignments.role` column suggests several roles.
8. **Data ownership and privacy are unaddressed.** Phone numbers and a referee directory are personal data. You'll need an opt-in flag, visibility rules and a way to delete an account.
9. **There's no plan for the transition.** Who enters the historical HR data, in what format, and who validates it? Manual entry of 25 years of events is a lot of work unless you import from the spreadsheet. That would be a one-time CSV import, even though you chose manual entry as the source.

**Data and architecture**
10. **The schema is missing most of what the features need.**
    - There's no email, password hash, status (Active or Inactive) or claim state on users.
    - There are no tables for event series, seasons, election rounds, preferences, assignments with a state, or an audit log.
    - `phone` is stored as Numeric, which strips leading zeros and `+`.
    - Dates are stored as Numeric but should be Date or ISO text.
    - `ref_role` and `site_role` are free text with no constraint.
    - `people` and `users` are split, which is good for unclaimed profiles. Make that explicit: a person exists before a user does.
11. **The `state_prov == 'MI'` filter is wrong.** It includes MI events that aren't FiM events, and excludes pre-district Michigan events whose `state_prov` is formatted differently. Use the TBA district key `fim` for district years, and an explicit rule for the 2001–2008 era.
12. **There's no refresh or caching strategy for TBA.** Decide whether to cache, whether to use ETags (`If-None-Match`) and how an admin triggers a refresh. Also decide what happens when TBA changes an event you've already assigned someone to.
13. **There is no migration plan.** `db_operate.py` mentions Alembic as maybe overkill. For a deployed app with real data it isn't.
14. **SQLite on a PaaS is risky.** Many platforms have ephemeral disks. Either use a persistent volume with backups or move to Postgres. Decide before deploying.
15. **The architecture is undecided.** The README's Design, Frontend and Backend sections are empty. `app.py` is empty, and the Flask structure (blueprints, templates, auth library, CSRF) isn't specified.

**Security and operations**
16. **Authentication needs a design.** It needs password hashing, claim flow, password reset (which needs email sending), session handling, CSRF protection, rate limiting and an admin role.
17. **The claim flow is an identity-theft risk.** Anyone who knows a referee's name could claim their profile. The claim needs a verification mechanism, such as an invite token sent by an admin or an email match.
18. **Secrets handling needs a documented procedure.** Document the `.env` variables and ship a `.env.example`. Your history was rewritten with BFG, but the old TBA and FIRST keys should be rotated if they were ever pushed.
19. **No tests, logging, backups or deployment plan.** The README admits the code is mostly stubs.

### 2. Bugs in the current code

These are worth fixing before building on it:
- `db_operate.py`:
  - `db_create(kwargs)` and `db_modify(kwargs)` pass a dict where `**kwargs` is expected, so they would raise a TypeError.
  - `"operation" not in ["insert", ...]` checks the literal string, not `kwargs["operation"]`, so it always fails.
  - `--args` with `type=dict` doesn't work on the command line.
  - `echo=True` is on, and the module prints at import time.
  - SQLite foreign keys aren't enforced without `PRAGMA foreign_keys=ON`.
  - Table definitions live inside `engine.begin()`, which isn't needed for `create_all`.
- `tba_handler.py`:
  - `__name__ == "__get_tba_response__"` is never true, so the CLI never runs.
  - `load_dotenv()` runs on every call, and there's no timeout on `requests.get`.
- `tba_event_getter.py`:
  - `baseApiURL` and `requestHeaders` are undefined.
  - `json.loads(response.json())` parses twice.
  - The year range 1992–2010 contradicts the README's 2001.
- `pyproject.toml` has empty `dependencies`, and the README references `uv.lock`, which I didn't see in the workspace listing.
- The notebook still has a Dataset import, which the README says you abandoned.

### 3. Open questions that block the election requirements

1. How do preferences work? Ranked list of all events, top N, or a pick per round?
2. What is the round mechanic? Does everyone submit round 1 before anyone sees round 2? What are the deadlines, and what happens to non-responders?
3. How is incumbency applied? Is it an automatic award, a priority bump, or a right of first refusal? Does it expire after some number of years?
4. How are conflicts resolved? Examples are two people picking the same event, tenure as a tie-break, or a random draw.
5. Are there per-referee limits, such as a maximum number of events per season, no back-to-back weekends or travel distance?
6. Is the lead HR's confirmation the final word, and can they override the system?
7. What is "Active" status, and who sets it?
8. Can assigned events be swapped or dropped, and by whom?

### 4. Draft requirements

**Actors:** Visitor (not logged in), Head Referee, Lead HR (super-user) and Site Admin.

**Phase 0: Foundation**
1. Python project with Flask, SQLAlchemy, requests and python-dotenv declared in `pyproject.toml`.
2. App-factory layout, config from environment, `.env.example`, structured logging, pytest set up.
3. SQLAlchemy ORM models and Alembic migrations, replacing the hand-rolled `db_operate` wrapper.
4. A decision between SQLite with a persistent volume and Postgres.

**Phase 1: Event data**
1. Import FiM events from TBA for 2001 onward. Use the `fim` district for district years and an explicit rule for earlier years. Store events by TBA key.
2. An event-series model links yearly events (admin can merge, split and relink). Events can be marked paused or resurrected.
3. An admin-triggered refresh that is idempotent and records what changed.
4. Event schedule page for a selected season (default is the upcoming one), with dates, city, venue and assigned HR.
5. Event history page by series, showing every year's dates, location and HR.

**Phase 2: People and accounts**
1. Admin creates or imports person profiles (name, rookie season, role, status, optional email).
2. Admin issues a claim invite. The referee sets a username and password through a one-time expiring token.
3. Login and logout, password reset, passwords hashed (argon2 or bcrypt), CSRF protection and rate limiting.
4. Roles: HR, Lead HR, Admin.
5. Profile page with the user's event history, and edit rights for their own contact details.
6. Admin enters and edits historical HR assignments, with an optional CSV import.

**Phase 3: Elections and assignments** (needs the section 3 answers first)
1. Admin opens a season and election with a set of events and eligible (Active) users.
2. Users submit preferences per round and can edit until the round closes.
3. A round only closes when all eligible users have submitted, or when an admin forces it.
4. The engine proposes assignments using the incumbency and conflict rules. It is deterministic and unit-tested with fixtures.
5. Lead HR can review, change and confirm assignments. All changes are audit-logged.
6. Users are notified of results, by email or in-app.

**Phase 4: Extras**
1. Resources page of curated links.
2. Opt-in directory, calendar and swap requests.

**Non-functional**
- Fewer than 50 users, with decent mobile support.
- Backups, an audit log of privileged actions, and an access rule that only the assigned HR or admins can see private event data.
- TBA key secrecy, with rate-limit and error handling around the API.
- Automated tests for the election engine and the auth flows.

### 5. Suggested next steps

1. Answer the section 3 questions, ideally in a short written rule set added to the README.
2. Decide on the database, hosting and email provider (required for invites and resets).
3. Draft a revised README with this structure, an ER diagram of the target schema, and a prioritized backlog.
