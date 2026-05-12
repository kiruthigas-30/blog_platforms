from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "blogsecretkey"

# MYSQL CONFIGURATION
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'kiruthiga'
app.config['MYSQL_DB'] = 'blog_platform'

mysql = MySQL(app)

# FIRST PAGE -> REGISTER
@app.route('/')
def first():

    return redirect('/register')

# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        # GET INPUT FROM HTML
        username = request.form['username']

        email = request.form['email']

        password = request.form['password']

        cur = mysql.connection.cursor()

        # CHECK EMAIL EXISTS
        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cur.fetchone()

        if existing_user:

            return "Email already registered"

        # INSERT USER
        cur.execute(
            """
            INSERT INTO users(
                username,
                email,
                password
            )
            VALUES(%s,%s,%s)
            """,
            (
                username,
                email,
                password
            )
        )

        mysql.connection.commit()

        return redirect('/login')

    return render_template("register.html")

# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        # GET INPUT
        email = request.form['email']

        password = request.form['password']

        cur = mysql.connection.cursor()

        # CHECK MYSQL USER
        cur.execute(
            """
            SELECT * FROM users
            WHERE email=%s
            AND password=%s
            """,
            (
                email,
                password
            )
        )

        user = cur.fetchone()

        # LOGIN SUCCESS
        if user:

            session['user_id'] = user[0]

            session['username'] = user[1]

            return redirect('/dashboard')

        # LOGIN FAILED
        else:

            return "Invalid Email or Password"

    return render_template("login.html")

# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:

        return redirect('/login')

    cur = mysql.connection.cursor()

    # GET POSTS
    cur.execute("""
        SELECT posts.id,
               posts.title,
               posts.content,
               posts.created_at,
               users.username
        FROM posts
        JOIN users
        ON posts.user_id = users.id
        ORDER BY posts.id DESC
    """)

    posts = cur.fetchall()

    return render_template(
        "dashboard.html",
        posts=posts
    )

# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

# CREATE POST
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():

    if 'user_id' not in session:

        return redirect('/login')

    if request.method == 'POST':

        title = request.form['title']

        content = request.form['content']

        cur = mysql.connection.cursor()

        # INSERT POST
        cur.execute(
            """
            INSERT INTO posts(
                title,
                content,
                user_id
            )
            VALUES(%s,%s,%s)
            """,
            (
                title,
                content,
                session['user_id']
            )
        )

        mysql.connection.commit()

        return redirect('/dashboard')

    return render_template("create_post.html")

# VIEW POST + COMMENT
@app.route('/post/<int:id>', methods=['GET', 'POST'])
def view_post(id):

    cur = mysql.connection.cursor()

    # ADD COMMENT
    if request.method == 'POST':

        if 'user_id' not in session:

            return redirect('/login')

        comment = request.form['comment']

        # INSERT COMMENT
        cur.execute(
            """
            INSERT INTO comments(
                comment,
                user_id,
                post_id
            )
            VALUES(%s,%s,%s)
            """,
            (
                comment,
                session['user_id'],
                id
            )
        )

        mysql.connection.commit()

    # GET SINGLE POST
    cur.execute("""
        SELECT posts.id,
               posts.title,
               posts.content,
               posts.created_at,
               users.username
        FROM posts
        JOIN users
        ON posts.user_id = users.id
        WHERE posts.id=%s
    """, (id,))

    post = cur.fetchone()

    # GET COMMENTS
    cur.execute("""
        SELECT comments.comment,
               comments.created_at,
               users.username
        FROM comments
        JOIN users
        ON comments.user_id = users.id
        WHERE comments.post_id=%s
        ORDER BY comments.id DESC
    """, (id,))

    comments = cur.fetchall()

    return render_template(
        "view_post.html",
        post=post,
        comments=comments
    )

# EDIT POST
@app.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):

    if 'user_id' not in session:

        return redirect('/login')

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        title = request.form['title']

        content = request.form['content']

        # UPDATE POST
        cur.execute("""
            UPDATE posts
            SET title=%s,
                content=%s
            WHERE id=%s
            AND user_id=%s
        """,
        (
            title,
            content,
            id,
            session['user_id']
        ))

        mysql.connection.commit()

        return redirect('/dashboard')

    # GET POST
    cur.execute(
        "SELECT * FROM posts WHERE id=%s",
        (id,)
    )

    post = cur.fetchone()

    return render_template(
        "edit_post.html",
        post=post
    )

# DELETE POST
@app.route('/delete_post/<int:id>')
def delete_post(id):

    if 'user_id' not in session:

        return redirect('/login')

    cur = mysql.connection.cursor()

    # DELETE COMMENTS
    cur.execute(
        "DELETE FROM comments WHERE post_id=%s",
        (id,)
    )

    # DELETE POST
    cur.execute(
        """
        DELETE FROM posts
        WHERE id=%s
        AND user_id=%s
        """,
        (
            id,
            session['user_id']
        )
    )

    mysql.connection.commit()

    return redirect('/dashboard')

if __name__ == '__main__':

    app.run(debug=True)