from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, StudyPlan, StudyMaterial, StudySession, Reminder
from sqlalchemy.exc import SQLAlchemyError

study_plan_blueprint = Blueprint('study_plan', __name__)


@study_plan_blueprint.route('/study_plans', methods=['GET'])
@jwt_required()
def get_study_plans():
    user_id = get_jwt_identity()
    study_plans = StudyPlan.query.filter_by(owner_id=user_id).all()
    if study_plans:
        study_plan_dicts = [study_plan.to_dict() for study_plan in study_plans]
        return jsonify({'study_plans': study_plan_dicts}), 200
    else:
        return jsonify({'message': 'No study plans found'}), 200

@study_plan_blueprint.route('/study_plans', methods=['POST'])
@jwt_required()
def create_study_plan():
    user_id = get_jwt_identity()
    data = request.get_json()
    if data and 'title' in data and 'description' in data:
        try:
            new_study_plan = StudyPlan(
                title=data['title'],
                description=data['description'],
                tags=data.get('tags'),
                attachments=data.get('attachments'),
                comments=data.get('comments'),
                priority=data.get('priority', 1),
                progress=data.get('progress', 0),
                due_date=data.get('due_date'),
                owner_id=user_id
            )
            db.session.add(new_study_plan)
            db.session.commit()
            return jsonify({'message': 'StudyPlan created successfully', 'study_plan': new_study_plan.to_dict()}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Title and description are required'}), 400

@study_plan_blueprint.route('/study_plans/<int:study_plan_id>', methods=['GET'])
@jwt_required()
def get_study_plan_by_id(study_plan_id):
    user_id = get_jwt_identity()
    study_plan = StudyPlan.query.filter_by(id=study_plan_id, owner_id=user_id).first()
    if study_plan:
        return jsonify({'study_plan': study_plan.to_dict()}), 200
    else:
        return jsonify({'message': 'StudyPlan not found'}), 404

@study_plan_blueprint.route('/study_plans/<int:study_plan_id>', methods=['PUT'])
@jwt_required()
def update_study_plan(study_plan_id):
    user_id = get_jwt_identity()
    study_plan = StudyPlan.query.filter_by(id=study_plan_id, owner_id=user_id).first()
    if study_plan:
        data = request.get_json()
        if data:
            try:
                for key, value in data.items():
                    setattr(study_plan, key, value)
                db.session.commit()
                return jsonify({'message': 'StudyPlan updated successfully', 'study_plan': study_plan.to_dict()}), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'message': 'Invalid request'}), 400
    else:
        return jsonify({'message': 'StudyPlan not found'}), 404

@study_plan_blueprint.route('/study_plans/<int:study_plan_id>', methods=['DELETE'])
@jwt_required()
def delete_study_plan(study_plan_id):
    user_id = get_jwt_identity()
    study_plan = StudyPlan.query.filter_by(id=study_plan_id, owner_id=user_id).first()
    if study_plan:
        try:
            db.session.delete(study_plan)
            db.session.commit()
            return jsonify({'message': 'StudyPlan deleted successfully'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'StudyPlan not found'}), 404

@study_plan_blueprint.route('/study_materials', methods=['GET'])
@jwt_required()
def get_study_materials():
    user_id = get_jwt_identity()
    study_materials = StudyMaterial.query.filter_by(owner_id=user_id).all()
    if study_materials:
        study_material_dicts = [study_material.to_dict() for study_material in study_materials]
        return jsonify({'study_materials': study_material_dicts}), 200
    else:
        return jsonify({'message': 'No study materials found'}), 200

@study_plan_blueprint.route('/study_materials', methods=['POST'])
@jwt_required()
def create_study_material():
    user_id = get_jwt_identity()
    data = request.get_json()
    if data and 'title' in data and 'description' in data:
        try:
            new_study_material = StudyMaterial(
                title=data['title'],
                description=data['description'],
                tags=data.get('tags'),
                attachments=data.get('attachments'),
                comments=data.get('comments'),
                priority=data.get('priority', 1),
                progress=data.get('progress', 0),
                due_date=data.get('due_date'),
                owner_id=user_id
            )
            db.session.add(new_study_material)
            db.session.commit()
            return jsonify({'message': 'StudyMaterial created successfully', 'study_material': new_study_material.to_dict()}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Title and description are required'}), 400

@study_plan_blueprint.route('/study_materials/<int:study_material_id>', methods=['GET'])
@jwt_required()
def get_study_material_by_id(study_material_id):
    user_id = get_jwt_identity()
    study_material = StudyMaterial.query.filter_by(id=study_material_id, owner_id=user_id).first()
    if study_material:
        return jsonify({'study_material': study_material.to_dict()}), 200
    else:
        return jsonify({'message': 'StudyMaterial not found'}), 404

@study_plan_blueprint.route('/study_materials/<int:study_material_id>', methods=['PUT'])
@jwt_required()
def update_study_material(study_material_id):
    user_id = get_jwt_identity()
    study_material = StudyMaterial.query.filter_by(id=study_material_id, owner_id=user_id).first()
    if study_material:
        data = request.get_json()
        if data:
            try:
                for key, value in data.items():
                    setattr(study_material, key, value)
                db.session.commit()
                return jsonify({'message': 'StudyMaterial updated successfully', 'study_material': study_material.to_dict()}), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'message': 'Invalid request'}), 400
    else:
        return jsonify({'message': 'StudyMaterial not found'}), 404

