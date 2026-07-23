# DodOps
DodOps es una aplicación web para la creación, gestión y seguimiento de tickets, diseñada con enfoque en simplicidad, eficiencia y adaptabilidad a distintos entornos.

## Tecnologías.
**Backend:**
    - Python
    - Flask / FastAPI

**Base de datos:**
    - SQLite en fase inicial.
    - Uso de ORM SQLAlchemy -> Para opcion de migración a MySQL / PostgreSQL u otros motores SQL.

**FrontEnd:**
    - HTML5
    - CSS3
    - Javascript
> Nota: El frontend se implementará como **mínimo viable**, sin frameworks adicionales en esta fase inicial. El objetivo es proveer una interfaz simple y funcional, priorizando el desarrollo del backend y la lógica de negocio.

**Control de versiones:**
    - Git + Github

## Funcionalidades iniciales
- CRUD de tickets:
    - `POST` -> Crear ticket.
    - `GET` -> Consultar ticket.
    - `PUT / PATCH` -> Actualizar ticket.
    - `DELETE` -> Eliminar ticket.

Ciclo de vida de un ticket:
1. **Nuevo** -> Ticket recien creado, aún sin responsable.
2. **Asignado** -> Ticket asignado a un usuario/responsable.
3. **En progreso** -> Ticket en seguimiento o resolución activa.
4. **En pausa (opcional)** -> Ticket detenido por razones justificadas. En esta fase, el tiempo del ticket se pausa.
5. **Resuelto** -> Ticket solucionado, pendiente de cierre.
6. **Cerrado** -> Ticket finalizado oficialmente.

## Identidad visual.
- Logo principal: DodOps en indigo sobre fondo blanco.
- Variante para fondo oscuro: DodOps indigo con outline claro.
- Submarcas futuras:
  - DodOps Tickets
  - DodOps Reports  
  - DodOps Config 

## Organización del repositorio.
DodOps/
|- README.md
|- .gitignore
|- static/
|  |- css/
|  |- js/
|  |- img/
|
|- templates/
|- routes/
|- models/