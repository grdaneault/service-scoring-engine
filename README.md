# service-scoring-engine
A blue team service scoring engine written in python

# "Quick" Start
1. Configure your competition by creating the necessary classes in configuration/competition_name
  - Each machine gets a file:
    - `get_services` returns a list of the services this machine should be scoring, based on the team.  (usually used to configure ips/hostnames/etc)
    - `get_flags` returns a list of flags that can be discovered on that machine
    - `get_injects` returns a list of injects that can be solved, based on the team.  (used to differentiate red vs blue injects)
  - users.py creates all the users (red, white, and blue teams)
  
2. Update `configuration/web_configuration.py` to change database credentials
3. Update the imports in `configuration/create_competition.py` to include your modules
4. Run `python3 configuration/create_competition.py` to intialize all the database tables and content for the competition
5. Run `python3 scoreboard/run.py` to start the web service.  Make sure the root directory is in your python path.
6. Run `python3 engine.py` to start scoring
