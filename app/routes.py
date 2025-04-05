from flask import jsonify
from marshmallow import ValidationError

from app import app, jwt, api

from app.resources.user import UserRegister, UserLogin, UserDetailsResource, \
      UserPasswordUpdateResource, UserDeleteResource
from app.resources.task import TaskResource, TaskDetailsResource
from app.resources.comment import CommentResource
from app.resources.notification import NotificationResource


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserPasswordUpdateResource, "/update-password")
api.add_resource(UserDeleteResource, "/user-delete/<int:user_id>")
api.add_resource(UserDetailsResource, "/user-details/<int:user_id>")
api.add_resource(TaskResource, "/create_task")
api.add_resource(TaskDetailsResource, "/task-details/<int:task_id>")
api.add_resource(CommentResource, "/create_comment")
api.add_resource(NotificationResource, "/create_notification")


@app.route('/')
@app.route('/index')
def index():
    return 'This is my first flask project!!'