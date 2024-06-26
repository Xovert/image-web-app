from flask import Blueprint, flash, g, redirect, render_template, url_for, current_app, send_from_directory
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from imgwebapp.auth import login_required
from imgwebapp.db import get_db

import os
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

bp = Blueprint('image', __name__)

photos = UploadSet('photos', IMAGES)

def init_uploads(app):
    configure_uploads(app, photos)

class UploadFileForm(FlaskForm):
    photo = FileField(validators=[
        FileAllowed(photos, 'Only images are allowed!'),
        FileRequired('File upload must not be empty!')
    ])
    submit = SubmitField("Upload")


@bp.route('/gallery')
@login_required
def gallery():
    db = get_db()
    datas = db.execute(
        'SELECT img.id, img_path, user.username'
        ' FROM images img JOIN user ON img.user_id = user.id'
        ' WHERE img.user_id = ?'
        ' ORDER BY img.id DESC',
        (g.user['id'],)
    ).fetchall()
    form = UploadFileForm()
    return render_template('gallery.html', form=form, datas=datas)

@bp.route('/uploads/<filename>', methods=('GET',))
@login_required
def get_file(filename):
    return send_from_directory(os.path.join(current_app.instance_path,current_app.config['UPLOADED_PHOTOS_DEST'],g.user['username']), filename)

@bp.route('/upload', methods=('POST',))
@login_required
def upload_image():
    form = UploadFileForm()
    error = None

    if not form.validate_on_submit():
        error = form.photo.errors[0]
    
    if error is None:
        photo = form.photo.data
        photo.filename = secure_filename(photo.filename)
        dir = os.path.join(current_app.instance_path,current_app.config['UPLOADED_PHOTOS_DEST'],g.user['username'])
        os.makedirs(dir,exist_ok=True)
        filepath = os.path.join(dir, photo.filename)
        photo.save(filepath)
        img_path = url_for('image.get_file', filename=photo.filename)
        db = get_db()
        try:
            db.execute(
                'INSERT INTO images (user_id, img_path, img_name)'
                ' VALUES (?, ?, ?)',
                (g.user['id'], img_path, photo.filename)
            )
            db.commit()
        except db.IntegrityError:
            error = 'File already exists!'
        else:
            flash('Image upload successful!')
            return redirect(url_for('gallery'))

    flash(error)
    return redirect(url_for('gallery'))

def get_image(id, user_id):
    data = get_db().execute(
        'SELECT img.id, img_path, img_name, img.user_id'
        ' FROM images img JOIN user ON img.user_id = user.id'
        ' WHERE img.id = ? AND user.id = ?',
        (id,user_id)
    ).fetchone()
            
    if data is None:
        abort(404, f"Data not found.")
    
    return data['img_name']


@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    filename = get_image(id, g.user['id'])
    db = get_db()
    db.execute('DELETE FROM images WHERE id = ?', (id,))
    db.commit()
    os.remove(os.path.join(current_app.instance_path, current_app.config['UPLOADED_PHOTOS_DEST'], g.user['username'], filename))
    flash('Image successfully deleted!')
    return redirect(url_for('gallery'))

@bp.errorhandler(413)
def request_entity_too_large(error):
    max_size = current_app.config['MAX_CONTENT_LENGTH']
    flash(f'File Cannot Exceed {sizeof_fmt(max_size)}')
    return redirect(url_for('gallery'))

# SIZE CONVERSION, NEED NOT BE TESTED
def sizeof_fmt(num, suffix="B"): # pragma: no cover
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"