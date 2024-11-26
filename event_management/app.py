from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'sabari'

# Configure MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tamil_2005'
app.config['MYSQL_DB'] = 'event_management'

mysql = MySQL(app)

# Home page route
@app.route('/')
def home():
    return render_template('home.html')

# Events page route (with search functionality)
@app.route('/events', methods=['GET', 'POST'])
def events():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        search_query = request.form['search']
        cur.execute("SELECT * FROM events WHERE title LIKE %s", ('%' + search_query + '%',))
    else:
        cur.execute("SELECT * FROM events")

    events = cur.fetchall()
    return render_template('events.html', events=events)

# Add Event page route
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO events (title, description, date) VALUES (%s, %s, %s)", (title, description, date))
        mysql.connection.commit()
        flash('Event Added Successfully!', 'success')
        return redirect(url_for('events'))

    return render_template('add_event.html')

# Edit Event route
@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']

        cur.execute('UPDATE events SET title = %s, description = %s, date = %s WHERE id = %s',
                    (title, description, date, event_id))
        mysql.connection.commit()
        flash('Event Updated Successfully!', 'success')
        return redirect(url_for('events'))

    cur.execute('SELECT * FROM events WHERE id = %s', (event_id,))
    event = cur.fetchone()
    return render_template('edit_event.html', event=event)

# Delete Event route
@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM events WHERE id = %s', (event_id,))
    mysql.connection.commit()
    flash('Event Deleted Successfully!', 'success')
    return redirect(url_for('events'))

if __name__ == '__main__':
    app.run(debug=True)
