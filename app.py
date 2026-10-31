import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Carpeta donde se van a guardar los respaldos de las bases de datos en la nube
CARPETA_RESPALDOS = "respaldos_clientes"
os.makedirs(CARPETA_RESPALDOS, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
  return jsonify(
      {"estado": "Servidor de NeoPOS activo y funcionando correctamente 🚀"}
  )


@app.route("/subir_backup", methods=["POST"])
def subir_backup():
  # Verificamos si se envió un archivo y el nombre de la tienda
  if "file" not in request.files:
    return jsonify({"error": "No se encontró el archivo de base de datos"}), 400

  archivo = request.files["file"]
  nombre_tienda = request.form.get("tienda", "tienda_desconocida")

  if archivo.filename == "":
    return jsonify({"error": "Nombre de archivo vacío"}), 400

  if archivo:
    # Limpiamos el nombre para evitar errores en la ruta
    nombre_seguro = f"{nombre_tienda}_neopos.db"
    ruta_guardado = os.path.join(CARPETA_RESPALDOS, nombre_seguro)

    # Guardamos el archivo sobrescribiendo el anterior respaldo de esa tienda
    archivo.save(ruta_guardado)
    return (
        jsonify({
            "exito": True,
            "mensaje": f"Respaldo de {nombre_tienda} guardado con éxito.",
        }),
        200,
    )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
