from extensions import db

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Company id = {self.id} name = {self.name} active = {self.active}>"

    def __str__(self):
        return f"""
        Company: {self.name}, Active: {self.active},
        Created: {self.created_at}, Updated: {self.updated_at},
        Deleted: {self.deleted_at}
        """