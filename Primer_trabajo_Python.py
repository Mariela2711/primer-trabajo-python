
# COLORAMA   
from colorama import Fore, Back, init
init()




# BASE DE DATOS SQL    

''' 
Crear una base de datos llamada 'inventario.db' para almacenar los datos de los productos.
La tabla 'productos' debe contener las siguientes columnas:
id': Identificador único del producto (clave primaria, autoincremental).
nombre': Nombre del producto (texto, no nulo).
descripcion': Breve descripción del producto (texto).
cantidad': Cantidad disponible del producto (entero, no nulo).
precio': Precio del producto (real, no nulo).
categoria': Categoría a la que pertenece el producto (texto).
'''

import sqlite3

conexion=sqlite3.connect("inventario.db")

cursor=conexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        categoria TEXT
    )
''')

print( Back.BLUE + "Tabla 'productos' creada exitosamente en 'inventario.db'"+ Back.RESET )

conexion.commit()



# FUNCIONES  

'''
Funcionalidades de la aplicación:
Registrar nuevos productos.
Visualizar datos de los productos registrados.
Actualizar datos de productos, mediante su ID.
Eliminación de productos, mediante su ID.
Búsqueda de productos, mediante su ID. De manera opcional, se puede implementar la búsqueda por los 
campos nombre o categoría.
Reporte de productos que tengan una cantidad igual o inferior a un límite especificado por el 
usuario o usuaria.
'''

#funcion REGISTRAR NUEVOS PRODUCTOS:

def registrar_producto(nombre, descripcion, cantidad, precio, categoria):
    """Insertar un nuevo producto en 'inventario'"""
    try:
        #iniciar la transaccion  y pedir a usuario el ingreso de información. Uso de colorama AZUL para información
        conexion=sqlite3.connect("inventario.db")
        cursor=conexion.cursor()
        conexion.execute("BEGIN TRANSACTION")
                
        #insertar el nuevo producto
        cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?,?,?,?,?)",(nombre, descripcion, cantidad, precio, categoria))
        
        #confirmar los cambios. uso de colorama fondo verde para confirmación 
        conexion.commit()
        print(Fore.GREEN + "Producto agregado con éxito" + Fore.RESET )
    #error de datos ingresados en cantidad y precio. uso de colorama rojo para error    
    except ValueError:
        print(Fore.RED + "Error: Cantidad y precio deben ser números" + Fore.RESET)    
        
    except sqlite3.Error as e:
        #si ocurre un error se revierte los cambios. uso de colorama fondo rojo para error 
        conexion.rollback()
        print(f"{Back.RED}[ERROR]{Back.RESET} al registrar el producto: {e}")
    finally:
        conexion.close()
   
        


#Funcion visualizar datos de todos los productos registrados:
def visualizar_producto ():    
    try: 
        conexion=sqlite3.connect("inventario.db")
        cursor=conexion.cursor()
        """Muestra todos los productos del inventario"""
        cursor.execute("SELECT*FROM productos")
        productos=cursor.fetchall()
        if not productos:
            print(Fore.YELLOW + "No hay productos registrados" + Fore.RESET)
        else: 
            print("\n" + Back.BLUE + "Lista de productos: "+ Back.RESET)
            for producto in productos:
                print(f"""
                ID:{producto[0]},
                nombre:{producto[1]},
                descripcion: {producto[2]},
                cantidad: {producto[3]},
                precio: $ {producto[4]:.2f},
                categoria: {producto[5]}
                """)
    except sqlite3.Error as e:
        print(f"{Back.RED}[ERROR]{Back.RESET} al visualizar productos: {e}")
    finally: 
        conexion.close()
       
#Funcion Actualizar precio de  producto buscando por ID    
def actualizar_productos(id_productos, nuevo_precio):
    """codigo busqueda por ID de producto"""
    try:
        conexion = sqlite3.connect("inventario.db") 
        cursor=conexion.cursor()
        cursor.execute('UPDATE productos SET precio = ? WHERE id =?', (nuevo_precio, int(id_producto)))
        conexion.commit()
        print(Fore.GREEN  + "Producto actualizado correctamente" + Fore.RESET)
    except sqlite3.Error as e:
        print(f"{Back.RED}[ERROR]{Back.RESET} al actualizar producto: {e}")
    finally:
        conexion.close() 
    
    
#Funcion Eliminar producto bucando por ID     
def eliminar_producto(id):
    """Eliminar producto de la base de datos, buscando por id"""
    try:
        conexion = sqlite3.connect("inventario.db") 
        cursor=conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id=?", (id,))
        conexion.commit()
        print(Fore.GREEN  +"Producto eliminado" + Fore.RESET)
    except sqlite3.Error as e:
        print(f"{Back.RED}[ERROR]{Back.RESET} al eliminar producto: {e}")
    finally:
        conexion.close() 

#Funcion buscar productos por ID , Nombre y Categoría 
def buscar_id():
    """Buscar producto por ID"""
    try:
        id_producto = int(input("Ingrese el ID del producto a buscar: "))
        conexion = sqlite3.connect("inventario.db") 
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id=?", (id_producto,)) 
        producto = cursor.fetchone()
        
        if producto:
            print(f"{Fore.GREEN}Producto encontrado:{Fore.RESET}\nID:{producto[0]},\nnombre:{producto[1]},\ndescripcion: {producto[2]},\ncantidad: {producto[3]},\nprecio: $ {producto[4]:.2f},\ncategoria: {producto[5]}")
        else:
            print(f"\n{Fore.RED} No se encontró ningún producto con ID {id_producto} {Fore.RESET}")
            
    except ValueError:
        print(f"\n{Back.RED}[Error]{Back.RESET}: El ID debe ser un número entero ")
    except sqlite3.Error as e:
        print(f"\n{Back.RED} [Error]{Back.RESET} en la base de datos: {e} ")
    finally: 
        conexion.close()

def buscar_nombre():
    """Buscar producto por nombre"""
    try:
        nombre_producto = input("Ingrese el nombre del producto a buscar: ").strip().capitalize()
        conexion = sqlite3.connect("inventario.db") 
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre_producto}%",)) 
        productos = cursor.fetchall()
        
        if productos:
            
            for producto in productos:
                print(f"{Fore.GREEN}Producto encontrado:{Fore.RESET}\nID:{producto[0]},\nnombre:{producto[1]},\ndescripcion: {producto[2]},\ncantidad: {producto[3]},\nprecio: $ {producto[4]:.2f},\ncategoria: {producto[5]}")
        else:
            print(f"\n{Fore.RED} No se encontraron productos con nombre '{nombre_producto}' {Fore.RESET}")
            
    except sqlite3.Error as e:
        print(f"\n{Back.RED} [Error]{Back.RESET} en la base de datos: {e} ")
    finally: 
        conexion.close()

def buscar_categoria():
    """Buscar productos por categoría"""
    try:
        categoria_producto = input("Ingrese la categoría a buscar: ").strip().capitalize()
        conexion = sqlite3.connect("inventario.db") 
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", (f"%{categoria_producto}%",)) 
        productos = cursor.fetchall()
        
        if productos:
            
            for producto in productos:
                print(f"{Fore.GREEN}Producto encontrado:{Fore.RESET}\nID:{producto[0]},\nnombre:{producto[1]},\ndescripcion: {producto[2]},\ncantidad: {producto[3]},\nprecio: $ {producto[4]:.2f},\ncategoria: {producto[5]}")
        else:
            print(f"\n{Fore.RED} No se encontraron productos en la categoría '{categoria_producto}' {Fore.RESET}")
            
    except sqlite3.Error as e:
        print(f"\n{Back.RED} [Error] {Back.RESET} en la base de datos: {e} ")
    finally: 
        conexion.close()

    

#Funcion Reporte de productos que tengan una cantidad igual o inferior a 5 unidades    
def Reporte_producto_bajo_stock():
    
    try:
        control_stock=int(input("Ingrese la cantidad de stock a controlar: "))
        conexion = sqlite3.connect("inventario.db") 
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (control_stock,)) 
        productos = cursor.fetchall()
        
        if productos:
            print(f"{Back.BLUE}Productos con stock bajo :{Back.RESET}\n")
            for producto in productos:
                print(f"""
                ID: {producto[0]}
                Nombre: {producto[1]}
                Descripción: {producto[2]}
                Cantidad: {producto[3]}
                Precio: $ {producto[4]:.2f}
                Categoría: {producto[5]}
                """)
        else:
            print(f"{Fore.RED}+ No hay productos con stock menor a {control_stock} +{Fore.RESET}")
    except sqlite3.Error as e:
        print(f"{Back.RED}[ERROR]{Back.RESET} al generar reporte: {e}")        
    finally:
        conexion.close() 



#MENU  

while True: 
    print("\n" + Back.BLUE + "Programa de Gestión de Inventario" + Back.RESET)
    print("1- Registrar nuevos productos. ")
    print("2- Visualizar datos de los productos registrados. ")
    print("3- Actualizar datos de productos, mediante su ID. ")
    print("4- Eliminación de productos, mediante su ID.")
    print("5- Búsqueda de productos.  ")
    print("6- Reporte de productos con bajo stock.")
    print("7- Salir. ")
    
    
    opcion= input("\nIngresar número de opción: ")
    
    if opcion=="1":
        try: 
            nombre = input("Nombre del producto: ").strip().capitalize()
            descripcion = input("Descripción: ").strip().capitalize()
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            categoria = input("Categoría: ").strip().capitalize()
            if cantidad >0 and precio >0:
                registrar_producto(nombre, descripcion, cantidad, precio, categoria)
            else:
                print(Fore.RED + "El precio y la cantidad deben ser mayores a cero." + Fore.RESET)
        except ValueError:
            print(Fore.RED + "Error: Cantidad y precio deben ser números válidos" + Fore.RESET)  
              
    elif opcion =="2":
        visualizar_producto ()
        
    elif opcion == "3":
        try:
            id_producto= input(" Ingrese el id del producto a actualizar: ")
            nuevo_precio= float(input("Ingrese el nuevo precio: "))
            if nuevo_precio > 0:
                actualizar_productos(id_producto, nuevo_precio)
            else:
                print("El ID no existe")
        except ValueError:
            print(Fore.RED + "Error: ID y precio deben ser números válidos" + Fore.RESET)  
              
    elif opcion == "4":
        try:
            id_producto = int(input("Ingrese el ID del producto a eliminar: "))
            eliminar_producto(id_producto)
        except ValueError:
            print(Fore.RED + "Error: El ID debe ser un número válido" + Fore.RESET)
            
    elif opcion == "5":
        print("\nOpciones de búsqueda:")
        print("1 - Buscar por ID")
        print("2 - Buscar por nombre")
        print("3 - Buscar por categoría")
    
        try:
            opcion_buscar = input("Ingrese el número de opción de búsqueda: ")
            if opcion_buscar == "1":
                buscar_id()
            elif opcion_buscar == "2":
                buscar_nombre()
            elif opcion_buscar == "3":
                buscar_categoria()
            else:
                print(f"\n{Back.RED} Opción de búsqueda inválida {Back.RESET}")
        except Exception as e:
            print(f"\n{Back.RED} Error: {e} {Back.RESET}")
      
    
    elif opcion == "6":
        Reporte_producto_bajo_stock()
        
    elif opcion == "7":
        print (Fore.GREEN + "Salió del Programa de Gestion de Inventario." + Fore.RESET)
        break
    
    else:
        print(Fore.RED + "Opción inválida. Por favor ingrese un número del 1 al 7." + Fore.RESET)
        
        
conexion.close()