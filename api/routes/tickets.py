from flask import Blueprint, request, jsonify
from extensions import db
from models import Ticket
from datetime import datetime, timezone

# Creamos instancia de Blueprint para representar la ruta de tickets
tickets_bp = Blueprint("tickets", __name__)# Parametros: Nombre del archivo, __name__ para que Flask lo reconozca.

# Al finalizar de configurar las rutas importamos la blueprint en app.py usando "app.register_blueprint(tickets_bp)"

#------------------------ FUNCIONES AUXILIARES ------------------------
# Validacion de ID
def id_validation(id):
    '''
    Funcion que valida el ID recibido en la URL de una solicitud a la API.
    
    Parametros:
    - id: Identidicador del ticket. Actualmente es un numero entero positivo.
    
    Retorno: 
    Si la validacion es correcta:
    - error: None, id: int
    
    Si la validacion no es correcta:
    - error: dict, id: None

    Diferentes casos de validacion:
    - La longitud del ID debe ser menor o igual a 18 caracteres (Previene overflow de int).
    - El ID debe ser un numero entero.
    - El ID debe ser mayor a 0.
    '''
    if len(id) > 18:
        return {"error": "Invalid ticket ID"}, None
    
    try:
        id = int(id)
    except ValueError:
        return {"error": "Invalid ticket ID"}, None
    
    if id < 1:
        return {"error": "Invalid ticket ID"}, None

    return None, id


# Validacion de datos
def data_validation(data, partial = False):
    '''
    Funcion que valida los datos recibidos en el body de una solicitud a la API.
    
    Parametros:
    - data: dict con los datos recibidos en el body de la solicitud por medio de request.get_json(silent=True).
    - partial (Bool):
        False(por defecto) -> Validacion completa (POST, PUT).
            *Se requiere que exista title y description en el body.
            *Valida ambos campos.
        True -> Validacion parcial (PATCH).
            *Se requiere almenos uno de los campos title o description en el body.
            *Valida los campos presentes.

    Retorno:
    Si la validacion no es correcta, devuelve:
    error: dict, data: None
    
    Si la validacion es correcta, devuelve:
    error: None, data: dict

    Casos de validacion
    partial = False:
        - Ausente title o description
        - Vacios title o description
        - JSON con body None

    partial = True:
        - Ausente title y description
        - Vacios title o description
        - JSON con body None
    '''

    # Validacion de body Null
    if data is None:
        return {"error": "invalid or missing JSON body"}, None

    # Validacion de completa de campos title y description.
    if not partial:
        if 'title' not in data or 'description' not in data:
            return {"error": "Missing title or description"}, None
        
        # Validacion de campos no vacíos.
        if data['title'].strip() == "" or data['description'].strip() == "":
            return {"error": "Title or description can't be empty"}, None

    # Validacion parcial de campos title y description.
    else:
        if 'title' not in data and 'description' not in data:
            return {"error": "Missing data"}, None
        
        if 'title' in data and data['title'].strip() == "":
            return {"error": "Title can't be empty"}, None
        
        if 'description' in data and data['description'].strip() == "":
            return {"error": "Description can't be empty"}, None

    return None, data
# ----------------  NUEVO TICKET ----------------

@tickets_bp.route("/tickets", methods=["POST"])
def create_ticket():
    # Recibimos los datos del ticket en el body de la solicitud.
    data = request.get_json(silent=True)

    # Validacion de datos.
    error,valid_data = data_validation(data)

    # Si la validacion no fue correcta, devolvemos el error.
    if not valid_data:
        return jsonify(error), 400
    
    else:
        # Creamos nuevo ticket con los datos.
        new_ticket = Ticket(
            title = valid_data['title'],
            description = valid_data['description'])
                
        # Almacenamos el ticket en la base de datos.
        db.session.add(new_ticket)
        db.session.commit()

        # Retornamos mensaje de confirmación.
        return jsonify({
            "id": new_ticket.id,
            "title": new_ticket.title,
            "description": new_ticket.description,
            "creation_date": new_ticket.creation_date.isoformat(), #Formato ISO 8601 (YYYY-MM-DDTHH:MM:SS)
            "closed_date": new_ticket.closed_date # None por defecto
        }), 201 # 201 Created


#----------------  VER TICKETS (TODOS) ----------------
@tickets_bp.route("/tickets", methods=["GET"])
def get_tickets():
    tickets = db.session.scalars(db.select(Ticket)).all()
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
@tickets_bp.route("/tickets/<id>", methods=["GET"])
def get_ticket(id):

    # Validacion de ID
    error, valid_id = id_validation(id)

    if not valid_id:
        return jsonify(error), 400
    
    # Validacion ticket existente
    ticket = db.session.get(Ticket, valid_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    
    else:
        return jsonify({
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "creation_date": ticket.creation_date.replace(tzinfo=timezone.utc).isoformat(),
            "closed_date": ticket.closed_date.replace(tzinfo=timezone.utc).isoformat() if ticket.closed_date is not None else None
        }), 200


#----------------  EDITAR TICKET (COMPLETO) ----------------
@tickets_bp.route("/tickets/<id>", methods=["PUT"])
def edit_ticket(id):

    # Validacion de ID
    error, valid_id = id_validation(id)

    if not valid_id:
        return jsonify(error), 400
    
    # Validacion ticket existente
    ticket = db.session.get(Ticket, valid_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    # Validacion de datos.
    data = request.get_json(silent=True)
    error, valid_data = data_validation(data)

    # Si la validacion no fue correcta, devolvemos el error.
    if not valid_data:
        return jsonify(error), 400

    else:
        # Actualizacion del ticket
        ticket.title = valid_data['title']
        ticket.description = valid_data['description']
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
@tickets_bp.route("/tickets/<id>", methods=["PATCH"])
def patch_ticket(id):

    # Validacion de ID
    error, valid_id = id_validation(id)
    if not valid_id:
        return jsonify(error), 400
    
    # Validacion ticket existente
    ticket = db.session.get(Ticket, valid_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    # Validacion de datos
    data = request.get_json(silent=True)

    error, valid_data = data_validation(data, True)
    if not valid_data:
        return jsonify(error), 400
 
    # Actualizacion de title y description
    if 'title' in valid_data:
        ticket.title = valid_data['title']
    if 'description' in valid_data:
        ticket.description = valid_data['description']

    db.session.commit()

    # Mensaje de confirmacion
    return jsonify({
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "creation_date": ticket.creation_date.replace(tzinfo=timezone.utc).isoformat(),
        "closed_date": ticket.closed_date.replace(tzinfo=timezone.utc).isoformat() if ticket.closed_date is not None else None
    }), 200

#----------------  ELIMINAR TICKET ----------------
@tickets_bp.route("/tickets/<id>", methods=["DELETE"])
def delete_ticket(id):

    # Validacion de ID
    error, valid_id = id_validation(id)
    if not valid_id:
        return jsonify(error), 400
    
    # Validacion ticket existente
    ticket = db.session.get(Ticket, valid_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    
    else:
        db.session.delete(ticket)
        db.session.commit()
        return "", 204