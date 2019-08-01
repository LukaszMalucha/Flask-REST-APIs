from flask import g
from flask_restful import Resource
from oa import github

from models.user import UserModel


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        """send user to authorization page"""
        return github.authorize(callback="http://localhost:5000/login/github/authorized")


class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        """Take github data and send it to GitHub post request to retrieve user access token"""
        resp = github.authorized_response()
        g.access_token = resp['access_token']  # put access token inside flask_global
        github_user = github.get('user')
        github_username = github_user.data['login']

        user = UserModel.find_by_username(github_username)

        if not user:
            user = UserModel(username=github_username, password=None)
            user.save_to_db()



