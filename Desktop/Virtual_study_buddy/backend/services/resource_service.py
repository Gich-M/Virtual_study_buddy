from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, StudyPlan, StudyMaterial, StudySession, Reminder
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
api = Api(app)

class UserService(Resource):
    def get(self):
        users = User.query.all()
        user_dicts = [user.to_dict() for user in users]
        return user_dicts, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        try:
            user = User(
                username=args['username'],
                email=args['email'],
                password=args['password']
            )
            db.session.add(user)
            db.session.commit()
            return user.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def get_by_id(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.to_dict(), 200
        else:
            return {'message': 'User not found'}, 404

    def put_by_id(self, user_id):
        user = User.query.get(user_id)
        if user:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()
            try:
                for key, value in args.items():
                    setattr(user, key, value)
                db.session.commit()
                return user.to_dict(), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'User not found'}, 404

    def delete_by_id(self, user_id):
        user = User.query.get(user_id)
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                return {'message': 'User deleted successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'User not found'}, 404

class StudyPlanService(Resource):
    def get(self):
        user_id = get_jwt_identity()
        study_plans = StudyPlan.query.filter_by(owner_id=user_id).all()
        study_plan_dicts = [study_plan.to_dict() for study_plan in study_plans]
        return study_plan_dicts, 200

    def post(self):
        user_id = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        args = parser.parse_args()
        try:
            new_study_plan = StudyPlan(
                title=args['title'],
                description=args['description'],
                owner_id=user_id
            )
            db.session.add(new_study_plan)
            db.session.commit()
            return new_study_plan.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def get_by_id(self, study_plan_id):
        user_id = get_jwt_identity()
        study_plan = StudyPlan.query.filter_by(id=study_plan_id, owner_id=user_id).first()
        if study_plan:
            return study_plan.to_dict(), 200
        else:
            return {'message': 'StudyPlan not found'}, 404

    def put_by_id(self, study_plan_id):
        user_id = get_jwt_identity()
        study_plan = StudyPlan.query.filter_by(id=study_plan_id, owner_id=user_id).first()
        if study_plan:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str)
            parser.add_argument('description', type=str)
            args = parser.parse_args()
            try:
                for key, value in args.items():
                    setattr(study_plan, key, value)
                db.session.commit()
                return study_plan.to_dict(), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'StudyPlan not found'}, 404
        
    
    def delete_by_id(self, study_plan_id):
        user_id = get_jwt_identity()
        study_plan = StudyPlan.query.filter_by(id=study_plan_id, owner_id=user_id).first()
        if study_plan:
            try:
                db.session.delete(study_plan)
                db.session.commit()
                return {'message': 'StudyPlan deleted successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'StudyPlan not found'}, 404
        
class StudyMaterialService(Resource):
    def get(self):
        user_id = get_jwt_identity()
        study_materials = StudyMaterial.query.filter_by(owner_id=user_id).all()
        study_material_dicts = [study_material.to_dict() for study_material in study_materials]
        return study_material_dicts, 200
    
    def post(self):
        user_id = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        args = parser.parse_args()
        try:
            new_study_material = StudyMaterial(
                title=args['title'],
                description=args['description'],
                owner_id=user_id
            )
            db.session.add(new_study_material)
            db.session.commit()
            return new_study_material.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    
    def get_by_id(self, study_material_id):
        user_id = get_jwt_identity()
        study_material = StudyMaterial.query.filter_by(id=study_material_id, owner_id=user_id).first()
        if study_material:
            return study_material.to_dict(), 200
        else:
            return {'message': 'StudyMaterial not found'}, 404
        
    
    def put_by_id(self, study_material_id):
        user_id = get_jwt_identity()
        study_material = StudyMaterial.query.filter_by(id=study_material_id, owner_id=user_id).first()
        if study_material:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str)
            parser.add_argument('description', type=str)
            args = parser.parse_args()
            try:
                for key, value in args.items():
                    setattr(study_material, key, value)
                db.session.commit()
                return study_material.to_dict(), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'StudyMaterial not found'}, 404
        
    def delete_by_id(self, study_material_id):
        user_id = get_jwt_identity()
        study_material = StudyMaterial.query.filter_by(id=study_material_id, owner_id=user_id).first()
        if study_material:
            try:
                db.session.delete(study_material)
                db.session.commit()
                return {'message': 'StudyMaterial deleted successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'StudyMaterial not found'}, 404

class StudySessionService(Resource):
    def get(self):
        user_id = get_jwt_identity()
        study_sessions = StudySession.query.filter_by(owner_id=user_id).all()
        study_session_dicts = [study_session.to_dict() for study_session in study_sessions]
        return study_session_dicts, 200
    
    def post(self):
        user_id = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        args = parser.parse_args()
        try:
            new_study_session = StudySession(
                title=args['title'],
                description=args['description'],
                owner_id=user_id
            )
            db.session.add(new_study_session)
            db.session.commit()
            return new_study_session.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500
        
    def get_by_id(self, study_session_id):
        user_id = get_jwt_identity()
        study_session = StudySession.query.filter_by(id=study_session_id, owner_id=user_id).first()
        if study_session:
            return study_session.to_dict(), 200
        else:
            return {'message': 'StudySession not found'}, 404
        
    def put_by_id(self, study_session_id):
        user_id = get_jwt_identity()
        study_session = StudySession.query.filter_by(id=study_session_id, owner_id=user_id).first()
        if study_session:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str)
            parser.add_argument('description', type=str)
            args = parser.parse_args()
            try:
                for key, value in args.items():
                    setattr(study_session, key, value)
                db.session.commit()
                return study_session.to_dict(), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'StudySession not found'}, 404
    
    def delete_by_id(self, study_session_id):
        user_id = get_jwt_identity()
        study_session = StudySession.query.filter_by(id=study_session_id, owner_id=user_id).first()
        if study_session:
            try:
                db.session.delete(study_session)
                db.session.commit()
                return {'message': 'StudySession deleted successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'StudySession not found'}, 404

class ReminderService(Resource):
    def get(self):
        user_id = get_jwt_identity()
        reminders = Reminder.query.filter_by(owner_id=user_id).all()
        reminder_dicts = [reminder.to_dict() for reminder in reminders]
        return reminder_dicts, 200

    def post(self):
        user_id = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        args = parser.parse_args()
        try:
            new_reminder = Reminder(
                title=args['title'],
                description=args['description'],
                owner_id=user_id
            )
            db.session.add(new_reminder)
            db.session.commit()
            return new_reminder.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def get_by_id(self, reminder_id):
        user_id = get_jwt_identity()
        reminder = Reminder.query.filter_by(id=reminder_id, owner_id=user_id).first()
        if reminder:
            return reminder.to_dict(), 200
        else:
            return {'message': 'Reminder not found'}, 404

    def put_by_id(self, reminder_id):
        user_id = get_jwt_identity()
        reminder = Reminder.query.filter_by(id=reminder_id, owner_id=user_id).first()
        if reminder:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str)
            parser.add_argument('description', type=str)
            args = parser.parse_args()
            try:
                for key, value in args.items():
                    setattr(reminder, key, value)
                db.session.commit()
                return reminder.to_dict(), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'Reminder not found'}, 404

    def delete_by_id(self, reminder_id):
        user_id = get_jwt_identity()
        reminder = Reminder.query.filter_by(id=reminder_id, owner_id=user_id).first()
        if reminder:
            try:
                db.session.delete(reminder)
                db.session.commit()
                return {'message': 'Reminder deleted successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'Reminder not found'}, 404

api.add_resource(UserService, '/users')
api.add_resource(StudyPlanService, '/study-plans')
api.add_resource(StudyMaterialService, '/study-materials')
api.add_resource(StudySessionService, '/study-sessions')
api.add_resource(ReminderService, '/reminders')

if __name__ == '__main__':
    app.run(debug=True)
