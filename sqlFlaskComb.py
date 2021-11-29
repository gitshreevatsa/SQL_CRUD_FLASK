from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,MetaData,Column,Integer,String,Table,Boolean

engine = create_engine('sqlite:///newProject.db', echo = True)
meta= MetaData()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
db = SQLAlchemy(app)


data = Table(
   'params', meta, 
   Column('USN', String, primary_key = True), 
   Column('student_name', String),
   Column('Gender', String),
   Column('Entry_type', String),
   Column('YOA', Integer),
   Column('migrated', Boolean),
   Column('Details_of_migration', String),
   Column('admission_in_separate_division',Boolean),
   Column('adDetails', String),
   Column('YOP', Integer),
   Column('degree_type', String),
   Column('pu_marks', Integer),
   Column('entrance_marks', Integer),
)

meta.create_all(engine)


def create(body):
    conn = engine.connect()
    sUSN = str(body['USN'])
    sName = str(body['student_name'])
    sGender = str(body['Gender'])
    sEntry_type = str(body['Entry_type'])
    sYearOfAdmission = int(body['YOA'])
    sMigrated = int(body['migrated'])
    sDetails = str(body['Details_of_migration'])
    sadmissionInSepDiv = int(body['admission_in_separate_division'])
    admissionDetails = str(body['adDetails'])
    sYop = int(body['YOP'])
    sDegreeType = str(body['degree_type'])
    sPuMarks = int(body['pu_marks'])
    sEntranceExams = str(body['entrance_marks'])
    result = conn.execute(data.insert(),[
            {'USN' : sUSN, 'student_name' : sName, 'Gender' : sGender, 'Entry_type': sEntry_type,'YOA': sYearOfAdmission, 'migrated': sMigrated,
             'Details_of_migration': sDetails, 'admission_in_separate_division': sadmissionInSepDiv,'adDetails': admissionDetails ,'YOP': sYop, 'degree_type': sDegreeType,
             'pu_marks': sPuMarks, 'entrance_marks': sEntranceExams}
        ])
    result_dict = {'USN' : sUSN, 'student_name' : sName, 'Gender' : sGender, 'Entry_type': sEntry_type,'YOA': sYearOfAdmission, 'migrated': sMigrated,
             'Details_of_migration': sDetails, 'admission_in_separate_division': sadmissionInSepDiv,'adDetails': admissionDetails ,'YOP': sYop, 'degree_type': sDegreeType,
             'pu_marks': sPuMarks, 'entrance_marks': sEntranceExams}
    return result_dict

def read():
    conn = engine.connect()
    dataview = data.select()
    result = conn.execute(dataview)
    for row in result:
        row_dict = dict(row)
    return row_dict

def update(body):
    conn = engine.connect()
    dict_input = dict(body)
    match = dict_input['USN']
    for key, value in dict_input.items():
        updated = data.update().where(data.c.USN==match).values({key:value})
        result = conn.execute(updated)
    return "Appended Successfully"

def delete(body):
    conn = engine.connect()
    option = body['USN']
    deleted = data.delete().where(data.c.USN == option)
    result = conn.execute(deleted)
    return "Deleted"


@app.route('/newEntries', methods = ['POST'])
def assignment():
    body = request.get_json()
    output = create(body)
    return output


@app.route('/readEntries', methods = ['POST'])
def readingAssignment():
    output = read()
    return output


@app.route('/updateEntries', methods = ['POST'])
def updatingAssignment():
    body = request.get_json()
    output = update(body)
    return output    

@app.route('/deleteEntries', methods = ['POST'])
def deletingAssignment():
    body = request.get_json()
    output = delete(body)
    return output    

if __name__ == '__main__':
    app.run(debug= True, port= 5000)
    