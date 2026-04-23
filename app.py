from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

contactos = [
    {"id": 1, "nombre": "Carlos Mendoza", "email": "carlos@empresa.com", "rol": "Desarrollador", "estado": "Activo"},
    {"id": 2, "nombre": "Laura Torres",   "email": "laura@empresa.com",  "rol": "Diseñadora",    "estado": "Activo"},
    {"id": 3, "nombre": "Miguel Ríos",    "email": "miguel@empresa.com", "rol": "Product Manager","estado": "Inactivo"},
]
next_id = 4  


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/contactos", methods=["GET"])
def get_contactos():
    return jsonify(contactos)

@app.route("/api/contactos", methods=["POST"])
def create_contacto():
    global next_id
    datos = request.json

    if not datos.get("nombre") or not datos.get("email"):
        return jsonify({"error": "Nombre y email son requeridos"}), 400

    nuevo = {
        "id":     next_id,
        "nombre": datos["nombre"],
        "email":  datos["email"],
        "rol":    datos.get("rol", ""),
        "estado": datos.get("estado", "Activo"),
    }
    contactos.append(nuevo)
    next_id += 1
    return jsonify(nuevo), 201


# ── READ: obtener uno por ID ───────────────────────────────────────
@app.route("/api/contactos/<int:id>", methods=["GET"])
def get_contacto(id):
    contacto = next((c for c in contactos if c["id"] == id), None)
    if not contacto:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify(contacto)


# ── UPDATE: actualizar por ID ──────────────────────────────────────
@app.route("/api/contactos/<int:id>", methods=["PUT"])
def update_contacto(id):
    contacto = next((c for c in contactos if c["id"] == id), None)
    if not contacto:
        return jsonify({"error": "No encontrado"}), 404

    datos = request.json
    contacto["nombre"] = datos.get("nombre", contacto["nombre"])
    contacto["email"]  = datos.get("email",  contacto["email"])
    contacto["rol"]    = datos.get("rol",    contacto["rol"])
    contacto["estado"] = datos.get("estado", contacto["estado"])
    return jsonify(contacto)


# ── DELETE: eliminar por ID ────────────────────────────────────────
@app.route("/api/contactos/<int:id>", methods=["DELETE"])
def delete_contacto(id):
    global contactos
    contacto = next((c for c in contactos if c["id"] == id), None)
    if not contacto:
        return jsonify({"error": "No encontrado"}), 404

    contactos = [c for c in contactos if c["id"] != id]
    return jsonify({"mensaje": f"Contacto {id} eliminado"}), 200


if __name__ == "__main__":
    app.run(debug=True)