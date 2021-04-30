"""add initial admin user

Revision ID: d8f391174715
Revises: 4be03bdb5c90
Create Date: 2021-04-30 15:00:04.961247

"""
from alembic import op
import sqlalchemy as sa
from app.models.db_setup.session import SessionLocal
from app.models.user import User

db = SessionLocal()
# revision identifiers, used by Alembic.
revision = 'd8f391174715'
down_revision = '4be03bdb5c90'
branch_labels = None
depends_on = None


def upgrade():
    user = db.query(User).filter(User.username=='admin_user').first()
    if user: 
        return 
    username = 'admin_user'
    password = 'admin_pass'
    user = User(username=username, company_id=4, is_admin=True)
    user.set_password(password)
    db.add(user)
    db.commit()
    db.close()


def downgrade():
    user = db.query(User).filter(User.username=='admin_user').first()
    if user:
        db.delete(user)
        db.commit()
        db.close()
