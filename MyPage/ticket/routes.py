from ticket import app, db
from flask import render_template, request, flash, url_for, redirect, session
from sqlalchemy import text

@app.route('/')
def home_page():
    #cookie = request.cookies.get('name')
    cookie = session.get('username')
    print("<>home_page()")
    #return render_template('home.html', cookie=cookie)

    #users
    query_count_users=f"select count(*) from mypageusers"
    result = db.session.execute(text(query_count_users))
    count_users = result.fetchone()[0]    #touple unpack??
    print("Number of users: ", count_users)

    #posts
    query_count_status=f"select count(*) from mypagestatus"
    result = db.session.execute(text(query_count_status))
    count_status = result.fetchone()[0]    #touple unpack??
    print("Number of posts: ", count_status)
    return render_template('home.html', count_users=count_users, count_status=count_status, cookie=cookie)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    print("register was called")
    if request.method == 'POST':
        print('->register_page()')
        username = request.form.get('Username')
        email = request.form.get('Email')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        print("Provided Username: ", username)
        print("Provided Email: ", email)
        print("PW1: ", password1)
        print("PW2:", password2)

        if (username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            print("Invalid username")
            #flash("Invalid username", category='danger')
            print("<-register_page(), username not valid")
            return render_template('register.html', cookie=None)

        if(email is None or
                isinstance(email, str) is False or
                len(email) < 3):
            print("Invalid email")
            print("<-register_page(), email not valid")
            #flash("Invalid email",category = "danger")
            return render_template('register.html', cookie=None)

        if(password1 is None or
                isinstance(password1,str) is False or
                len(password1) < 3 or
                password1 != password2):
            print('First password invalid!')
            print("<-register_page(), pw1 not valid")
            #flash("Invalid first password", category="danger")
            return render_template('register.html', cookie=None)

        #schauen ob eintrag in db ist fuer username
        query_stmt = f"select * from mypageusers where username = '{username}'"
        print("Query Statement: ",query_stmt)
        result = db.session.execute(text(query_stmt))
        #fetchone ist ein item aus liste
        item = result.fetchone()
        print("Already existing item: ", item)

        #falls username existiert schon
        if item is not None:
            #flash(f"Username exists try again", category="danger")
            print("username exists")
            return render_template('register.html', cookie=None)

        #eintag in db fuer neuen user
        query_insert = f"insert into mypageusers (username, email, password) values ('{username}', '{email}', '{password1}')"
        print("Query Insert: ", query_insert)
        db.session.execute(text(query_insert))
        #wichtig committen
        db.session.commit()
        #flash("You are registered", category="success")
        #resp=redirect('/')
        #resp.set_cookie('name', username)
        print("<-register_page(), go to feed_page()")
        return redirect(url_for('feed_pages'))
        #return resp

    return render_template('register.html', cookie=None)

@app.route('/login', methods=['GET', 'POST'])
def login_pages():
    print("login was called")

    if request.method == 'POST':
        print("->login_pages()")
        username = request.form.get('Username')
        password = request.form.get('Password')
        print("Here's the LOGIN data!!!")
        print("User submitted username:", username)
        print("User submitted pw:", password)

        if (username is None or
                isinstance(username,str) is False or
                len(username) < 3):
            print('Invalid username')
            #flash(f"Username is not valid", category='warning')
            return render_template('login.html', cookie=None)

        if (password is None or
                isinstance(password,str) is False or
                len(password) < 3):
            print("Invalid password")
            #flash(f"Password not valid", category='warning')
            return render_template('login.html', cookie=None)

        query_stmt = f"select username from mypageusers where username = '{username}' and password = '{password}'"
        print(query_stmt)
        # text konvertieren in alchemy text
        result = db.session.execute(text(query_stmt))
        # resultat holen
        user = result.fetchall()

        if not user:
            #flash(f"Invalid Credentials. Try again!", category='warning')
            return render_template('login.html', cookie=None)

        #falls alles klappt
        #username key in session
        session['username'] = username
        #flash(f"'{user}', you are logged in :D", category='success')
        #resp=redirect('/feed')
        #resp.set_cookie('name', username)
        print("<-login(), go to feed_pages")
        #return resp
        return redirect(url_for('feed_pages'))
        # alternativ
        # return render_template('status.html)

    return render_template('login.html', cookie=None)


@app.route('/logout')
def logout():
    if 'username' not in session:
        #flash("You can't log out if you weren't signed in :)", category='info')
        #return redirect(url_for('home_page'))
        session.pop('username', None)
    # flash("You have been logged out. See you!", category='info')
        return redirect(url_for('home_page'))

    #resp=redirect('/')
    #resp.set_cookie('name', '', expires=0)
    #return resp

@app.route('/feed')
def feed_pages():
    if 'username' not in session:
    #     #flash('You need to log in first', category='warning')
        return redirect(url_for('login_pages'))

    #items = [{"id": 1, "prio": 2, "user": "Mark", "title":"backend broken"},
    #        {"id": 2, "prio": 1, "user": "Luke", "title":"GUI not working"},
    #        {"id": 3, "prio": 2, "user": "Han", "title":"Nothing works"}]
    #query_stmt = f"select * from mypagestatus"

    #cookie = request.cookies.get('name')
    cookie = session.get('username')
    print("<-feed_pages()", cookie)
    if not session.get('username'):
        return redirect(url_for('login_pages'))

    query_stmt = f"SELECT mypageusers.id, mypageusers.username, mypagestatus.feeling, songname, color FROM mypagestatus INNER JOIN mypageusers ON mypagestatus.user_id = mypageusers.id order by mypagestatus.id"
    result = db.session.execute(text(query_stmt))
    itemsquery = result.fetchall()
    print("items_feed:", itemsquery)

    return render_template('feed.html', items=itemsquery, cookie=cookie)

@app.route('/feed_entry', methods=['GET', 'POST'])
def feed_entry():
    #cookie=request.cookies.get('name')
    cookie = session.get('username')
    print('->feed_entry()', cookie)
    if not cookie:
        print("no cookie")
        return redirect(url_for('login_pages'))

    if request.method == 'POST':
        print("hello hier post")
        username = session.get('username')

        user_id_query=f"SELECT id FROM mypageusers WHERE username = '{username}'"
        print(user_id_query)
        #exekutieren und in alchemy text
        result_id = db.session.execute(text(user_id_query))
        #holen
        user_id = result_id.fetchone()[0]
        print(user_id)

        feeling = request.form.get('Feeling')
        songname = request.form.get('Song')
        color = request.form.get('Color')

        print("feeling: ", feeling)
        print("songname: ", songname)
        print("color: ", color)



        query_insert= f"insert into mypagestatus (user_id, feeling, songname, color) values ('{user_id}','{feeling}','{songname}','{color}')"
        print(query_insert)
        db.session.execute(text(query_insert))
        db.session.commit()
        print("hey erfolgreich status_insert")

        #resp = redirect("/feed")
        #resp.set_cookie('name', cookie)
        #return resp

    return render_template('feed_entry.html', cookie=cookie)

@app.route('/feed_item/<item_id>', methods=['GET'])
def feed_item(item_id):
    print("<-feed_item()", item_id)
    #cookie = request.cookies.get('name')
    cookie = session.cookies('username')
    print('->cookie', cookie)
    if not cookie:
        print("no cookie")
        return redirect(url_for('login_pages'))

    # item_id = f"select id from mypageusers where username='{item_name}'"
    # result_item_name_to_id= db.session.execute(text(item_id))
    # item_name_to_id = result_item_name_to_id.fetchone()[0]



    #query_stmt = f"select * from mypagestatus where user_id={item_id}"
    query_stmt = f" select mypageusers.username, mypagestatus.* from mypagestatus inner join mypageusers on mypagestatus.user_id = mypageusers.id where mypagestatus.user_id = {item_id}"
    print("query sttmnt", query_stmt)
    result = db.session.execute(text(query_stmt))
    item = result.fetchall()
    print("item:", item)
    if not item:
        print("no such item")
        #error handling....


    # query_username = f"SELECT username FROM mypageusers WHERE id={item_id}"
    # result_username = db.session.execute(text(query_username))
    # username = result_username.fetchone()[0]

    #cookie = request.cookies.get('name')
    cookie = session.get('username')


    return render_template('feed_item.html', item=item, cookie=cookie)
