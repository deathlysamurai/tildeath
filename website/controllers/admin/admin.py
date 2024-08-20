from flask import render_template, Blueprint, request
from ...models import ACCESS, User
from ...decorators import requires_access_level
from flask_login import current_user
import datetime

admin = Blueprint('admin', __name__)

@admin.route('/', methods=['GET'])
@requires_access_level(ACCESS['admin'])
def home():
    items = []
    table_columns = []

    return render_template("admin/home.html", table_columns=table_columns, items=items, table_title="Users", user=current_user, page="admin_home")