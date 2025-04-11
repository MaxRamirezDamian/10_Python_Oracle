from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from  flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
# Configurar CORS para permitir solicitudes desde React (puerto 3000)
#CORS(app, resources={r"/*": {"origins": "https://silver-guide-449w56p7667fq64p-3000.app.github.dev"}})
CORS(app, resources={r"/*": {"origins": "*"}})  # Permitir todos los orígenes temporalmente

#CONFIGURAR EL QSlALCHEMY CON ORACLE CLOUD
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#CONFIGURAR EL QSlALCHEMY CON ORACLE CLOUD
db = SQLAlchemy(app)

#DEFINIR EL MODELO DE LA BASE DE DATOS
class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {	
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio
        }
#crear  las tablas en la base de datos
with app.app_context():
    db.create_all()



# RUTA PARA OBTENER TODOS LOS PRODUCTOS 
@app.route('/productos', methods=['GET'])
def get_productos():
    productos = Productos.query.all()
    return jsonify([p.to_dict() for p in productos])
    
# RUTA PARA  OBTENER UN  PRODUCTO POR ID
@app.route('/productos/<int:id>', methods=['GET'])
def get_producto_by_id(id):
    productos = Productos.query.get(id)
    return jsonify([productos.to_dict() if productos else ('Producto no encontrado'), 404])	


# RUTA PARA CREAR UN NUEVO PRODUCTO
@app.route('/productos', methods=['POST'])
def create_producto():
    data = request.get_json()
    nuevo_producto = Productos(nombre=data['nombre'], precio=data['precio'])
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify(nuevo_producto.to_dict()), 201

# RUTA PARA ACTUALIZAR UN PRODUCTO
@app.route('/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    data = request.get_json()
    productos = Productos.query.get(id)
    if not productos:
        return jsonify({'message': 'Producto no encontrado'}), 404
    productos.nombre = data['nombre']
    productos.precio = data['precio']
    db.session.commit()
    return jsonify(productos.to_dict())

# RUTA PARA ELIMINAR UN PRODUCTO
@app.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    productos = Productos.query.get(id)
    if not productos:
        return jsonify({'message': 'Producto no encontrado'}), 404
    db.session.delete(productos) 
    db.session.commit()
    return jsonify({'message': 'Producto eliminado'}), 200    


if __name__ == '__main__':
    app.run(debug=True ,host='0.0.0.0', port=5000)


    