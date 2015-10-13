import sys
sys.path.insert(0, '/opt/scoring')

from scoreboard.app import register_modules, app as application
register_modules()