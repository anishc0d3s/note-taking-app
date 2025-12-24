from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for Android app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.json
    note = Note(
        title=data.get('title', 'Untitled'),
        content=data.get('content', '')
    )
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.json
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    note.timestamp = datetime.utcnow()
    db.session.commit()
    return jsonify(note.to_dict())

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
