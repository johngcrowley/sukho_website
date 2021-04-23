
from flask import current_app as app
from .models import db, employee, tips, User, Crews
import pandas as pd
from df2gspread import df2gspread as d2g
from datetime import datetime as dt, timedelta
from sqlalchemy.sql import func
from sqlalchemy import desc
import config
from flask import Blueprint, redirect, request, render_template, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import math
import re





wks_name = config.Config.wks_name
spreadsheet_key = config.Config.spreadsheet_key
creds = config.Config.creds

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
@login_required
@main_bp.route('/')
def index():
    try:
        employees = employee.query.all()
    except:
        employees = 'please add employees to the database'
    return render_template('index.html',employees=employees)

@login_required
@main_bp.route('/update_emp/<int:id>',methods=["GET","POST"])
def update_emp(id):
    emp_to_update = employee.query.filter(employee.id == id).first()
    
    if request.method == "POST":
        employee.query.filter(employee.id == id).delete()
        tips.query.filter(tips.employee_id == id).delete()
        db.session.commit()
        return redirect('/')

    else:
        return render_template('update_emp.html',emp_to_update=emp_to_update)

@login_required
@main_bp.route('/redo/<int:id>',methods=["POST"])
def redo(id):
    tips.query.filter(tips.crew_id==id).delete()
    Crews.query.filter(Crews.id==id).delete()
    db.session.commit()
    return redirect('/create')


@login_required
@main_bp.route('/update/<int:id>',methods=["GET","POST"])
def update(id):
    name_to_update = User.query.filter(User.id == id).first()
    if request.method == "POST":
        
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.getlist('password')
       
        name_to_update.name = name
        name_to_update.email = email
        name_to_update.password = generate_password_hash(password[0], method='sha256')

        delete = request.form.get('delete')
        if delete != '':
            User.query.filter(User.id == id).delete()

        if password[0] != password[1]:
            msg = "Passwords must match"
            return render_template('update.html',msg=msg,name_to_update=name_to_update)
        
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return redirect('/signup')
        except:
            flash("Error! Looks like there was a problem. Try again")
            return render_template("update.html",name_to_update = name_to_update)

    else:
        return render_template("update.html",name_to_update=name_to_update)

@login_required
@main_bp.route('/add_employee',methods=["GET","POST"])
# @login_required
def add_employee():
    positions = ['Expo','Bartender','Server','Dish','Kitchen']
    if request.method == "GET":
        return render_template('add_employee.html',positions=positions)
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        position = request.form.get("pos")
        if name and email and position:
            if name == email or name == position or email == position:
                msg = 'Each field must be unique'
                return render_template('add_employee.html',msg=msg,positions=positions)
            else:    
                if employee.query.filter(employee.name == name).count() == 0:
                    new_employee = employee(
                    name=name,
                    email=email,
                    position=position
                    )
                    db.session.add(new_employee)
                    db.session.commit()
                    return redirect('/')
                else:
                    msg = 'You cannot add the same employee twice'
                    return render_template('add_employee.html',msg=msg,positions=positions)
        else:
            msg = 'Must enter all fields to submit'
            return render_template('add_employee.html',msg=msg,positions=positions)
@login_required
@main_bp.route('/create',methods=["GET","POST"])
# @login_required
def create():
    if request.method == "GET":    
        return render_template('shift.html')
    else:
        number = request.form.get("number")
        if number == 0 or number == '' or number.isdigit() == False:
            msg='please enter a number'
            return render_template('shift.html',msg=msg)
        else:
            fields = int(number)
            employees = employee.query.all()
            location = ['Marigny','Uptown']
            times = ['Lunch','Dinner']
            return render_template('filloutshift.html',fields=fields,times=times,employees=employees,location=location)

@login_required
@main_bp.route('/newshift',methods=["POST"])
def newshift():
    
    #Instantiate Crew ID by Inserting new Autoincrement value into Crews Join Table
    
    #to_email = []
    employee_ids = []
    #email = request.form.getlist("email?")
    names = request.form.getlist("employee")
    tipz = request.form.get("tips")
    location = request.form.get("loc")
    time = request.form.get("time")

    new_crew = Crews(
        created_at = dt.now() 
        )
    db.session.add(new_crew)
    db.session.commit()
    
    def check_fields(tipz):
        flag = True
        if tipz == '' or tipz == None:
            flag = False
        return flag

    def tip_split(tipz):
        FOH_count = len(names)

        FOH = round(tipz * .85) / FOH_count
        D = round(tipz * .05)
        K = round(tipz * .10)
        return FOH,D,K
    
    if  check_fields(tipz) == True:
        tipz = int(tipz)

        # shift_tips = dict(zip(names,tipz))
        # for i, key in enumerate(shift_tips.keys()):
        #     for j in email:
        #         if int(i) == int(j):
        #             whom = employee.query.filter(
        #                 employee.name == key).first()
        #             to_email.append(whom.email)
        crew_id = Crews.query.order_by(desc(Crews.created_at)).limit(1).first()

        for name in names:
            person = employee.query.filter(employee.name == name).first()
            persons_tips = tip_split(tipz)[0]
            new_shift = tips(
                employee = name,
                employee_id = person.id,
                tips = persons_tips,
                location = location,
                time = time,
                crew_id = crew_id.id
            )
            db.session.add(new_shift)
            db.session.commit()
        
        
        if time == 'Dinner':
            #Kitchen
            kitchen = employee.query.filter(employee.position == 'Kitchen').first()
            kitchen_tips = tips(
                employee = 'Kitchen',
                employee_id = kitchen.id,
                tips = tip_split(tipz)[2],
                location = location,
                time = time,
                crew_id = crew_id.id
            )
            db.session.add(kitchen_tips)
            db.session.commit()
            
            #Dish
            dish = employee.query.filter(employee.position == 'Dish').first()
            dish_tips = tips(
                employee = 'Dish',
                employee_id = dish.id,
                tips = tip_split(tipz)[1],
                location = location,
                time = time,
                crew_id = crew_id.id
            )
            db.session.add(dish_tips)
            db.session.commit()

    else:
        msg='fill out all fields'
        return render_template('shift.html',msg=msg)
    
    
    tipout = tips.query.filter(tips.crew_id==crew_id.id).all()
    c_id = crew_id.id


    return render_template('success.html',tipout=tipout,location=location,c_id=c_id)

