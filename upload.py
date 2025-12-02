from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import os
from models import insert_document, mark_document_processed
from text_processing import process_pdf_for_faiss
from functools import wraps

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

UPLOAD_FOLDER = "uploads"   
ALLOWED_EXT = {'pdf'}


def curator_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "role" not in session or session["role"] != "Curator":
            return "Unauthorized", 403
        return f(*args, **kwargs)
    return wrapper


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


# --- Upload form ---
@upload_bp.route('', methods=['GET'])
@curator_required
def upload_page():
    return render_template('upload.html')


# --- Upload submit ---
@upload_bp.route('', methods=['POST'])
@curator_required
def upload_document():

    title = request.form['title']
    doc_type = request.form['doc_type']
    source = request.form['source']
    user_id = session.get("user_id")

    file = request.files['pdf']

    if not file or file.filename == '':
        return "No file uploaded", 400

    if not allowed_file(file.filename):
        return "Only PDF files allowed", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file.save(filepath)

    doc_id = insert_document(title, doc_type, source, user_id, filename)

    num_chunks = process_pdf_for_faiss(doc_id, filepath)

    mark_document_processed(doc_id)

    return redirect(url_for('upload.upload_page'))

def process_document(filepath):
    print("Hi")