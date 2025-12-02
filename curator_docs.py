from flask import Blueprint, render_template, request, redirect, session, url_for
from functools import wraps
import os

from models import (
    get_documents_by_user,
    get_document_by_id,
    update_document,
    delete_document_db
)

curator_bp = Blueprint('curator', __name__, url_prefix='/curator')

UPLOAD_FOLDER = "uploads"


def curator_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "role" not in session or session["role"] != "Curator":
            return "Unauthorized", 403
        return f(*args, **kwargs)
    return wrapper


@curator_bp.route('/documents')
@curator_required
def documents_list():
    user_id = session.get("user_id")
    docs = get_documents_by_user(user_id)
    return render_template("curator_documents.html", docs=docs)


@curator_bp.route('/edit/<int:doc_id>', methods=['GET', 'POST'])
@curator_required
def edit_document(doc_id):
    doc = get_document_by_id(doc_id)

    if not doc or doc["added_by"] != session["user_id"]:
        return "Unauthorized", 403

    if request.method == 'POST':
        title = request.form["title"]
        doc_type = request.form["doc_type"]
        source = request.form["source"]

        update_document(doc_id, title, doc_type, source)

        return redirect(url_for('curator.documents_list'))

    return render_template("edit_document.html", doc=doc)


@curator_bp.route('/delete/<int:doc_id>', methods=['POST'])
@curator_required
def delete_document(doc_id):

    doc = get_document_by_id(doc_id)

    if not doc or doc["added_by"] != session["user_id"]:
        return "Unauthorized", 403

    delete_document_db(doc_id)

    return redirect(url_for('curator.documents_list'))