#Helper Functions for Last 2 Routes for Tip-Out Excel file and Payroll viz

def df_prep(df):
    cols = df.columns
    df.drop(cols[0:6],axis=1,inplace=True)
    df.drop('created_at',axis=1,inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['tips'] = round(df.tips.astype(int))
    return df
           
def tip_out_prep(df):
    df['day'] = df['date'].dt.day_name().astype(str)
    df['day'] = df['day'].str.replace(r'(\w+day\b)',lambda x: x.groups()[0][:3])
    df['Date'] =  df.date.astype(str) + '\n' + df.day + '\n' + df.time.astype(str)
    df.fillna('-',inplace=True)
    df = df.pivot_table('tips','name','date')
    return df

@login_required       
@main_bp.route('/export/<location>',methods=["POST"])
def export(location):
    dataframe = pd.read_sql('''
        SELECT tips.employee_id, tips.location, tips.time, tips.crew_id, employee.position, employee.name, 
        tips.tips, "Crews".created_at FROM "Crews"
        JOIN tips ON tips.crew_id="Crews".id JOIN employee ON employee.id=tips.employee_id''',db.session.bind)

    dataframe['date'] = pd.to_datetime(dataframe['created_at']).dt.date

    loc = location

    if loc == 'Marigny':
        marigny = dataframe.loc[dataframe['location'] == 'Marigny']
        marigny_df = df_prep(marigny)
        marigny_df = tip_out_prep(marigny_df)
        d2g.upload(marigny_df, spreadsheet_key, wks_name[0], credentials=creds, row_names=True)
    elif loc == 'Uptown':
        uptown = dataframe.loc[dataframe['location'] == 'Uptown']
        uptown_df = df_prep(uptown)
        uptown_df = tip_out_prep(uptown_df)
        d2g.upload(uptown_df, spreadsheet_key, wks_name[1], credentials=creds, row_names=True)
    else:
        return redirect('/')
    msg='Success! \n\n Check out your Google Sheet for updated records'
    return render_template('success.html',msg=msg)

@login_required
@main_bp.route('/payroll',methods=["GET","POST"])
def payroll():
    dataframe = pd.read_sql('''
        SELECT tips.employee_id, tips.location, tips.time, tips.crew_id, employee.position, employee.name, 
        tips.tips, "Crews".created_at FROM "Crews"
        JOIN tips ON tips.crew_id="Crews".id JOIN employee ON employee.id=tips.employee_id''',db.session.bind)

    dataframe['date'] = pd.to_datetime(dataframe['created_at']).dt.date

    if request.method == "GET":
        return render_template('payroll.html')
    else:
        s = request.form.get("date")
        df = df_prep(dataframe)
        df = df.pivot_table('tips','name','date')
        patt = re.compile('\d{2}[-/]\d{2}[-/]\d{2}')

        if re.findall(patt,s) == []:
            print('you fucked up')
            msg='Not a valid date, try agin'
            return render_template('payroll.html',msg=msg)
        else:
            print('gucci')
            try:
                start = pd.to_datetime(s).date()
                print(start)
                try:
                    pay_period = pd.date_range(start, start + timedelta(3))
                    print(pay_period)
                    df1 = df[[pay_period[0],pay_period[3]]].copy()
                    print('df1 made')
                    df1['gross'] = df1.sum(axis=1)
                    df1['claimed'] = df1['gross'] * .60
                    df2 = df1[['gross','claimed']]
                    period = f'For the Pay period of {start} until {pay_period[-1].date()}'.format(start,pay_period)
                    return render_template('biweekly.html',df2=df2,period=period)
                except:
                    print('is datetime, but something off with ranges')
                    msg = 'is datetime, but something off with ranges'
                    return render_template('payroll.html',msg=msg)
            except:
                #if they a sneaky one and try to put in random nubmers in format
                msg = 'valid format, but not a valid date, good try.'
                return render_template('payroll.html',msg=msg)

    


