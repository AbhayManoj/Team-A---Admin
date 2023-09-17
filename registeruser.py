import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def registeruser():
    if request.method == 'POST':
        firstname = request.form.get('first_name')

        lastname = request.form.get('last_name')

        dept = request.form.get('department')

        username = request.form.get('user_name')

        password = request.form.get('user_password')

        cpassword = request.form.get('confirm_password')

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
        df = pd.DataFrame(data)
        df.to_csv('registereduser.csv', mode='a', index=False, header=False)
        print(df)
        return print('Data saved to excel')
    
    return render_template('registeruser.html')

if __name__ == '__main__':
    app.run()
