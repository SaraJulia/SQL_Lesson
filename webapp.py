from flask import Flask, render_template, request
import HB_app_copy

app = Flask(__name__)

@app.route("/student")
def get_student():
    HB_app_copy.connect_to_db()
    student_last_name = request.args.get("last_name")
    print "student_last_name = ", student_last_name
    rows = HB_app_copy.show_all_grades(student_last_name)
    print "rows = ", rows
    html = render_template("students_info.html", all_projects = rows,
                                                last_name = student_last_name)
    # return HB_app_copy.get_student_by_github(student_github)
    return html

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/projects")
def get_projects(project_title):
    HB_app_copy.connect_to_db() 
    project_title=request.args.get("project_title")
    return rows



if __name__ == "__main__":
    app.run(debug = True)