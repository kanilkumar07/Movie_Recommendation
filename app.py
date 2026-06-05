from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    session
)
from flask_mail import Mail, Message
from flask_mysqldb import MySQL

from chatbot import movie_chatbot
import smtplib

from model import (
    recommend,
    get_movie
)

app = Flask(__name__)

# ================= MAIL CONFIG =================

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'

# app.config['MAIL_PORT'] = 587

# app.config['MAIL_USE_TLS'] = True

# app.config['MAIL_USERNAME'] = 'kanilkumar8419@gmail.com'

# app.config['MAIL_PASSWORD'] = 'nznduwtedixiozez'

# mail = Mail(app)

# ================= SECRET KEY =================

app.secret_key = "movie_secret"

# ================= MYSQL CONFIG =================

app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = '123456'

app.config['MYSQL_DB'] = 'movie_db'

mysql = MySQL(app)

# ================= HOME =================

# @app.route('/')

# def home():

#     return render_template(
#         'index.html'
#     )

# ================= RECOMMEND =================

@app.route(
    '/recommend',
    methods=['POST']
)

def recommendation():

    movie_name = request.form.get(
        'movie'
    )

    recommendations = recommend(
        movie_name
    )

    return render_template(

        'result.html',

        recommendations=recommendations

    )

# ================= MOVIE DETAIL =================

@app.route('/movie/<movie_name>')

def movie_detail(movie_name):

    movie = get_movie(movie_name)

    return render_template(

        'movie_detail.html',

        movie=movie

    )

# ================= HOME =================

@app.route('/')

def home():

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM movies"
    )

    movies = cur.fetchall()

    cur.close()

    return render_template(

        'index.html',

        movies=movies

    )

# ================= CHATBOT PAGE =================

@app.route('/chatbot')

def chatbot():

    return render_template(
        'chatbot.html'
    )

# ================= CHATBOT RESPONSE =================

@app.route(
    '/get_chat',
    methods=['POST']
)

def get_chat():

    user_message = request.form[
        'message'
    ]

    response = movie_chatbot(
        user_message
    )

    return jsonify(response)

# ================= FAVORITES PAGE =================

@app.route('/favorites')

def favorites():

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM favorites"
    )

    data = cur.fetchall()

    cur.close()

    return render_template(

        'favorites.html',

        favorites=data

    )




# ================= REGISTER PAGE =================

@app.route('/register')

def register_page():

    return render_template(
        'register.html'
    )

# ================= REGISTER USER =================

@app.route(
    '/register_user',
    methods=['POST']
)

def register_user():

    name = request.form['name']

    email = request.form['email']

    password = request.form['password']

    role = "user"

    cur = mysql.connection.cursor()

    cur.execute(

        """

        INSERT INTO users
        (
            name,
            email,
            password,
            role
        )

        VALUES(%s,%s,%s,%s)

        """,

        (
            name,
            email,
            password,
            role
        )

    )

    mysql.connection.commit()

    # ================= SEND EMAIL =================

#     msg = Message(

#         'New User Registered',

#         sender='movierecommed@gmail.com',

#         recipients=['kanilmahto071gmail.com']

#     )

#     msg.body = f"""

# New User Registered

# Name: {name}

# Email: {email}

# """

#     mail.send(msg)

    

    cur.close()

    

    return redirect('/login')

# ================= LOGIN PAGE =================

@app.route(
    '/login_user',
    methods=['POST']
)

def login_user():

    email = request.form['email']

    password = request.form['password']

    cur = mysql.connection.cursor()

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

    cur.close()

    if user:

        session['user'] = user[1]

        session['role'] = user[4]

        # ================= ADMIN =================

        if user[4] == "admin":

            return redirect('/admin')

        # ================= USER =================

        else:

            return redirect('/home')

    else:

        return "Invalid Email or Password"

# ================= HOME PAGE =================

# ================= HOME PAGE =================

@app.route('/home')

def home_page():

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM movies"
    )

    movies = cur.fetchall()

    cur.close()

    return render_template(

        'home.html',

        movies=movies

    )



# ================= LOGOUT =================


@app.route('/logout')

def logout():

    session.clear()

    return redirect('/login')

# ================= LOGIN PAGE =================

@app.route('/login')

def login_page():

    return render_template(
        'login.html'
    )


# ================= ADMIN PANEL =================

@app.route('/admin')

