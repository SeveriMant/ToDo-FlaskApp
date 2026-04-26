
from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__)

tasks = []

@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        tasks.append({"task": task, "done": False})
    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect("/")


@app.route("/complete/<int:task_id>")
def complete(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
    return redirect("/")

@app.route("/save", methods=["POST"])
def save():
    filename = request.form.get("filename", "tasks.txt")
    if not filename.endswith(".txt"):
        filename += ".txt"

    task_str =""
    for task in tasks:
        task_str += f"{task["task"]} {("✅" if task["done"] else "")}\n"

    response = make_response(task_str)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/plain"
    return response

if __name__ == "__main__":
    app.run(debug=True)