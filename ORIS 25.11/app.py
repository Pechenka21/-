from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('ideas.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    cursor = conn.execute('SELECT COUNT(*) FROM categories')
    if cursor.fetchone()[0] == 0:
        conn.execute('INSERT INTO categories (name) VALUES (?)', ('Работа',))
        conn.execute('INSERT INTO categories (name) VALUES (?)', ('Учеба',))
        conn.execute('INSERT INTO categories (name) VALUES (?)', ('Личное',))

        conn.execute('INSERT INTO ideas (title, description, category_id) VALUES (?, ?, ?)',
                     ('Learn Flask', 'Some description', 2))
        conn.execute('INSERT INTO ideas (title, description, category_id) VALUES (?, ?, ?)',
                     ('Create a portfolio', 'Make a personal website', 1))

    conn.commit()
    conn.close()


@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    conn = get_db_connection()

    base_query = '''
        SELECT ideas.*, categories.name as category_name 
        FROM ideas 
        LEFT JOIN categories ON ideas.category_id = categories.id
    '''

    if q:
        query = base_query + ' WHERE ideas.title LIKE ?'
        ideas = conn.execute(query, ('%' + q + '%',)).fetchall()
    else:
        ideas = conn.execute(base_query).fetchall()

    conn.close()
    return render_template("index.html", ideas=ideas, q=q)


@app.route("/ideas/<int:idea_id>")
def detail(idea_id):
    conn = get_db_connection()
    query = '''
        SELECT ideas.*, categories.name as category_name 
        FROM ideas 
        LEFT JOIN categories ON ideas.category_id = categories.id
        WHERE ideas.id = ?
    '''
    idea = conn.execute(query, (idea_id,)).fetchone()
    conn.close()

    if idea is None:
        return "Idea not found", 404

    return render_template("detail.html", idea=idea)


@app.route("/ideas/add", methods=["GET", "POST"])
def add_idea():
    conn = get_db_connection()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category_id = request.form.get("category_id", "")

        errors = []
        if not title:
            errors.append("Title is required")
        if not description:
            errors.append("Description is required")

        if errors:
            categories = conn.execute('SELECT * FROM categories').fetchall()
            conn.close()
            return render_template("add.html", errors=errors, title=title, description=description,
                                   categories=categories, selected_cat=category_id)

        conn.execute('INSERT INTO ideas (title, description, category_id) VALUES (?, ?, ?)',
                     (title, description, category_id if category_id else None))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template("add.html", categories=categories)


@app.route("/ideas/<int:idea_id>/edit", methods=["GET", "POST"])
def edit_idea(idea_id):
    conn = get_db_connection()
    idea = conn.execute('SELECT * FROM ideas WHERE id = ?', (idea_id,)).fetchone()

    if idea is None:
        conn.close()
        return "Idea not found", 404

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category_id = request.form.get("category_id", "")

        errors = []
        if not title:
            errors.append("Title is required")
        if not description:
            errors.append("Description is required")

        if errors:
            categories = conn.execute('SELECT * FROM categories').fetchall()
            conn.close()
            return render_template("edit.html", errors=errors, title=title, description=description, idea_id=idea_id,
                                   categories=categories, selected_cat=category_id)

        conn.execute('UPDATE ideas SET title = ?, description = ?, category_id = ? WHERE id = ?',
                     (title, description, category_id if category_id else None, idea_id))
        conn.commit()
        conn.close()
        return redirect(url_for("detail", idea_id=idea_id))

    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template("edit.html", title=idea['title'], description=idea['description'], idea_id=idea_id,
                           categories=categories, selected_cat=idea['category_id'])


@app.route("/ideas/<int:idea_id>/delete", methods=["POST"])
def delete_idea(idea_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM ideas WHERE id = ?', (idea_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