def admin():

    if 'role' in session:

        if session['role'] == "admin":

            cur = mysql.connection.cursor()

            cur.execute(
                "SELECT COUNT(*) FROM users"
            )

            total_users = cur.fetchone()[0]

            cur.execute(
                "SELECT COUNT(*) FROM favorites"
            )

            total_favorites = cur.fetchone()[0]

            cur.close()

            return render_template(

                'admin.html',

                total_users=total_users,

                total_favorites=total_favorites

            )

    return redirect('/login')

# ================= ADD MOVIE PAGE =================

@app.route('/add_movie')

def add_movie_page():

    if 'role' in session:

        if session['role'] == "admin":

            return render_template(
                'add_movie.html'
            )

    return redirect('/login')

# ================= SAVE MOVIE =================

@app.route(
    '/save_movie',
    methods=['POST']
)

def save_movie():

    if 'role' in session:

        if session['role'] == "admin":

            name = request.form['name']

            poster = request.form['poster']

            rating = request.form['rating']

            year = request.form['year']

            trailer = request.form['trailer']

            description = request.form['description']

            cur = mysql.connection.cursor()

            cur.execute(

                """

                INSERT INTO movies
                (
                    name,
                    poster,
                    rating,
                    year,
                    trailer,
                    description
                )

                VALUES(%s,%s,%s,%s,%s,%s)

                """,

                (
                    name,
                    poster,
                    rating,
                    year,
                    trailer,
                    description
                )

            )

            mysql.connection.commit()

            cur.close()

            return redirect('/admin')

    return redirect('/login')

# ================= ALL MOVIES =================

@app.route('/all_movies')

def all_movies():

    if 'role' in session:

        if session['role'] == "admin":

            cur = mysql.connection.cursor()

            cur.execute(
                "SELECT * FROM movies"
            )

            movies = cur.fetchall()

            cur.close()

            return render_template(

                'all_movies.html',

                movies=movies

            )

    return redirect('/login')

# ================= DELETE MOVIE =================

@app.route('/delete_movie/<int:id>')

def delete_movie(id):

    if 'role' in session:

        if session['role'] == "admin":

            cur = mysql.connection.cursor()

            cur.execute(

                "DELETE FROM movies WHERE id=%s",

                (id,)

            )

            mysql.connection.commit()

            cur.close()

            return redirect('/all_movies')

    return redirect('/login')

# ================= ALL USERS =================

@app.route('/all_users')

def all_users():

    if 'role' in session:

        if session['role'] == "admin":

            cur = mysql.connection.cursor()

            cur.execute(
                "SELECT * FROM users"
            )

            users = cur.fetchall()

            cur.close()

            return render_template(

                'all_users.html',

                users=users

            )

    return redirect('/login')

# ================= DELETE USER =================

@app.route('/delete_user/<int:id>')

def delete_user(id):

    if 'role' in session:

        if session['role'] == "admin":

            cur = mysql.connection.cursor()

            cur.execute(

                "DELETE FROM users WHERE id=%s",

                (id,)

            )

            mysql.connection.commit()

            cur.close()

            return redirect('/all_users')

    return redirect('/login')

# ================= EDIT MOVIE PAGE =================

@app.route('/edit_movie/<int:id>')

def edit_movie(id):

    if 'role' in session:

        if session['role'] == "admin":

            cur = mysql.connection.cursor()

            cur.execute(

                "SELECT * FROM movies WHERE id=%s",

                (id,)

            )

            movie = cur.fetchone()

            cur.close()

            return render_template(

                'edit_movie.html',

                movie=movie

            )

    return redirect('/login')

# ================= UPDATE MOVIE =================

@app.route(
    '/update_movie/<int:id>',
    methods=['POST']
)

def update_movie(id):

    if 'role' in session:

        if session['role'] == "admin":

            name = request.form['name']

            poster = request.form['poster']

            rating = request.form['rating']

            year = request.form['year']

            trailer = request.form['trailer']

            description = request.form['description']

            cur = mysql.connection.cursor()

            cur.execute(

                """

                UPDATE movies

                SET

                name=%s,
                poster=%s,
                rating=%s,
                year=%s,
                trailer=%s,
                description=%s

                WHERE id=%s

                """,

                (
                    name,
                    poster,
                    rating,
                    year,
                    trailer,
                    description,
                    id
                )

            )

            mysql.connection.commit()

            cur.close()

            return redirect('/all_movies')

    return redirect('/login')


movies = [
    {
        "title": "Interstellar",
        "trailer_link": "https://prmovies.courses/interstellar-wars-2016-Watch-online-full-movie/"
    }
]

# ================= RUN =================

if __name__ == '__main__':

    app.run(debug=True)