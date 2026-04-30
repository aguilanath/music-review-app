from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import get_connection

app = Flask(__name__)
app.secret_key = "cs348_secret_key"

# ─────────────────────────────────────────────
# all_users context processor to make it available in all templates for dropdowns and user info
# ─────────────────────────────────────────────

@app.context_processor
def inject_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name FROM Users ORDER BY name")
    users = cursor.fetchall()
    conn.close()
    return dict(all_users=users, session=session)

# ─────────────────────────────────────────────
# User Login (rough template, no actual login just selection)
# ─────────────────────────────────────────────

@app.route("/set_user", methods=["POST"])
def set_user():
    session["user_id"] = request.form.get("user_id")
    session["user_name"] = request.form.get("user_name")
    return redirect(request.referrer or url_for("index"))

# ─────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ─────────────────────────────────────────────
# 2a - Insert, Update, Delete, Reviews
# ─────────────────────────────────────────────

@app.route("/reviews")
def reviews():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.review_id, r.rating, r.comment, r.created_at, r.user_id,
               u.name AS user_name,
               al.title AS album_title,
               ar.name AS artist_name
        FROM Reviews r
        JOIN Users u ON r.user_id = u.user_id
        JOIN Albums al ON r.album_id = al.album_id
        JOIN Artists ar ON al.artist_id = ar.artist_id
        ORDER BY r.created_at DESC
    """)
    reviews = cursor.fetchall()
    conn.close()
    return render_template("reviews/index.html", reviews=reviews)


@app.route("/reviews/new", methods=["GET", "POST"])
def new_review():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        user_id = session["user_id"]
        album_id = request.form["album_id"]
        rating = request.form["rating"]
        comment = request.form["comment"]

        cursor.execute(
            "INSERT INTO Reviews (user_id, album_id, rating, comment) VALUES (%s, %s, %s, %s)",
            (user_id, album_id, rating, comment)
        )
        conn.commit()
        conn.close()
        flash("Review added successfully!", "success")
        return redirect(url_for("reviews"))

    # Populate dropdowns from DB
    cursor.execute("SELECT user_id, name FROM Users ORDER BY name")
    users = cursor.fetchall()

    cursor.execute("""
        SELECT al.album_id, al.title, ar.name AS artist_name
        FROM Albums al
        JOIN Artists ar ON al.artist_id = ar.artist_id
        ORDER BY ar.name, al.title
    """)
    albums = cursor.fetchall()
    conn.close()
    return render_template("reviews/form.html", users=users, albums=albums, review=None)


@app.route("/reviews/<int:review_id>/edit", methods=["GET", "POST"])
def edit_review(review_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        user_id = request.form["user_id"]
        album_id = request.form["album_id"]
        rating = request.form["rating"]
        comment = request.form["comment"]

        cursor.execute("""
            UPDATE Reviews
            SET user_id=%s, album_id=%s, rating=%s, comment=%s
            WHERE review_id=%s
        """, (user_id, album_id, rating, comment, review_id))
        conn.commit()
        conn.close()
        flash("Review updated successfully!", "success")
        return redirect(url_for("reviews"))

    cursor.execute("SELECT * FROM Reviews WHERE review_id=%s", (review_id,))
    review = cursor.fetchone()

    cursor.execute("SELECT user_id, name FROM Users ORDER BY name")
    users = cursor.fetchall()

    cursor.execute("""
        SELECT al.album_id, al.title, ar.name AS artist_name
        FROM Albums al
        JOIN Artists ar ON al.artist_id = ar.artist_id
        ORDER BY ar.name, al.title
    """)
    albums = cursor.fetchall()
    conn.close()
    return render_template("reviews/form.html", users=users, albums=albums, review=review)


@app.route("/reviews/<int:review_id>/delete", methods=["POST"])
def delete_review(review_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Reviews WHERE review_id=%s", (review_id,))
    conn.commit()
    conn.close()
    flash("Review deleted.", "info")
    return redirect(url_for("reviews"))


# ─────────────────────────────────────────────
# REQUIREMENT 2 — Report Interface
# ─────────────────────────────────────────────

@app.route("/report", methods=["GET", "POST"])
def report():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Populate filter dropdowns
    cursor.execute("SELECT artist_id, name FROM Artists ORDER BY name")
    artists = cursor.fetchall()

    cursor.execute("SELECT DISTINCT genre FROM Albums WHERE genre IS NOT NULL ORDER BY genre")
    genres = cursor.fetchall()

    results = []
    stats = None
    filters = {}

    if request.method == "POST":
        filters = {
            "artist_id": request.form.get("artist_id"),
            "genre": request.form.get("genre"),
            "rating_min": request.form.get("rating_min"),
            "rating_max": request.form.get("rating_max"),
            "date_from": request.form.get("date_from"),
            "date_to": request.form.get("date_to"),
        }

        query = """
            SELECT r.review_id, r.rating, r.comment, r.created_at,
                   u.name AS user_name,
                   al.title AS album_title, al.genre AS album_genre,
                   ar.name AS artist_name
            FROM Reviews r
            JOIN Users u ON r.user_id = u.user_id
            JOIN Albums al ON r.album_id = al.album_id
            JOIN Artists ar ON al.artist_id = ar.artist_id
            WHERE TRUE
        """
        params = []
        param_string = ""

        if filters["artist_id"]:
            param_string += " AND ar.artist_id = %s"
            params.append(filters["artist_id"])
        if filters["genre"]:
            param_string += " AND al.genre = %s"
            params.append(filters["genre"])
        if filters["rating_min"]:
            param_string += " AND r.rating >= %s"
            params.append(filters["rating_min"])
        if filters["rating_max"]:
            param_string += " AND r.rating <= %s"
            params.append(filters["rating_max"])
        if filters["date_from"]:
            param_string += " AND r.created_at >= %s"
            params.append(filters["date_from"])
        if filters["date_to"]:
            param_string += " AND r.created_at <= %s"
            params.append(filters["date_to"])

        query += param_string
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Stats over filtered results
        if results:
            stats_query = """
                SELECT
                    COUNT(*) AS total_reviews,
                    ROUND(AVG(r.rating), 2) AS avg_rating,
                    MAX(r.rating) AS highest_rating,
                    MIN(r.rating) AS lowest_rating
                FROM Reviews r
                JOIN Albums al ON r.album_id = al.album_id
                JOIN Artists ar ON al.artist_id = ar.artist_id
                WHERE TRUE
            """

            stats_query += param_string + " ORDER BY r.created_at DESC"

            cursor.execute(stats_query, params)
            stats = cursor.fetchone()

    conn.close()
    return render_template("report.html", artists=artists, genres=genres,
                           results=results, stats=stats, filters=filters)


if __name__ == "__main__":
    app.run(debug=True)
