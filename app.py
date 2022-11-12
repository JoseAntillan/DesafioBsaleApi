from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from configuracion import configuracion

app = Flask(__name__)
CORS(app)
conexion = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/productos', methods=['GET'])
def listar_productos():
    try:
        app.config["MYSQL_HOST"] = "mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com"
        app.config["MYSQL_USER"] = "bsale_test"
        app.config["MYSQL_PASSWORD"] = "bsale_test"
        app.config["MYSQL_DB"] = "bsale_test"

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


@app.route('/categorias/<int:categoria>/listarproductos', methods=['GET'])
def leer_producto_bd(categoria):
    try:
        app.config["MYSQL_HOST"] = "mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com"
        app.config["MYSQL_USER"] = "bsale_test"
        app.config["MYSQL_PASSWORD"] = "bsale_test"
        app.config["MYSQL_DB"] = "bsale_test"

        cursor = conexion.connection.cursor()
        # consulta SQL combina la tabla product y category para poder entregar el nombre de la categoria
        sql =  \
              " ( SELECT product.id, product.name as producto, product.url_image, product.price, product.discount, product.category, " \
              " category.id as 'category_id', category.name as 'category_name' " \
              " FROM product INNER JOIN category ON product.category = category.id WHERE product.category="+str(categoria)+" ORDER BY product.name ) "




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




#obtener nombre de las categorias
@app.route('/categorias', methods=['GET'])
def listar_categorias():
    try:
        app.config["MYSQL_HOST"] = "mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com"
        app.config["MYSQL_USER"] = "bsale_test"
        app.config["MYSQL_PASSWORD"] = "bsale_test"
        app.config["MYSQL_DB"] = "bsale_test"


        cursor = conexion.connection.cursor()

        sql =  \
              "SELECT * from category"

        cursor.execute(sql)
        datos = cursor.fetchall()
        Categorias = []
        for fila in datos:
            Categoria = {
                'id': fila[0],
                'name': fila[1],
                'cantidad_productos': contar_category(fila[0])
            }
            Categorias.append(Categoria)
        return jsonify({'Categorias': Categorias, 'mensaje': "Categorias listadas.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error "+str(ex), 'exito': False})


def contar_category(categoria):
    try:
        app.config["MYSQL_HOST"] = "mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com"
        app.config["MYSQL_USER"] = "bsale_test"
        app.config["MYSQL_PASSWORD"] = "bsale_test"
        app.config["MYSQL_DB"] = "bsale_test"


        cursor = conexion.connection.cursor()

        sql =  \
              "SELECT COUNT(*) from product where category ="+str(categoria)

        cursor.execute(sql)
        datos = cursor.fetchall()
        for fila in datos:
               cantidad = fila[0]



        return cantidad
    except Exception as ex:
        return jsonify({'mensaje': "Error "+str(ex), 'exito': False})


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(configuracion['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()