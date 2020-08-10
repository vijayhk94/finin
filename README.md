This project implements a JWT based auth system.

It uses following to do so:
1. Django
2. DRF
3. djangorestframework-jwt.
4. rest_auth

List of APIs:
1. Signup
2. Login
3. Logout
4. Force Logout
5. Test API: authenticated/authorized API to test auth system.(only allowed to admin)

Core problem:
Implementing signup/login are very easy to implement using rest_auth and djangorestframework-jwt.
The real problem is with implementation of logout.
The way JWT works, access to a authorized resource is allowed if token passed is not expired.
A token cant be expired on command either, once issued it will remain valid till expiry.
Due to this JWT doesn't really have a concrete logout functionality. It basically doesn't store tokens in DB at all.
To logout, all it does is it deletes the token cookie from the client.
To solve this problem then, you have to start storing tokens in DB/maintain a list of tokens that are blacklisted.
Add tokens to balcklist whenever logout for a user happens.
Write a custom permission class to check if the token being passed to authorized resource is not from 
the blacklist and then allow access.

To view actual implementation, checkout model: JWTToken. Permission class IsTokenValid.

To run:
1. clone the project. import in pycharm, create virtual env, run: pip install -r requirements.txt
2. db is already present, delete db.sqlite3 file if you want to test from scratch.
3. run python manage.py migrate to create db schema.
4. run server using python manage.py runserver.
5. use postman collection to test APIs.(contains data schema for APIs as well.)
6. to test force logout API, a superuser needs to be created. create using command: python manager



Transactions fetch from gmail task:
1. This is executed using script: email_script.py. use this command: python email_script.py
2. script will prompt for uname and pwd, start_date, end_date for emails to be parsed.
3. password to be given here will be app password, not mail pwd. to generate it follow this:https://support.google.com/accounts/answer/185833?hl=en
4. script will end up creating a transactions.csv file in finin/ directory. this csv will have all transactions in that period,
it will capture transaction type, amount, date for each transaction.


