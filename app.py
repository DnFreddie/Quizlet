from flask import Flask,  render_template, request, redirect 
import sqlite3

app = Flask(__name__)

# SQLite database configuration
DATABASE = 'quizlet.db'

# Connect to the SQLite database
def get_db():
    db = sqlite3.connect(DATABASE)
    return db

@app.route('/', methods=['GET', 'POST'])
def display_data():
    if request.method == 'POST':
 # redirect to the '/quizlet' route
        return redirect('/quizlet') 
    # If somthing does not work 
    # Redirect user to Eror 404 site 
    try:
        db = get_db()
        cursor = db.execute('SELECT * FROM vocab;')
        data = cursor.fetchall()
        return render_template('table.html', rows=data)
    except:
        return render_template('error.html')

# Just a edit template 
@app.route('/quizlet', methods=['GET', 'POST'])
def editable_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM vocab")
    rows = cursor.fetchall()
   
    return render_template('edit_table.html', rows=rows)

# Modyfie and add new words 
# Click applaies the changes 
@app.route('/save-table', methods=['POST'])
def save_table():
    # Get the updated values from the form
    updated_ids = request.form.getlist('column1[]')
    updated_column2 = request.form.getlist('column2[]')
    updated_column3 = request.form.getlist('column3[]')
    db = get_db()
    cursor = db.cursor()
    # Applay changes to words 
    for i in range(len(updated_ids)):
        query = "UPDATE vocab SET word = ?, translation = ? WHERE id = ?"
        values = (updated_column2[i], updated_column3[i], updated_ids[i])
        cursor.execute(query, values)
    column2_values = request.form.getlist('column4[]')
    column3_values = request.form.getlist('column5[]')
    # Add the word if input not  empty 
    if column2_values[0] and column3_values[0] != '':
        cursor.execute("INSERT INTO vocab  (word ,translation) VALUES (?, ?)",
               (column2_values[0], column3_values[0]))
    db.commit()
    return redirect('/quizlet')



@app.route('/delete-row', methods=['POST'])
def delete_row():
    db = get_db()
    cursor = db.cursor()
    deleted_row_data = request.get_json()
    # Remove the row from the database
    word = deleted_row_data['column1']
    translation = deleted_row_data['column2']
    cursor.execute('DELETE FROM vocab WHERE word = ? and translation = ?', (word, translation))
    db.commit()
    return 'Row deleted successfully'



if __name__ == '__main__':
    app.run()

