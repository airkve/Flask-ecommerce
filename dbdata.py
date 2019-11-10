# Diccionario con la configuracion de la base de datos

dbconf = {
    'host':'localhost',
    'database':'ecommerce',
    'user':'root',
    'password':''
}

queries = {
    'get_user_by_pswd':'SELECT * FROM usuarios WHERE clave = %s',
    'get_user_by_email':'SELECT * FROM usuarios WHERE email = %s',
    'get_user_by_dni':'SELECT * FROM usuarios WHERE usuario_id = %s',
    'get_user_dni':'SELECT dni FROM usuarios WHERE dni = %s',
    'get_user_email':'SELECT email FROM usuarios WHERE email = %s',
    'add_user':'INSERT INTO usuarios (dni, nombre, apellido, email, telefono, clave, direccion, ciudad_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
    'del_user_by_id':'DELETE FROM usuarios WHERE usuario_id = %s',
    'del_user_by_dni':'DELETE FROM usuarios WHERE dni = %s',
    'validate_user':'SELECT * FROM usuarios WHERE email = %s AND clave = %s',
    'get_user_shop_history':'SELECT usuarios.nombre, compras.fecha_compra, productos.producto_id, productos.nombre, compras.cantidad, compras.precio_total FROM usuarios INNER JOIN compras ON compras.usuario_id = usuarios.usuario_id INNER JOIN productos ON productos.producto_id = compras.producto_id WHERE usuarios.email = %s  ORDER BY compras.fecha_compra desc',
    'get_clients':'SELECT usuarios.email, usuarios.nombre, usuarios.apellido, usuarios.clave, usuarios.dni, usuarios.telefono, direcciones.direccion, direcciones.altura, direcciones.codigo_postal, ciudades.nombre, provincias.nombre, paises.nombre FROM usuarios INNER JOIN direcciones ON direcciones.id = usuarios.direccion_id INNER JOIN ciudades ON ciudades.ciudad_id = direcciones.ciudad_id INNER JOIN provincias ON provincias.provincia_id = ciudades.provincia_id INNER JOIN paises ON paises.pais_id = provincias.pais_id',
    'get_client':'SELECT usuarios.email, usuarios.nombre, usuarios.apellido, usuarios.clave, usuarios.dni, usuarios.telefono, direcciones.direccion, direcciones.altura, direcciones.codigo_postal, ciudades.nombre, provincias.nombre, paises.nombre FROM usuarios INNER JOIN direcciones ON direcciones.id = usuarios.direccion_id INNER JOIN ciudades ON ciudades.ciudad_id = direcciones.ciudad_id INNER JOIN provincias ON provincias.provincia_id = ciudades.provincia_id INNER JOIN paises ON paises.pais_id = provincias.pais_id WHERE usuario_id = %s',
    'get_address_by_user_id':'SELECT direcciones.id, direcciones.direccion, direcciones.altura, direcciones.codigo_postal, ciudades.nombre, provincias.nombre, paises.nombre FROM direcciones INNER JOIN ciudades ON ciudades.ciudad_id = direcciones.ciudad_id INNER JOIN provincias ON provincias.provincia_id = ciudades.provincia_id INNER JOIN paises ON paises.pais_id = provincias.pais_id WHERE direcciones.id = (SELECT usuarios.direccion_id FROM usuarios WHERE usuarios.direccion_id = %s)',
    'get_address_id':'SELECT direccion_id FROM usuarios WHERE dni = %s',
    'get_product_by_id':'SELECT productos.producto_id, productos.nombre, productos.descripcion, productos.precio, categorias.nombre, marcas.nombre, productos.cantidad FROM productos INNER JOIN categorias ON categorias.categoria_id = productos.categoria_id INNER JOIN marcas ON marcas.marca_id = productos.marca_id WHERE producto_id = %s',
    'get_product_by_name':'SELECT productos.producto_id FROM productos WHERE productos.nombre = %s',
    'get_product_cant_by_id':'SELECT productos.cantidad FROM productos WHERE productos.producto_id = %s',
    'get_products':'SELECT productos.producto_id, productos.nombre, productos.descripcion, productos.precio, categorias.nombre, marcas.nombre, productos.cantidad FROM productos INNER JOIN categorias ON categorias.categoria_id = productos.categoria_id INNER JOIN marcas ON marcas.marca_id = productos.marca_id',
    'add_product':'INSERT INTO productos (nombre, descripcion, marca, categoria, precio) VALUES (%s, %s, %s, %s, %s)',
    'mod_product_cant':'UPDATE productos set cantidad = %s where producto_id = %s',
    'del_product':'DELETE FROM productos WHERE producto_id = %s',
    'new_shopping':'INSERT INTO compras (usuario_id, fecha_compra, producto_id, cantidad, precio_total) VALUES (%s, %s, %s, %s, %s)',
    'ciudades':'SELECT ciudad_id, nombre FROM ciudades'
}