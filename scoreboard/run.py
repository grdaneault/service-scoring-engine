from scoreboard.app import app, register_modules

register_modules()
app.run(host='0.0.0.0', port=8080, debug=True)