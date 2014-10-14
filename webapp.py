from flask import Flask, render_template, request
import HB_app_copy

app = Flask(__name__)

@app.route("/student")
def get_student():
    HB_app_copy.connect_to_db()
    student_github = request.args.get("github")
    print "student_github = ", student_github
    row = HB_app_copy.get_student_by_github(student_github)
    print "row = ", row
    html = render_template("students_info.html", first_name=row[0],
                                                last_name=row[1],
                                                github=row[2])
    # return HB_app_copy.get_student_by_github(student_github)
    return html

@app.route("/")
def get_github():
    return render_template("get_github.html")


if __name__ == "__main__":
    app.run(debug = True)