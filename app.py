from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL
from config import Config
from auth import token_required, generate_token
from utils import format_response, parse_xml_request, xml_response
import MySQLdb.cursors
import json

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'football_ui_secret'
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return jsonify({'token': generate_token()})

@app.route('/players', methods=['POST'])
@token_required
def create_player():
    format_type = request.args.get('format', 'json')
    if request.is_json:
        data = request.json
    elif request.content_type and 'xml' in request.content_type:
        data = parse_xml_request(request.data.decode('utf-8'))
        if not data:
            return xml_response('Invalid XML', 400) if format_type == 'xml' else jsonify({'error': 'Invalid XML'}), 400
    else:
        data = request.json
    
    required = ['name', 'club', 'position', 'goals', 'assists', 'appearances']
    if not all(k in data for k in required):
        msg = {'error': 'Missing fields'}
        return xml_response('Missing fields', 400) if format_type == 'xml' else (jsonify(msg), 400)
    try:
        name = str(data.get('name', '')).strip()
        club = str(data.get('club', '')).strip()
        position = str(data.get('position', '')).strip()
        goals = int(data.get('goals'))
        assists = int(data.get('assists'))
        appearances = int(data.get('appearances'))
    except Exception:
        return xml_response('Invalid field types', 400) if format_type == 'xml' else (jsonify({'error': 'Invalid field types'}), 400)

    if not name or not club or not position or goals < 0 or assists < 0 or appearances < 0:
        return xml_response('Invalid field values', 400) if format_type == 'xml' else (jsonify({'error': 'Invalid field values'}), 400)

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO players (name, club, position, goals, assists, appearances)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, club, position, goals, assists, appearances))
        mysql.connection.commit()
        player_id = cur.lastrowid
        cur.close()

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM players WHERE id=%s", (player_id,))
        player_data = cur.fetchone()
        cur.close()

        if format_type == 'xml':
            return xml_response('Player added', 201, player_data)
        return jsonify(player_data), 201
    except Exception:
        return xml_response('Database error', 500) if format_type == 'xml' else (jsonify({'error': 'Database error'}), 500)

@app.route('/players', methods=['GET'])
def get_players():
    club = request.args.get('club')
    min_goals = request.args.get('min_goals')
    format_type = request.args.get('format', 'json')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if club:
        cur.execute("SELECT * FROM players WHERE club=%s", (club,))
    elif min_goals:
        cur.execute("SELECT * FROM players WHERE goals >= %s", (min_goals,))
    else:
        cur.execute("SELECT * FROM players")

    data = cur.fetchall()
    return format_response(data, format_type)

@app.route('/players/<int:id>', methods=['PUT'])
@token_required
def update_player(id):
    format_type = request.args.get('format', 'json')
    if request.is_json:
        data = request.json
    elif request.content_type and 'xml' in request.content_type:
        data = parse_xml_request(request.data.decode('utf-8'))
        if not data:
            return xml_response('Invalid XML', 400) if format_type == 'xml' else (jsonify({'error': 'Invalid XML'}), 400)
    else:
        data = request.json
    update_fields = []
    update_values = []
    
    for field in ['name', 'club', 'position', 'goals', 'assists', 'appearances']:
        if field in data:
            update_fields.append(f"{field}=%s")
            update_values.append(data[field])
    
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    
    update_values.append(id)
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(f"UPDATE players SET {', '.join(update_fields)} WHERE id=%s", update_values)
    mysql.connection.commit()
    cur.execute("SELECT * FROM players WHERE id=%s", (id,))
    updated = cur.fetchone()
    cur.close()
    
    if format_type == 'xml':
        return xml_response('Player updated', 200, updated)
    return jsonify(updated), 200

@app.route('/players/<int:id>', methods=['DELETE'])
@token_required
def delete_player(id):
    format_type = request.args.get('format', 'json')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM players WHERE id=%s", (id,))
    mysql.connection.commit()
    
    if format_type == 'xml':
        return xml_response('Player deleted')
    return jsonify({'message': 'Player deleted'})

@app.route('/')
def ui_index():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM players")
        players = cur.fetchall()
        cur.close()
        json_data = json.dumps(players, indent=2, default=str)
        xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n<players>\n'
        for p in players:
            xml_str += f'  <player>\n'
            xml_str += f'    <id>{p.get("id", "")}</id>\n'
            xml_str += f'    <name>{p.get("name", "")}</name>\n'
            xml_str += f'    <club>{p.get("club", "")}</club>\n'
            xml_str += f'    <position>{p.get("position", "")}</position>\n'
            xml_str += f'    <goals>{p.get("goals", "")}</goals>\n'
            xml_str += f'    <assists>{p.get("assists", "")}</assists>\n'
            xml_str += f'    <appearances>{p.get("appearances", "")}</appearances>\n'
            xml_str += f'  </player>\n'
        xml_str += '</players>'
        
        return render_template('index.html', players=players, json_data=json_data, xml_data=xml_str)
    except Exception as e:
        return render_template('index.html', players=[], json_data='{}', xml_data='', error=str(e))

@app.route('/create', methods=['GET', 'POST'])
def ui_create():
    if request.method == 'POST':
        try:
            data = request.form
            player_id = data.get('id', '').strip()
            name = str(data.get('name', '')).strip()
            club = str(data.get('club', '')).strip()
            position = str(data.get('position', '')).strip()
            goals = int(data.get('goals', 0))
            assists = int(data.get('assists', 0))
            appearances = int(data.get('appearances', 0))
            
            if not name or not club or not position:
                return render_template('create.html', error='Name, Club, and Position are required')
            
            cur = mysql.connection.cursor()
            if player_id:
                # Insert with specific ID
                cur.execute("""
                    INSERT INTO players (id, name, club, position, goals, assists, appearances)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (int(player_id), name, club, position, goals, assists, appearances))
                created_id = int(player_id)
            else:
                cur.execute("""
                    INSERT INTO players (name, club, position, goals, assists, appearances)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (name, club, position, goals, assists, appearances))
                created_id = cur.lastrowid
            mysql.connection.commit()
            cur.close()
            
            return redirect(url_for('ui_index', message=f'Player created successfully! ID: {created_id}'))
        except Exception as e:
            return render_template('create.html', error=str(e))
    
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def ui_edit(id):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM players WHERE id=%s", (id,))
        player = cur.fetchone()
        cur.close()
        
        if not player:
            return redirect(url_for('ui_index'))
        
        if request.method == 'POST':
            data = request.form
            name = str(data.get('name', '')).strip() or player.get('name')
            club = str(data.get('club', '')).strip() or player.get('club')
            position = str(data.get('position', '')).strip() or player.get('position')
            goals = int(data.get('goals', player.get('goals', 0)))
            assists = int(data.get('assists', player.get('assists', 0)))
            appearances = int(data.get('appearances', player.get('appearances', 0)))
            
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE players SET name=%s, club=%s, position=%s, goals=%s, assists=%s, appearances=%s
                WHERE id=%s
            """, (name, club, position, goals, assists, appearances, id))
            mysql.connection.commit()
            cur.close()
            
            return redirect(url_for('ui_index'))
        
        return render_template('edit.html', player=player)
    except Exception as e:
        return render_template('edit.html', player={}, error=str(e))

@app.route('/delete/<int:id>', methods=['POST'])
def ui_delete(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM players WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        pass
    
    return redirect(url_for('ui_index'))

if __name__ == '__main__':
    app.run(debug=True)
