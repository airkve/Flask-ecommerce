from app import conexion, queries, Error

class Database():
    """ Clase para consultar, modificar y conectarse a la base de datos. """

    def __init__(self, *args, **kwargs):
        self.cursor = conexion.cursor()
        
    def crear_usuario(self, user):
        """ Crea un usuario en la DB usando:
        dni, item, apellido, email y clave. """

        try:
            self.cursor.execute(queries['add_user'], user)
        except Error as e:
            print('Hubo un problema al registrar los datos en la DB.', e)
        else:
            # registra los cambios a la base de datos
            conexion.commit()

    def eliminar_usuario(self, usuario_dni):
        """ Elimina a un usuario en la db usando su dni. """

        # archiva el DNI del usuario para multiple usos
        dni = usuario_dni.get_dni()
        # valida si existe el usuario en la db
        self.cursor.execute(queries['get_user_dni'], (dni,))
        consulta = self.cursor.fetchone()
        if consulta:
            try:
                self.cursor.execute(queries['del_user_by_dni'], (dni,))
            except Error as e:
                print('No existe alguien con ese codigo de usuario.', e)
            else:
                # registra los cambios a la base de datos
                conexion.commit()
                print('Usuario eliminado.')
        else:
            print('No existe un usuario con ese DNI.')
        
    def consultar_usuario_por_email(self, usuario):
        """ Busca a un usuario en la db por su email. """

        try:
            self.cursor.execute(queries['get_user_by_email'], (usuario,))
        except Error as e:
            print('No existe alguien con ese E-Mail.', e)
        else:
            consulta = self.cursor.fetchone()
        # envia el reporte en caso de que exista el email
        return consulta
    
    def consultar_usuario_por_dni(self, dni):
        """ Busca un usuario en la DB utilizando su DNI. """

        try:
            self.cursor.execute(queries['get_user_by_dni'], (dni,))
        except Error as e:
            print('No se encontró el usuario con ese DNI.', e)
        else:
            # archiva en una variable los resultados del query
            consulta = self.cursor.fetchone()
            # retorna la data del query
            return consulta

    def consultar_usuario_clave(self, clave):
        """ Busca la clave de un usuario en la DB. """

        self.cursor.execute(queries['get_user_by_pswd'], (clave,))
        consulta = self.cursor.fetchone()
        return consulta

    def consultar_clientes(self):
        """ Busca la lista de clientes en la DB. """

        self.cursor.execute(queries['get_clients'])
        consulta = self.cursor.fetchall()
        return consulta


    def validar_usuario(self, data):
        """ Busca el email y la clave de un usuario en la DB para validar login. """

        try:
            self.cursor.execute(queries['validate_user'], data)
        except Error as e:
            print('El usuario o la contraseña no coinciden.', e)
        else:
            # guarda la consulta en una variable
            result = self.cursor.fetchone()
            return result

    # Metodos para los poductos
    def eliminar_producto(self, producto):
        """ Elimina un producto en la DB por su ID. """

        # elimina un producto de la base de datos
        try:
            self.cursor.execute(queries['del_producto'], (producto.get_id(),))
        except Error as e:
            print('No existe un producto con ese ID.')
        else:
            # registra los cambios a la base de datos
            conexion.commit()

    def cargar_producto(self, producto):
        """ Crea un producto nuevo en la DB. """

        # inserta un producto en la base de datos
        try:
            self.cursor.execute(queries['add_product'], producto)
        except Error as e:
            print('No existe producto con ese ID.')
        else:
            # registra los cambios a la base de datos
            conexion.commit()
    
    def modificar_producto_cantidad(self, data):
        """ Modifica la cantidad de un producto en la DB. """

        try:
            self.cursor.execute(queries['mod_product_cant'], data)
        except Error as e:
            print('Ocurrió un problema al tratar de ejecutar la operación.', e)
        else:
            # registra los cambios a la base de datos
            conexion.commit()
            #print('Cambio exitoso {}.'.format(producto))

    def consultar_producto_id(self, producto):
        try:
            self.cursor.execute(queries['get_product_by_id'], (producto,))
        except Error as e:
            print('No se encontró el producto.', e)
        else:
            consulta = self.cursor.fetchone()
            # retorna el resultado de la busqued
            return consulta

    def consultar_lista_productos(self):
        """ Busca toda la lista de productos en la DB. """
        
        try:
            self.cursor.execute(queries['get_products'])
        except Error as e:
            print('Ocurrió un error al hacer la consulta.', e)
        else:
            # guarda la consulta en una variable
            consulta = self.cursor.fetchall()
            return consulta

    def crear_compra(self, shop_data):
        """ Registra las compras del cliente en la DB con:
            usuario_id, fecha, producto_id, cantidad y precioT. """

        try:
            self.cursor.execute(queries['new_shopping'], shop_data)
        except Error as e:
            print("Error al guardar los datos de la compra.", e)
        else:
            #guarda la consulta en una variable
            conexion.commit()

    def consultar_compras(self, cliente):
        """ Busca el historial de compras en la DB con el email del usuario. """

        try:
            self.cursor.execute(queries['get_user_shop_history'], (cliente,))
        except Error as e:
            print("Error al consultar el historico", e)
        else:
            # guarda la consulta en una variable
            consulta = self.cursor.fetchall()
            return consulta
        
    def consultar_ciudades(self):
        """ Busca la lista de ciudades en la DB. """

        try:
            self.cursor.execute(queries['ciudades'])
        except Error as e:
            print('Error al consultar la lista de ciudades.', e)
        else:
            # guarda la consulta en una variable
            consulta = self.cursor.fetchall()
            return consulta

    def consultar_producto_por_nombre(self, nombre):
        """ Busca producto en la DB por su nombre. """

        try:
            self.cursor.execute(queries['get_product_by_name'], (nombre,))
        except Error as e:
            print('Ocurrió un error al hacer la consulta.', e)
        else:
            # guarda la consulta en una variable
            consulta = self.cursor.fetchall()
            return consulta
