import pandas as pd
from flask import Flask, render_template, request, redirect,url_for
from datetime import datetime
import plotly.express as px
import json
import plotly
data = pd.read_excel("data.xls", engine='xlrd')

data_dict = dict(zip(data['email'], data['password']))
print(data_dict)

dataframe = pd.read_excel('registereduser.xlsx')
print(dataframe)
department_list = dataframe['Department'].tolist()

if 'Department' in department_list:
    department_list.remove('Department')

# print(department_list)

#---------------------------plotting the department---------------------------------------

department_plot = {
    'Department' : department_list
}

dataframe = pd.DataFrame(department_plot)

print('dataframe:',dataframe)

count_of_each_department = dataframe['Department'].value_counts()

department_percentage = (count_of_each_department / len(dataframe)) * 100

fig = px.pie(
    names = count_of_each_department.index,
    values = count_of_each_department.values,
    title = 'Department Distribution'
)

fig.update_layout(
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor = 'rgba(0,0,0,0)',
)

graphJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
#------------------------------------------------------------------------------------------





app = Flask(__name__)

#------------------------------------Admin Landing Page-----------------------------------
@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       username = request.form.get("uname")
       # getting input with name = lname in HTML form
       password = request.form.get("psw")

       if data_dict[username] == password:
           return redirect('/dashboard/' + username)
       else:
           return 'Error! Wrong Password/Username'
    return render_template('userlogin.html',year = datetime.now().year)

#--------------------------------------------------------------------------------------------

#--------------------------------user registeration----------------------------------------

@app.route('/register', methods = ["GET", "POST"])
def registeruser():
    if request.method == 'POST':
        firstname = request.form.get('first_name')

        lastname = request.form.get('last_name')

        dept = request.form.get('department')

        username = request.form.get('user_name')

        password = request.form.get('user_password')

        email = request.form.get('email')

        contactno = request.form.get('contact_no')

        employeeid = request.form.get('employee_id')

        data = {
            'First Name': [firstname],
            'Last Name': [lastname],
            'Department': [dept],
            'Username': [username],
            'Password': [password],
            'Email': [email],
            'Contact No': [contactno],
            'Employee ID': [employeeid]
        }
        existing_data = pd.read_excel('registereduser.xlsx')
        df = pd.DataFrame(data)
        updated_data = pd.concat([existing_data, df])
        updated_data.to_excel('registereduser.xlsx', index=False)
        # df.to_csv('registereduser.csv', mode='a', index=False, header=False)
        print(updated_data)
        return print('Data saved to excel')
    
    return render_template('registeruser.html')
# @app.route('/userreg2.html', methods=['POST'])
# def userregg2():
#     return render_template('userreg2.html')
#-----------------------------------------------------------------------------------------
exFile = 'requests.xlsx'
df = pd.read_excel(exFile)
trainer_frame = pd.read_excel('ExpertRegister.xlsx')

#---------------------------------------plotting the course vs trainers--------------------------------------
available_trainers = trainer_frame[trainer_frame['Availability'] == 'Yes']

#group the data by course name count the no of trainers
course_trainer_counts = available_trainers['Course Name'].value_counts().reset_index()
course_trainer_counts.columns = ['Course Name', 'Count']

#create a bar chart
fig = px.bar(course_trainer_counts, x='Course Name', y='Count', title='Number of Available Trainers per Course') 
fig.update_traces(
    marker_color="#000080",  # customize the bar color 
    selector=dict(type="bar"),
    width=0.2,  # Adjust  bar width
)
# Layout customization
fig.update_layout(
    xaxis_title="Course Name",
    yaxis_title="Number of Trainers",
    bargap=0.2,  # Adjust  gap between bars
    bargroupgap=0.1, 
    plot_bgcolor='rgba(0,0,0,0)',  # Set plot background to transparent
    paper_bgcolor='rgba(0,0,0,0)',  # Set paper background to transparent
    modebar_remove="zoom"
)


bargraphJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
#----------------------------------------------------------------------------------------------------------------

#---------------------------------------------------Main Dashboard-------------------------------------------------
@app.route('/dashboard/<username>')
def dashboard(username):
    return render_template('index.html',name = username, graphJSON = graphJSON,
                           pendingrequests = len(df[df['Status'] == 'Pending']),
                           count_of_trainers = trainer_frame['ID'].nunique(),
                           bargraphJSON = bargraphJSON)
#----------------------------Training Request Section--------------------------------------
#cource request
@app.route('/request/<username>')
def course_request(username):
    new_trainer_frame = trainer_frame[trainer_frame['Availability'] == 'Yes']
    #create a dict that groups the dataframe by Course Name and creates list of trainers
    #corresponding to course name
    course_to_trainers = new_trainer_frame.groupby('Course Name')['Name'].apply(list).to_dict()
    print(course_to_trainers)

    pending_req=df[df['Status']=='Pending']
    # course = pending_req['Course Name']
    # print(course)
    return render_template('request.html',name = username,data=pending_req,
                           course_to_trainers = course_to_trainers)

#course approval
@app.route('/approve/<int:id>/<username>',methods=["GET", "POST"])
def approve_request(id, username):
    select_trainer = request.form['trainer']
    print(select_trainer)
    emp_id_frame = trainer_frame[trainer_frame['Name'] == select_trainer]
    emp_id = emp_id_frame['ID'].values[0]
    index=df[df['id']==id].index[0]
    df.at[index,'Status'] = 'Approved'
    df.at[index,'Trainer'] = emp_id
    availability_frame = trainer_frame[trainer_frame['Name'] == select_trainer].index[0]
    trainer_frame.at[availability_frame,'Availability'] = 'No'
    df.to_excel(exFile,index=False)
    trainer_frame.to_excel('ExpertRegister.xlsx',index=False)
    return redirect(url_for('course_request', username = username))

#course rejection
@app.route('/reject/<int:id>/<username>')
def reject_request(id,username):
    index=df[df['id']==id].index[0]
    df.at[index,'Status'] = 'Rejected'
    df.at[index,'Trainer'] = 'None'
    df.to_excel(exFile,index=False)
    return redirect(url_for('course_request',username = username))
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.debug = True
    app.run()


# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# if __name__ == '__main__':
#     app.debug = True
#     app.run()

