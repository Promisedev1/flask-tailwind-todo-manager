from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# ----------------------------------------------------
# 1. FLASK AND SQLALCHEMY SETUP
# ----------------------------------------------------

app = Flask(__name__)

DB_URI = "sqlite:///todos.db"

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# ----------------------------------------------------
# 2. DATABASE MODEL DEFINITION
# ----------------------------------------------------


class Task(db.Model):
    """
    SQLAlchemy Model for the Task entity.
    Maps to a table named 'task' in the database.
    """

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        """Converts the Task object to a dictionary for JSON response."""
        return {"id": self.id, "text": self.text, "completed": self.completed}


# ----------------------------------------------------
# 3. DATA PERSISTENCE AND LOGIC IMPLEMENTATION (SQLAlchemy)
# ----------------------------------------------------


def create_task(text: str) -> dict:
    """
    Creates a new task record in the database.
    """
    new_task = Task(text=text)
    db.session.add(new_task)
    db.session.commit()
    return new_task.to_dict()


def get_all_tasks() -> list:
    """
    Fetches all tasks from the database, ordered by ID.
    """

    # Query all tasks and convert them to a list of dictionaries
    tasks = Task.query.order_by(Task.id).all()
    return [task.to_dict() for task in tasks]


def update_task_status(task_id: int, completed_status: bool) -> dict | None:
    """
    Updates the 'completed' status of a specific task by ID.
    """
    task = db.session.get(Task, task_id)
    if task:
        task.completed = completed_status
        db.session.commit()
        return task.to_dict()
    return None


def delete_task(task_id: int) -> bool:
    """
    Deletes a task by ID.
    Returns True if the task was found and deleted, False otherwise.
    """
    task = db.session.get(Task, task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return True
    return False


# ----------------------------------------------------
# 4. FLASK ROUTES (API ENDPOINTS)
# ----------------------------------------------------


# Route 1: Serve Frontend Index
@app.route("/")
def serve_frontend():
    """Serves the main HTML file from the 'static' folder."""
    try:
        return app.send_static_file("index.html")
    except Exception:
        return "Frontend file not found. Ensure index.html is in the 'static' folder."


# Route 2: Handle all Task CRUD Operations (GET and POST)
@app.route("/api/tasks", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        tasks = get_all_tasks()
        return jsonify(tasks)

    elif request.method == "POST":
        if not request.is_json:
            return jsonify(error="Unsupported media type"), 415
        data = request.json.get("text")
        if not data:
            return jsonify(error="Invalid request data: 'text' field is required"), 400
        try:
            new_task = create_task(data)
            return jsonify(new_task), 201
        except Exception as e:
            return jsonify(error=e), 500


# Route 3: Handle Single Task Operations (PATCH and DELETE)
@app.route("/api/tasks/<int:id>", methods=["PATCH", "DELETE"])
def handle_single_task(id: int):

    if request.method == "PATCH":
        # UPDATE: Toggle completion status
        data = request.get_json()
        completed_status = data.get("completed")

        updated_task = update_task_status(id, completed_status)

        if updated_task:
            return jsonify(updated_task)
        else:
            return jsonify({"error": "Task not found"}), 404

    elif request.method == "DELETE":
        # DELETE: Remove the task
        success = delete_task(id)

        if success:
            return ("", 204)  # 204 No Content
        else:
            return jsonify({"error": "Task not found"}), 404


# ----------------------------------------------------
# 5. INITIALIZATION AND RUNNER
# ----------------------------------------------------


def init_db():
    """Initializes the database and creates tables if they don't exist."""
    with app.app_context():
        # This function creates the database file and all tables defined in the models
        db.create_all()


if __name__ == "__main__":
    # Initialize the database before running the app server
    init_db()

    # Run the application
    app.run(debug=True)
