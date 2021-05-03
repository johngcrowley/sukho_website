# johngcrowley-lagniapp-for-sukho-thai
I made a project to automate payroll, tipout, and data visualization tasks for General Management at Sukho Thai LLC.
It's honestly really sweet. 
Without admin or manager access, you can't play around with it, but it is live at https://www.sukhoapp.herokuapp.com

- admin access that controls views and can update / delegate manager access
- manager access that controls some views and can update employees, shift tips, database, and export info to according stores' google sheet. 
- payroll calculator for Gross income, taxed income, and groupbys for each employee by customizable 2 week pay periods. 
- bug checked routes with fail-safes, re-do's, and error-messaging
- enabled testing with Mabl 
- created a CI/CD pipeline, triggering deployments and Github checks using Mabl CLI

Functionality I'd Like to add:
- implement sendgrid email server to automate giving employees' tip information to their inbox // 
OR
- implement individualized google worksheets per employee granting them view access to a pivot table of their history / date / time of income (preferred)
