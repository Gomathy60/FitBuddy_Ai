from pathlib import Path
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.models import User, WorkoutPlan
from app.schemas import UserInput, FeedbackRequest
from app.services.gemini_generator import generate_workout_gemini
from app.services.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.services.updated_plan import update_workout_plan

r = APIRouter()
t = Jinja2Templates(directory=str(Path(__file__).parent / 'templates'))

# 1. HOME ROUTE
@r.get('/', response_class=HTMLResponse)
def home(request: Request): 
    return t.TemplateResponse(request=request, name='index.html')

@r.get('/api/health')
def health(): 
    return {'status': 'healthy', 'application': settings.APP_NAME}

def get_or_create(d, db):
    u = db.query(User).filter(User.user_id == d.user_id).first()
    if not u: 
        u = User(**d.model_dump())
        db.add(u)
        db.flush()
    else:
        u.name, u.age, u.weight, u.goal, u.intensity = d.name, d.age, d.weight, d.goal, d.intensity
    return u

# 2. GENERATE WORKOUT ROUTE
@r.post('/generate-workout', response_class=HTMLResponse)
def generate(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        d = UserInput(user_id=user_id, name=name, age=age, weight=weight, goal=goal, intensity=intensity)
        u = get_or_create(d, db)
        plan = generate_workout_gemini(name, age, weight, goal, intensity)
        tip = generate_nutrition_tip_with_flash(goal, age, weight)
        p = WorkoutPlan(user_id=u.id, original_plan=plan, nutrition_tip=tip)
        db.add(p)
        db.commit()
        return t.TemplateResponse(
            request=request,
            name='result.html',
            context={'user': u, 'plan': p, 'display_plan': plan, 'is_updated': False}
        )
    except Exception as e:
        db.rollback()
        return t.TemplateResponse(
            request=request,
            name='error.html',
            context={'message': str(e)},
            status_code=500
        )

@r.post('/api/generate-workout')
def generate_api(d: UserInput, db: Session = Depends(get_db)):
    u = get_or_create(d, db)
    plan = generate_workout_gemini(d.name, d.age, d.weight, d.goal, d.intensity)
    tip = generate_nutrition_tip_with_flash(d.goal, d.age, d.weight)
    db.add(WorkoutPlan(user_id=u.id, original_plan=plan, nutrition_tip=tip))
    db.commit()
    return {'user_id': d.user_id, 'workout_plan': plan, 'nutrition_tip': tip}

# 3. SUBMIT FEEDBACK ROUTE
@r.post('/submit-feedback', response_class=HTMLResponse)
def feedback(request: Request, user_id: str = Form(...), feedback: str = Form(...), db: Session = Depends(get_db)):
    u = db.query(User).filter(User.user_id == user_id).first()
    p = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == u.id).order_by(WorkoutPlan.created_at.desc()).first() if u else None
    if not u or not p: 
        raise HTTPException(404, 'User or plan not found')
    p.updated_plan = update_workout_plan(p.original_plan, feedback, u.name, u.goal, u.intensity)
    p.feedback = feedback
    db.commit()
    return t.TemplateResponse(
        request=request,
        name='result.html',
        context={'user': u, 'plan': p, 'display_plan': p.updated_plan, 'is_updated': True}
    )

@r.post('/api/submit-feedback')
def feedback_api(d: FeedbackRequest, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.user_id == d.user_id).first()
    p = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == u.id).order_by(WorkoutPlan.created_at.desc()).first() if u else None
    if not u or not p: 
        raise HTTPException(404, 'User or plan not found')
    p.updated_plan = update_workout_plan(p.original_plan, d.feedback, u.name, u.goal, u.intensity)
    p.feedback = d.feedback
    db.commit()
    return {'updated_plan': p.updated_plan}

# 4. ADMIN ROUTE
@r.get('/admin', response_class=HTMLResponse)
def admin(request: Request, key: str = '', db: Session = Depends(get_db)):
    if key != settings.ADMIN_KEY: 
        raise HTTPException(403, 'Invalid admin key')
    return t.TemplateResponse(
        request=request,
        name='all_users.html',
        context={'users': db.query(User).all()}
    )