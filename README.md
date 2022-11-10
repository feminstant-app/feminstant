# FemInstant

On MySQL:

1. Ensure you have set up a user with the username and password as `admin`
2. Under administration, users and privileges, Administrative Roles - ensure that all the boxes have been ticked and then press ‘Apply’
3. Create a database called `feminstant` and run.

On PyCharm:

1. First ensure you have the following packages installed. If you use pip as your package manager, you can run `pip install -r requirements.txt` to install them automatically.
    - Flask
    - Flask-SQLAlchemy
    - Flask-WTF 
    - Flask-Login 
    - Flask-Bcrypt 
    - PyMySQL
    - Bcrypt 
    - Email-validator 
    - Requests
    - Stripe
2. Create a new python file called `config.py` and paste the context of the separate document sent to instructors (not uploaded on github) with the secret keys and passwords. 
3. Run the `sample_data.py` file
4. Run `app.py`
