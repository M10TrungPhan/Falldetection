from webfall import app
from webfall import db
from os import path
#Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    if not path.exists("webfall/webfall.db"):
        db.create_all(app=app)
    app.run(debug=True)
    