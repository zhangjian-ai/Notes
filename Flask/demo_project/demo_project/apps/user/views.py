from flask import Blueprint

user = Blueprint(name="user",
                 import_name=__name__,
                 static_folder="static",
                 template_folder="templates",
                 static_url_path="static",
                 url_prefix="/user/")


@user.route("/", methods=["GET"])
def user_index():
    return "用户首页"


@user.route("logon/", methods=["GET"])
def user_logon():
    return "用户注册"
