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
def listar_productos():
    try:
        busqueda = request.args.get("busqueda")
        cursor = conexion.connection.cursor()
        # consulta SQL combina la tabla product y category para poder entregar el nombre de la categoria
        sql =  \
              " ( SELECT product.id, product.name as producto, product.url_image, product.price, product.discount, product.category, " \
              " category.id as 'category_id', category.name as 'category_name' " \
              " FROM product INNER JOIN category ON product.category = category.id ORDER BY product.name ) "

        #si existe el parametro busqueda se usa como filtro en la consulta SQL
        if busqueda:
            busqueda = busqueda.strip()
            sql = "SELECT * FROM " + sql + "AS TablaBusqueda WHERE TablaBusqueda.producto LIKE '%"+busqueda+"%' ORDER BY TablaBusqueda.producto"

        cursor.execute(sql)
        datos = cursor.fetchall()
        Productos = []
        for fila in datos:
            Producto = {
                'id': fila[0],
                'name': fila[1],
                'url_image': fila[2],
                'price': fila[3],
                'discount': fila[4],
                #'Pcategory_id': fila[5],
                "Ccategory_id": fila[6],
                "Category_name": fila[7],
            }
            Productos.append(Producto)
        return jsonify({'Productos': Productos, 'mensaje': "Productos listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error "+str(ex), 'exito': False})


@app.route('/productos/<int:categoria>', methods=['GET'])
def leer_producto_bd(categoria):
    try:
        busqueda = request.args.get("busqueda")
        cursor = conexion.connection.cursor()
        # consulta SQL combina la tabla product y category para poder entregar el nombre de la categoria
        sql =  \
              " ( SELECT product.id, product.name as producto, product.url_image, product.price, product.discount, product.category, " \
              " category.id as 'category_id', category.name as 'category_name' " \
              " FROM product INNER JOIN category ON product.category = category.id WHERE product.category="+str(categoria)+" ORDER BY product.name ) "

        #si existe el parametro busqueda se usa como filtro en la consulta SQL
        if busqueda:
            busqueda = busqueda.strip()
            sql = "SELECT * FROM " + sql + "AS TablaBusqueda WHERE TablaBusqueda.producto LIKE '%"+busqueda+"%' ORDER BY TablaBusqueda.producto"

        cursor.execute(sql)
        datos = cursor.fetchall()
        Productos = []
        for fila in datos:
            Producto = {
                'id': fila[0],
                'name': fila[1],
                'url_image': fila[2],
                'price': fila[3],
                'discount': fila[4],
                #'Pcategory_id': fila[5],
                "Ccategory_id": fila[6],
                "Category_name": fila[7],
            }
            Productos.append(Producto)
        return jsonify({'Productos': Productos, 'mensaje': "Productos listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error "+str(ex), 'exito': False})


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(configuracion['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()