from app.models.db_setup.session import BaseModel
import sqlalchemy as sql


class Company(BaseModel):
    __tablename__ = 'companies'

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    name = sql.Column(sql.String, unique=True)
    description = sql.Column(sql.String, nullable=True)

    def __repr__(self):
        return f'Company: {self.name}'


