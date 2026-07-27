from extensions import db

# Heredamos de db.model para convertir la clase en una tabla.
class Ticket(db.Model):

    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    closed_date = db.Column(db.DateTime(timezone=True), nullable=True)
    # db.DateTume(timezone=True) -> Define fecha y hora con zona horaria.
    # server_default=db.func.now() -> Hace que la db asigne fecha y hora al crear el registro.

    def __repr__(self):
        return f"""
        Ticket(title = {self.title},
        description = {self.description},
        creation_date = {self.creation_date},
        closed_date = {self.closed_date})
        """

    def __str__(self):
        return f"""
        title = {self.title},
        description = {self.description},
        creation_date = {self.creation_date},
        closed_date = {self.closed_date})
        """