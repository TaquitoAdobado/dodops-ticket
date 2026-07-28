from flask import Blueprint, request, jsonify
from extensions import db
from models import Ticket
from datetime import datetime, timezone

# Creamos instancia de Blueprint para representar la ruta de tickets
tickets_bp = Blueprint("tickets", __name__)# Parametros: Nombre del archivo, __name__ para que Flask lo reconozca.

# Al finalizar de configurar las rutas importamos la blueprint en app.py usando "app.register_blueprint(tickets_bp)"


# ----------------  NUEVO TICKET ----------------

@tickets_bp.route("/tickets", methods=["POST"])
def create_ticket():
    # Recibimos los datos del ticket en el body de la solicitud.
    data = request.get_json()

    # Creamos nuevo ticket con los datos.
    new_ticket = Ticket(
        title = data['title'],
        description = data['description']
    )

    # Almacenamos el ticket en la base de datos.
    db.session.add(new_ticket)
    db.session.commit()

    # Retornamos mensaje de confirmación.
    return jsonify({
        "id": new_ticket.id,
        "title": new_ticket.title,
        "description": new_ticket.description,
        "creation_date": new_ticket.creation_date.isoformat() #Formato ISO 8601 (YYYY-MM-DDTHH:MM:SS)
    }), 201 # 201 Created
    

#----------------  VER TICKETS (TODOS) ----------------
@tickets_bp.route("/tickets", methods=["GET"])
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify([
        {
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            # Creation date viene en UTC, inlcuimos la zona horaria "+00:00" y lo formateamos en ISO 8601 (YYYY-MM-DDTHH:MM:SS+00:00) 
            "creation_date": ticket.creation_date.replace(tzinfo=timezone.utc).isoformat(),
            # Si el ticket esta cerrado (Ya no es null -> none en python), aplicamos formato de creation_date.
            "closed_date": ticket.closed_date.replace(tzinfo=timezone.utc).isoformat() if ticket.closed_date is not None else None
        }
    for ticket in tickets]), 200


#----------------  VER TICKETS (POR ID) ----------------
@tickets_bp.route("/tickets/<int:id>", methods=["GET"])
def get_ticket(id):
    ticket =Ticket.query.get(id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    else:
        return jsonify({
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "creation_date": ticket.creation_date.replace(tzinfo=timezone.utc).isoformat(),
            "closed_date": ticket.closed_date.replace(tzinfo=timezone.utc).isoformat() if ticket.closed_date is not None else None
        })


#----------------  EDITAR TICKET (COMPLETO) ----------------
@tickets_bp.route("/tickets/<int:id>", methods=["PUT"])
def edit_ticket(id):
    # Ticket no econtrado
    ticket = Ticket.query.get(id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    
    data = request.get_json()

    # Campos incompletos
    if "title" not in data or "description" not in data:
        return jsonify({"error": "Missing title or description"}), 400

    # Actualizacion del ticket
    ticket.title = data['title']
    ticket.description = data['description']
    db.session.commit()

    # Mensaje de confirmacion
    return jsonify({
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "creation_date": ticket.creation_date.replace(tzinfo=timezone.utc).isoformat(),
        "closed_date": ticket.closed_date.replace(tzinfo=timezone.utc).isoformat() if ticket.closed_date is not None else None
    }), 200


#----------------  EDITAR TICKET (Parcial) ----------------
@tickets_bp.route("/tickets/<int:id>", methods=["PATCH"])
def patch_ticket(id):
    
    # Ticket no econtrado
    ticket = Ticket.query.get(id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    
    data = request.get_json()

    # Actualizacion del ticket
    if "title" in data: ticket.title = data['title']
    if "description" in data: ticket.description = data['description']
    db.session.commit()

    # Mensaje de confirmacion
    return jsonify({
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "creation_date": ticket.creation_date.replace(tzinfo=timezone.utc).isoformat(),
        "closed_date": ticket.closed_date.replace(tzinfo=timezone.utc).isoformat() if ticket.closed_date is not None else None
    }), 200


@tickets_bp.route("/tickets/<int:id>", methods=["DELETE"])
def delete_ticket(id):

    ticket = Ticket.query.get(id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    
    else:
        db.session.delete(ticket)
        db.session.commit()
        return "", 204