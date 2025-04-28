from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # مفتاح التشفير للجلسة

# وظيفة لمساعدتنا في التعامل مع قاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect('task_manager.db')
    conn.row_factory = sqlite3.Row
    return conn

# الصفحة الرئيسية (تسجيل الدخول)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # conn = get_db_connection()
        # user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        # conn.close()

        if username == 'admin' and password == 'password':
            session['user_id'] = password
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')

# # صفحة إنشاء حساب
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         hashed_password = generate_password_hash(password)

#         conn = get_db_connection()
#         try:
#             conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
#             conn.commit()
#             conn.close()
#             flash('Account created successfully! Please log in.', 'success')
#             return redirect(url_for('login'))
#         except sqlite3.IntegrityError:
#             flash('Username already exists!', 'danger')

#     return render_template('register.html')

# صفحة لوحة التحكم
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')


@app.route('/requested_cars', methods=['GET', 'POST'])
def requested_cars():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM requested_cars').fetchall()
    conn.close()
    session['rows'] = len(rows)
    return render_template('requested_cars.html', rows=rows)


@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    if request.method == 'POST':
        phone = request.form['phone']
        client_name = request.form['client-name']
        car_num = request.form['car-num']
        car_model = request.form['car-model']
        car_location = request.form['car-location']
        car_color = request.form['car-color']
        conn.execute('INSERT INTO current_cars (phone, client_name, car_number, car_model, location, car_color) VALUES (?, ?, ?, ?, ?, ?)',
                    (phone, client_name, car_num, car_model, car_location, car_color))
        conn.execute('INSERT INTO history (phone, client_name, car_number, car_model, location, car_color) VALUES (?, ?, ?, ?, ?, ?)',
                    (phone, client_name, car_num, car_model, car_location, car_color))
        conn.commit()
        

    return render_template('add_car.html')


@app.route('/current_cars', methods=['GET', 'POST'])
def current_cars():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM current_cars').fetchall()
    conn.close()
    return render_template('current_cars.html', rows=rows)


@app.route('/history', methods=['GET', 'POST'])
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    rows2 = conn.execute('SELECT * FROM history').fetchall()
    conn.close()
    return render_template('history.html', rows=rows2)


# حذف المهام
@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM current_cars WHERE phone = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('current_cars'))



@app.route('/out/<int:task_id>')
def out(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM requested_cars WHERE phone = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('requested_cars'))

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
