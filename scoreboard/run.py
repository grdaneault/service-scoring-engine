from scoreboard.app import app, register_modules
import sys


if __name__ == '__main__':
    register_modules()
    debug = True if len(sys.argv) == 2 and sys.argv[1].lower() == 'debug' else False
    print('Starting in %s mode' % ('debug' if debug else 'production'))
    app.run(host='0.0.0.0', port=8080, debug=debug)