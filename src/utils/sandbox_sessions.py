from sqlalchemy.orm import Session
from models import sessions_models
from sqlalchemy.exc import IntegrityError
from models.sessions_models import Sessions

def model_to_dict(model):
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}

# Save or update session and stack name
def save_update_stack_session(db: Session, unique_id: str, stack: str):
    try:
        db_session = db.query(sessions_models.Sessions).filter_by(id=unique_id).first()
        if db_session:
            db_session.stack = stack
        else:
            db_session = sessions_models.Sessions(
                id=unique_id,
                stack=stack
            )
            db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save or update session.")

def update_user_session(db: Session, unique_id: str, user: str):
    db_session = db.query(Sessions).filter(Sessions.id == unique_id).first()
    if db_session:
        db_session.user = user
        db.commit()
        db.refresh(db_session)
        return model_to_dict(db_session)
    else:
        raise ValueError(f"Session with id {unique_id} does not exist")