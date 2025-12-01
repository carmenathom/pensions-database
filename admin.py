from flask import Blueprint, render_template, request, redirect, url_for, session
from models import get_all_users, get_user_by_id, update_user
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "role" not in session or session["role"] != "Admin":
            return "Unauthorized", 403
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route('/users')
@admin_required
def users_list():
    users = get_all_users()
    return render_template('admin_users.html', users=users)


@admin_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = get_user_by_id(user_id)

    if not user:
        return "User not found", 404

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        name = request.form['name']

        update_user(user_id, username, email, role, name)

        return redirect(url_for('admin.users_list'))

    return render_template('edit_user.html', user=user)
