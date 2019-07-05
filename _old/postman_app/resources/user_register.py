import sqlite3
from flask_restful import Resource
from models.user import UserModel


class UserRegister(Resource):
    
    parser = reqparser.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Cannot be blank"
                        )
                        
    parser.add_argument('password',
                    type=str,
                    required=True,
                    help="Cannot be blank"
                    )                    
    
    def post(self):
        
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': ' user already exists'}, 400
        
        user = UserModel(**data)
        user.save_to_db()
        
        
        return {"message": "User created successfully."}, 201