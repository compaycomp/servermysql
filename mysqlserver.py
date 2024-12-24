from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Конфигурация подключения к базе данных
db_config = {
    'user': 'sql7751532',
    'password': '1E3VW4YZbN',
    'host': 'sql7.freemysqlhosting.net',
    'database': 'sql7751532'
}

def get_db_connection():
    """Создает подключение к базе данных."""
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    """Главная страница."""
    return "Welcome to the Petya schedule app!"

# Эндпоинт для получения расписания преподавателя
@app.route('/teacher_schedule', methods=['GET'])
def get_teacher_schedule():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
        SELECT
            t.FirstName AS teacher_first_name,
            t.LastName AS teacher_last_name,
            g.StudentGroupNumber AS group_number,
            s.SubjectName AS subject_name,
            p.PairID AS pair_id,
            c.CabinetNumber AS cabinet_number
        FROM pair p
        JOIN teachers t ON p.Teachers_TeachersID = t.TeachersID
        JOIN studentgroup g ON p.StudentGroup_StudentGroupID = g.StudentGroupID
        JOIN subject s ON p.Subject_SubjectID = s.SubjectID
        JOIN cabinet c ON p.Cabinet_CabinetID = c.CabinetID
        WHERE t.TeachersID = 1
        ORDER BY p.PairID
    ''')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(rows)

# Эндпоинт для получения расписания группы
@app.route('/group_schedule', methods=['GET'])
def get_group_schedule():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
        SELECT
            g.StudentGroupNumber AS group_number,
            t.FirstName AS teacher_first_name,
            t.LastName AS teacher_last_name,
            s.SubjectName AS subject_name,
            p.PairID AS pair_id,
            c.CabinetNumber AS cabinet_number
        FROM pair p
        JOIN teachers t ON p.Teachers_TeachersID = t.TeachersID
        JOIN studentgroup g ON p.StudentGroup_StudentGroupID = g.StudentGroupID
        JOIN subject s ON p.Subject_SubjectID = s.SubjectID
        JOIN cabinet c ON p.Cabinet_CabinetID = c.CabinetID
        WHERE g.StudentGroupID = 1
        ORDER BY p.PairID
    ''')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(rows)

# Эндпоинт для получения расписания кабинета
@app.route('/room_schedule', methods=['GET'])
def get_room_schedule():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
        SELECT
            c.CabinetNumber AS cabinet_number,
            g.StudentGroupNumber AS group_number,
            t.FirstName AS teacher_first_name,
            t.LastName AS teacher_last_name,
            s.SubjectName AS subject_name,
            p.PairID AS pair_id
        FROM pair p
        JOIN teachers t ON p.Teachers_TeachersID = t.TeachersID
        JOIN studentgroup g ON p.StudentGroup_StudentGroupID = g.StudentGroupID
        JOIN subject s ON p.Subject_SubjectID = s.SubjectID
        JOIN cabinet c ON p.Cabinet_CabinetID = c.CabinetID
        WHERE c.CabinetID = 1
        ORDER BY p.PairID
    ''')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)