@study_plan_blueprint.route('/study_materials/<int:study_material_id>', methods=['DELETE'])
@jwt_required()
def delete_study_material(study_material_id):
    user_id = get_jwt_identity()
    study_material = StudyMaterial.query.filter_by(id=study_material_id, owner_id=user_id).first()
    if study_material:
        try:
            db.session.delete(study_material)
            db.session.commit()
            return jsonify({'message': 'StudyMaterial deleted successfully'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'StudyMaterial not found'}), 404

@study_plan_blueprint.route('/study_sessions', methods=['GET'])
@jwt_required()
def get_study_sessions():
    user_id = get_jwt_identity()
    study_sessions = StudySession.query.filter_by(owner_id=user_id).all()
    if study_sessions:
        study_session_dicts = [study_session.to_dict() for study_session in study_sessions]
        return jsonify({'study_sessions': study_session_dicts}), 200
    else:
        return jsonify({'message': 'No study sessions found'}), 200

@study_plan_blueprint.route('/study_sessions', methods=['POST'])
@jwt_required()
def create_study_session():
    user_id = get_jwt_identity()
    data = request.get_json()
    if data and 'title' in data and 'date' in data:
        try:
            new_study_session = StudySession(
                title=data['title'],
                date=data['date'],
                duration=data.get('duration'),
                description=data.get('description'),
                attachments=data.get('attachments'),
                comments=data.get('comments'),
                owner_id=user_id
            )
            db.session.add(new_study_session)
            db.session.commit()
            return jsonify({'message': 'StudySession created successfully', 'study_session': new_study_session.to_dict()}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Title and date are required'}), 400

@study_plan_blueprint.route('/study_sessions/<int:study_session_id>', methods=['GET'])
@jwt_required()
def get_study_session_by_id(study_session_id):
    user_id = get_jwt_identity()
    study_session = StudySession.query.filter_by(id=study_session_id, owner_id=user_id).first()
    if study_session:
        return jsonify({'study_session': study_session.to_dict()}), 200
    else:
        return jsonify({'message': 'StudySession not found'}), 404

@study_plan_blueprint.route('/study_sessions/<int:study_session_id>', methods=['PUT'])
@jwt_required()
def update_study_session(study_session_id):
    user_id = get_jwt_identity()
    study_session = StudySession.query.filter_by(id=study_session_id, owner_id=user_id).first()
    if study_session:
        data = request.get_json()
        if data:
            try:
                for key, value in data.items():
                    setattr(study_session, key, value)
                db.session.commit()
                return jsonify({'message': 'StudySession updated successfully', 'study_session': study_session.to_dict()}), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'message': 'Invalid request'}), 400
    else:
        return jsonify({'message': 'StudySession not found'}), 404

@study_plan_blueprint.route('/study_sessions/<int:study_session_id>', methods=['DELETE'])
@jwt_required()
def delete_study_session(study_session_id):
    user_id = get_jwt_identity()
    study_session = StudySession.query.filter_by(id=study_session_id, owner_id=user_id).first()
    if study_session:
        try:
            db.session.delete(study_session)
            db.session.commit()
            return jsonify({'message': 'StudySession deleted successfully'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'StudySession not found'}), 404

@study_plan_blueprint.route('/reminders', methods=['GET'])
@jwt_required()
def get_reminders():
    user_id = get_jwt_identity()
    reminders = Reminder.query.filter_by(owner_id=user_id).all()
    if reminders:
        reminder_dicts = [reminder.to_dict() for reminder in reminders]
        return jsonify({'reminders': reminder_dicts}), 200
    else:
        return jsonify({'message': 'No reminders found'}), 200

@study_plan_blueprint.route('/reminders', methods=['POST'])
@jwt_required()
def create_reminder():
    user_id = get_jwt_identity()
    data = request.get_json()
    if data and 'title' in data and 'date' in data:
        try:
            new_reminder = Reminder(
                title=data['title'],
                date=data['date'],
                description=data.get('description'),
                owner_id=user_id
            )
            db.session.add(new_reminder)
            db.session.commit()
            return jsonify({'message': 'Reminder created successfully', 'reminder': new_reminder.to_dict()}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Title and date are required'}), 400

@study_plan_blueprint.route('/reminders/<int:reminder_id>', methods=['GET'])
@jwt_required()
def get_reminder_by_id(reminder_id):
    user_id = get_jwt_identity()
    reminder = Reminder.query.filter_by(id=reminder_id, owner_id=user_id).first()
    if reminder:
        return jsonify({'reminder': reminder.to_dict()}), 200
    else:
        return jsonify({'message': 'Reminder not found'}), 404

@study_plan_blueprint.route('/reminders/<int:reminder_id>', methods=['PUT'])
@jwt_required()
def update_reminder(reminder_id):
    user_id = get_jwt_identity()
    reminder = Reminder.query.filter_by(id=reminder_id, owner_id=user_id).first()
    if reminder:
        data = request.get_json()
        if data:
            try:
                for key, value in data.items():
                    setattr(reminder, key, value)
                db.session.commit()
                return jsonify({'message': 'Reminder updated successfully', 'reminder': reminder.to_dict()}), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'message': 'Invalid request'}), 400
    else:
        return jsonify({'message': 'Reminder not found'}), 404

@study_plan_blueprint.route('/reminders/<int:reminder_id>', methods=['DELETE'])
@jwt_required()
def delete_reminder(reminder_id):
    user_id = get_jwt_identity()
    reminder = Reminder.query.filter_by(id=reminder_id, owner_id=user_id).first()
    if reminder:
        try:
            db.session.delete(reminder)
            db.session.commit()
            return jsonify({'message': 'Reminder deleted successfully'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Reminder not found'}), 404

        
