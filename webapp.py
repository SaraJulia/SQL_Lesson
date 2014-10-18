from flask import Flask, render_template, request
import HB_app_copy

app = Flask(__name__)

@app.route("/student")
def get_student():
    HB_app_copy.connect_to_db()
    student_last_name = request.args.get("last_name")
    # print "student_last_name = ", student_last_name
    projects = HB_app_copy.show_all_grades(student_last_name)

    html = render_template("students_info.html", all_projects = projects,
                                                last_name = student_last_name)
    return html

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/project")
def get_projects():
    HB_app_copy.connect_to_db() 
    project_id=request.args.get("id")
    project_info = HB_app_copy.show_projects(project_id)
    ###TESTING CODE####
    # print "total project list:", project_info
    for thing in project_info:
        print "current project", thing

    html = render_template("project.html", project_title = project_info[0],
                                            description = project_info[1],
                                            grades_list = project_info[2])
    return html

@app.route("/add_student")
def add_student():
    HB_app_copy.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    ### TESTING CODE ###
    # print first_name, last_name, github
    success = HB_app_copy.make_new_student(first_name, last_name, github)
    html = render_template("add_student.html", message = success,
                                                first_name = first_name,
                                                last_name = last_name) 
    return html

@app.route("/add_project")
def add_project():
    HB_app_copy.connect_to_db()
    project_name = request.args.get("project_name")
    description = request.args.get("description")
    max_grade = request.args.get("max_grade")
    ### TESTING CODE ###
    # print first_name, last_name, github
    success = HB_app_copy.add_a_project(project_name, description, max_grade)
    html = render_template("add_project.html", message = success,
                                                project_name = project_name) 
    return html

if __name__ == "__main__":
    app.run(debug = True)