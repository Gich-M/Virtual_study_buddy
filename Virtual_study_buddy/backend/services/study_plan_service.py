from flask import jsonify
from models import db, StudyPlan, StudyMaterial, StudySession, Reminder
from sqlalchemy.exc import SQLAlchemyError

def create_study_plan(data):
    try:
        new_study_plan = StudyPlan(
            title=data['title'],
            description=data['description'],
            tags=data.get('tags', None),
            attachments=data.get('attachments', None),
            comments=data.get('comments', None),
            priority=data.get('priority', 1),
            progress=data.get('progress', 0),
            due_date=data.get('due_date', None),
            owner_id=data['owner_id']
        )
        db.session.add(new_study_plan)
        db.session.commit()
        return jsonify({'message': 'StudyPlan created successfully', 'study_plan': str(new_study_plan)}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_study_plan_by_id(study_plan_id):
    study_plan = StudyPlan.query.get(study_plan_id)
    if study_plan:
        return jsonify({'study_plan': str(study_plan)}), 200
    else:
        return jsonify({'message': 'StudyPlan not found'}), 404

def update_study_plan(study_plan_id, data):
    study_plan = StudyPlan.query.get(study_plan_id)
    if study_plan:
        try:
            for key, value in data.items():
                setattr(study_plan, key, value)
            db.session.commit()
            return jsonify({'message': 'StudyPlan updated successfully', 'study_plan': str(study_plan)}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'StudyPlan not found'}), 404

def delete_study_plan(study_plan_id):
    study_plan = StudyPlan.query.get(study_plan_id)
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

def create_study_material(data):
    try:
        new_study_material = StudyMaterial(
            title=data['title'],
            description=data['description'],
            link=data['link'],
            tags=data.get('tags', None),
            attachments=data.get('attachments', None),
            comments=data.get('comments', None),
            priority=data.get('priority', 1),
            progress=data.get('progress', 0),
            due_date=data.get('due_date', None),
            owner_id=data['owner_id']
        )
        db.session.add(new_study_material)
        db.session.commit()
        return jsonify({'message': 'StudyMaterial created successfully', 'study_material': str(new_study_material)}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_study_material_by_id(study_material_id):
    study_material = StudyMaterial.query.get(study_material_id)
    if study_material:
        return jsonify({'study_material': str(study_material)}), 200
    else:
        return jsonify({'message': 'StudyMaterial not found'}), 404

def update_study_material(study_material_id, data):
    study_material = StudyMaterial.query.get(study_material_id)
    if study_material:
        try:
            for key, value in data.items():
                setattr(study_material, key, value)
            db.session.commit()
            return jsonify({'message': 'StudyMaterial updated successfully', 'study_material': str(study_material)}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'StudyMaterial not found'}), 404

def delete_study_material(study_material_id):
    study_material = StudyMaterial.query.get(study_material_id)
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

def create_study_session(data):
    try:
        new_study_session = StudySession(
            title=data['title'],
            description=data['description'],
            tags=data.get('tags', None),
            attachments=data.get('attachments', None),
            comments=data.get('comments', None),
            priority=data.get('priority', 1),
            progress=data.get('progress', 0),
            due_date=data.get('due_date', None),
            owner_id=data['owner_id'],
            study_plan_id=data['study_plan_id']
        )
        db.session.add(new_study_session)
        db.session.commit()
        return jsonify({'message': 'StudySession created successfully', 'study_session': str(new_study_session)}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_study_session_by_id(study_session_id):
    study_session = StudySession.query.get(study_session_id)
    if study_session:
        return jsonify({'study_session': str(study_session)}), 200
    else:
        return jsonify({'message': 'StudySession not found'}), 404

def update_study_session(study_session_id, data):
    study_session = StudySession.query.get(study_session_id)
    if study_session:
        try:
            for key, value in data.items():
                setattr(study_session, key, value)
            db.session.commit()
            return jsonify({'message': 'StudySession updated successfully', 'study_session': str(study_session)}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'StudySession not found'}), 404 
    
def delete_study_session(study_session_id):
    study_session = StudySession.query.get(study_session_id)
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

def create_reminder(data):
    try:
        new_reminder = Reminder(
            title=data['title'],
            description=data['description'],
            reminder_time=data['reminder_time'],
            tags=data.get('tags', None),
            attachments=data.get('attachments', None),
            comments=data.get('comments', None),
            priority=data.get('priority', 1),
            progress=data.get('progress', 0),
            due_date=data.get('due_date', None),
            owner_id=data['owner_id']
        )
        db.session.add(new_reminder)
        db.session.commit()
        return jsonify({'message': 'Reminder created successfully', 'reminder': str(new_reminder)}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_reminder_by_id(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if reminder:
        return jsonify({'reminder': str(reminder)}), 200
    else:
        return jsonify({'message': 'Reminder not found'}), 404

def update_reminder(reminder_id, data):
    reminder = Reminder.query.get(reminder_id)
    if reminder:
        try:
            for key, value in data.items():
                setattr(reminder, key, value)
            db.session.commit()
            return jsonify({'message': 'Reminder updated successfully', 'reminder': str(reminder)}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Reminder not found'}), 404

def delete_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
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
