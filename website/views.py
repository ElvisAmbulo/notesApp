#store all the urls/routes

from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .modals import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Not is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added succesfully!', category='success')

    return render_template('index.html', user = current_user)

from flask import jsonify

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = json.loads(request.data)           # rename variable
    note_id = data.get('note')                # safely get note id
    note_to_delete = Note.query.get(note_id)  # renamed variable

    if note_to_delete:
        if note_to_delete.user_id == current_user.id:
            db.session.delete(note_to_delete)
            db.session.commit()
            return jsonify({'success': True})
    
    return jsonify({'success': False})
