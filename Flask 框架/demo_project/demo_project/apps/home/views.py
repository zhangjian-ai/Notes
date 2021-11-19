from flask import Blueprint

home = Blueprint(name="home",
                 import_name=__name__,
                 static_folder="static",
                 template_folder="templates",
                 static_url_path="static",
                 url_prefix="/")


@home.route("/", methods=["GET"])
def user_index():
    return "网站首页"
