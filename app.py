from flask import Flask
from flask_cors import CORS
import services.init_database
from controllers.PersonController import getAllPeople, getPerson, addPerson, updatePerson, deletePerson

# ------------------------------------------------ Config ---------------------------------------------
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# ------------------------------------------------ Main Route ---------------------------------------------
@app.route("/")
def welcome():
    return "Welcome to Backend"

# ------------------------------------------------ People Routes ---------------------------------------------
app.route('/people', methods=['GET'])(getAllPeople)
app.route('/people/<person_id>', methods=['GET'])(getPerson)
app.route('/people', methods=['POST'])(addPerson)
app.route('/people/<person_id>', methods=['PUT'])(updatePerson)
app.route('/people/<person_id>', methods=['DELETE'])(deletePerson)


# ------------------------------------------------ End routes ---------------------------------------------
if __name__ == '__main__':
    app.run(debug=True) 