from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

from configuracion import configuracion
#from validaciones import *
app = Flask(__name__)

# CORS(app)
#CORS(app, resources={r"/cursos/*": {"origins": "http://localhost"}})

conexion = MySQL(app)


# @cross_origin
@app.route('/productos', methods=['GET'])
def listar_cursos():
    try:
        #nombre = request.args.get("nombre")

        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM product ORDER BY id ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        Productos = []
        for fila in datos:
            curso = {
                'id': fila[0],
                'name': fila[1],
                'url_image': fila[2],
                'price': fila[3],
                'discount': fila[4],
                'category': fila[5]
            }
            Productos.append(curso)
        return jsonify({'cursos': Productos, 'mensaje': "Cursos listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

##aqui hacer el metodo para buscar producto en especifico


@app.route('/productos/<categoria>', methods=['GET'])
def leer_curso_bd(categoria):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM product WHERE category = '{0}'".format(categoria)
        cursor.execute(sql)
        datos = cursor.fetchall()
        Productos = []
        for fila in datos:
            curso = {
                'id': fila[0],
                'name': fila[1],
                'url_image': fila[2],
                'price': fila[3],
                'discount': fila[4],
                'category': fila[5]
            }
            Productos.append(curso)
        return jsonify({'cursos': Productos, 'mensaje': "Cursos listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error: ", 'exito': False})



def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(configuracion['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()