# DodOps Ticket API
Versión API de DodOps Ticket.
API para creación, gestión y seguimiento de tickets.

## Requisitos
- Python 3.11.3
- Flask
- SQLAlchemy

## Instalación
```bash
git clone https://github.com/TaquitoAdobado/dodops-ticket.git
cd api
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
- Linux/MacOS: source venv/bin/activate
- Windows PowerShell: venv\Scripts\Activate.ps1
- Windows CMD: venv\Scripts\activate.bat

## Configuración
- Renombrar `.env.example` a `.env` y ajustar las variables con tus datos.
- Mover `config.example.py` a `instance/
- Renombrar a config.py` y configurar según tu entorno.

## Ejecución
python app.py

## Endpoints
En desarrollo. Por ahora solo corre localmente.
URL_BASE: http://127.0.0.1:5000/ ó http://localhost:5000/

- `GET /tickets` -> Lista todos los tickets (200 OK).
- `POST /tickets` -> Crea nuevo ticket (201 Created).
- `PUT /tickets/<int:id>` -> Edita título y descripción (200 OK).
- `PATCH /tickets/<int:id>` -> Edita título o descripción (200 OK).
- `DELETE /tickets/<int:id>` -> Elimina ticket (204 No Content).

## Ejemplo de usos para Endpoints

### Crear Ticket
**Request**
POST URL_BASE/tickets
BODY (JSON):
```json
{
    "title": "Title example ticket 2",
    "description": "This is an example description for ticket #2."
}
```
**Response**
Status: 201 Created
```json
{   "id": 2,
    "title": "Title example ticket 2",
    "description": "This is an example description for ticket #2.",
    "creation_date": "2026-07-27T23:22:14+00:00",
    "closed_date": null
}
```

### Ver Tickets (Todos)
GET URL_BASE/tickets
**Response**
Status: 200 OK
```json
[
    {   "id": 1,
        "title": "Title example ticket 1",
        "description": "This is an example description for ticket #1.",
        "creation_date": "2026-07-27T23:22:14+00:00",
        "closed_date": null
    },
    {   "id": 2,
        "title": "Title example ticket 2",
        "description": "This is an example description for ticket #2.",
        "creation_date": "2026-07-27T23:22:14+00:00",
        "closed_date": null
    }
]
```

### Ver Tickets (por ID)
GET URL_BASE/tickets/2
**Response**
Status: 200 OK
```json
{   "id": 2,
    "title": "Title example ticket 2",
    "description": "This is an example description for ticket #2.",
    "creation_date": "2026-07-27T23:22:14+00:00",
    "closed_date": null
}
```

### Editar Tickets (Título y descripción)
PUT URL_BASE/tickets/2
BODY (JSON):
```json
{
    "title": "New Title",
    "description": "This is the new description."
}
```
**Response**
Status: 200 OK
```json
{   "id": 2,
    "title": "New Title",
    "description": "This is the new description.",
    "creation_date": "2026-07-27T23:22:14+00:00",
    "closed_date": null
}
```

### Editar Tickets (Título ó descripción)
PATCH URL_BASE/tickets/2
BODY (JSON):
```json
{
    "title": "Im a Error"
}
```
**Response**
Status: 200 OK
```json
{   "id": 2,
    "title": "Im a Error",
    "description": "This is the new description.",
    "creation_date": "2026-07-27T23:22:14+00:00",
    "closed_date": null
}
```

### Eliminar Tickets (por ID)
DELETE URL_BASE/tickets/2
**Response**
Status: 204 No Content

> API en desarrollo. Solo está disponible en entorno local (`localhost:5000`).  
> Conforme avance el proyecto este archivo se irá actualizando.