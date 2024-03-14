from flask import Flask, Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, StudyPlan, StudyMaterial, StudySession, Reminder
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
resource_blueprint = Blueprint('resource', __name__)
api = Api(resource_blueprint)

class ResourceController(Resource):
    @resource_blueprint.route('/users', methods=['GET', 'POST'])
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        resources = Resource.query.filter_by(owner_id=user_id).all()
        resource_dicts = [resource.to_dict() for resource in resources]
        return resource_dicts, 200
    
    @resource_blueprint.route('/users', methods=['GET', 'POST'])
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        args = parser.parse_args()
        try:
            new_resource = Resource(
                title=args['title'],
                description=args['description'],
                owner_id=user_id
            )
            db.session.add(new_resource)
            db.session.commit()
            return new_resource.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    
    @resource_blueprint.route('/users/<int:resource_id>', methods=['GET'])
    @jwt_required()
    def get_by_id(self, resource_id):
        user_id = get_jwt_identity()
        resource = Resource.query.filter_by(id=resource_id, owner_id=user_id).first()
        if resource:
            return resource.to_dict(), 200
        else:
            return {'message': 'Resource not found'}, 404
        
    @resource_blueprint.route('/users/<int:resource_id>', methods=['PUT'])
    @jwt_required()
    def put_by_id(self, resource_id):
        user_id = get_jwt_identity()
        resource = Resource.query.filter_by(id=resource_id, owner_id=user_id).first()
        if resource:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str)
            parser.add_argument('description', type=str)
            args = parser.parse_args()
            try:
                for key, value in args.items():
                    setattr(resource, key, value)
                db.session.commit()
                return resource.to_dict(), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'Resource not found'}, 404
        
    @resource_blueprint.route('/users/<int:resource_id>', methods=['DELETE'])
    @jwt_required()
    def delete_by_id(self, resource_id):
        user_id = get_jwt_identity()
        resource = Resource.query.filter_by(id=resource_id, owner_id=user_id).first()
        if resource:
            try:
                db.session.delete(resource)
                db.session.commit()
                return {'message': 'Resource deleted successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 500
        else:
            return {'message': 'Resource not found'}, 404

api.add_resource(ResourceController, '/resources')

if __name__ == '__main__':
    app.run(debug=True)
