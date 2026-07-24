# DodOps Ticket
DodOps Ticket es un proyecto modular para la creación, gestión y seguimiento de tickets, diseñado con enfoque en simplicidad, eficiencia y adaptabilidad a distintos entornos.

El sistema se desarrollará en tres componentes principales:

1. **API**  
   Núcleo del proyecto. Gestiona la lógica de negocio, endpoints REST y conexión con la base de datos.
   Es la primera fase y el punto de partida.

2. **SaaS con interfaz web**  
   Aplicación web que consume la API y se despliega en la nube, ofreciendo el servicio a usuarios externos mediante login y gestión de tickets desde cualquier navegador.
   Planeado como fase futura.

3. **App local**  
   Versión de escritorio/servidor interno con backend integrado. Pensada para empresas que deseen correr DodOps Ticket en su propia infraestructura, accesible vía navegador dentro de la red interna.  
   Planeado como fase futura.

## Tecnologías.
**Backend:**
    - Python
    - Flask inicial / FastAPI posible migración a futuro

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
- Logo principal: Indigo sobre fondo blanco.
- Variante para fondo oscuro: Indigo con outline claro.

## Roadmap
- [ ] Fase 1: API (CRUD de tickets, autenticación básica).
- [ ] Fase 2: SaaS con interfaz web.
- [ ] Fase 3: App local con backend integrado.

## Organización del repositorio.
```
dodops-ticket/
├── README.md        # Visión general del proyecto
├── .gitignore
├── api/
│   ├── README.md    # Instrucciones para levantar la API
│   ├── instance/
│   ├── models/
│   ├── routes/
│   └── tests/
```
> Nota: Al planearse DodOps Ticket como 3 componenes (API, SaaS y App) se tendrán 3 carpetas principales con sus respectivos nombres. Cada carpeta será añadida conforme evolucione el proyecto.