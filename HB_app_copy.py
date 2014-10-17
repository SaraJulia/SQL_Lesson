import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row
    # print """
    # Student: %s %s
    # Github account: %s""" %(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def add_a_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project title: %s" % (title)

def query_for_projects(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\n
    Project ID: %s
    Project Title: %s
    Description: %s
    Max Grade: %s """ % (row[0], row[1], row[2])

def query_for_student_grade(last_name, project_title):
    query = """SELECT * FROM GradesView WHERE last_name = ? AND project_title = ?"""
    DB.execute(query, (last_name, project_title))
    row = DB.fetchone()
    print """
    Name: %s %s
    Project: %s
    Grade: %s """ % (row[0],row[1],row[2], row[3])

def assign_grade(github, project_title, grade):
    query = """INSERT INTO Grades (student_github, project_title, grade) VALUES (?,?,?)"""
    DB.execute(query, (github, project_title, grade))
    CONN.commit()
    print "Successfully assigned %s grade to %s student for %s project." %(grade, github, project_title)

def show_all_grades(last_name):
    query = """SELECT ReportCardView.first_name, ReportCardView.last_name, Projects.id, Projects.title, ReportCardView.grade  
               FROM Projects LEFT JOIN ReportCardView ON Projects.title=ReportCardView.title
               WHERE ReportCardView.last_name = ?;"""
    DB.execute(query, (last_name.strip(),))
    rows = DB.fetchall()
    proj_list = []
    for row in rows:
        d = {}
        d['first_name'] = row[0]
        d['last_name'] = row[1]
        d['project_id'] = row[2]
        d['project_title'] = row[3]
        d['grade'] = row[4]
        proj_list.append(d)

    return proj_list
    # for row in rows:
    #     print """
    #     Name: %s %s
    #     Project: %s
    #     Grade: %s """ % (row[0],row[1],row[2], row[3])

def show_projects(project_title):
    query = """SELECT * FROM GradesView WHERE project_title = ?"""
    DB.execute(query, project_title)
    rows = DB.fetchall()
    return rows
    # for row in rows:
    #     print """
    #     Name: %s %s
    #     Project: %s
    #     Grade: %s """ % (row[0],row[1],row[2], row[3])

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(',')
        command = tokens[0]
        args = tokens[1:]


        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "new_project":
            add_a_project(*args)
        elif command == "query_project":
            query_for_projects(*args)
        elif command == "get_grade":
            query_for_student_grade(*args)
        elif command == "assign_grade":
            assign_grade(*args)
        elif command == "show_all_grades":
            show_all_grades(*args)
        else:
            print "Please enter a valid command"
    CONN.close()

if __name__ == "__main__":
    main()
