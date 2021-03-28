# Questo modulo implementa una semplice versione di un database per gli utenti in memoria.

import uuid
import bcrypt
import statusLabels
from datetime import datetime
import base64

users = []
# Utenti sono memorizzati come dizionari.
# utente = {
#    'id': '123'
#    'name': 'giuseppe',
#    'surname': 'capasso',
#    'password': '123',
#    'email': 'giuseppe@test.com'
#    'created': '5-03-2024', 
# }

#Metodo di utilità per cercare un utente dato in ingresso l'email. Se non esiste viene ritornato None
def findUserByEmail(email: str)->dict:
    for user in users:
        if user['email'] == email:
            return user
    return None

#Metodo di utilità per cercare un utente dato in ingresso un ID. Se non esiste viene ritornato None
def findUserByID(id: str)->dict:
    bID = uuid.UUID(id)
    for user in users:
        if user['id'] == bID:
            return user
    return None

# SaveUser memorizza un utente nel sistema dopo la procedura di signin degli utenti. 
# Prima controlla che non sia già registrato un utente con la stessa email, altrimenti ritorna un errore
# con la chiamata uuid.uuid4() si genera una stringa randomica che rappresenta l'ID dell'utente
# è fortemente sconsigliata la memorizzazione delle password degli utenti in chiaro, in quanto
# sarebbero accessibili da tutti. In questo caso utilizziamo il modulo bcrypt ("https://github.com/pyca/bcrypt/")
# Bcrypt fornisce due funzioni:
#   hashpw: che ritorna una versione "hashata" della password
#   chechpw: che effettua un confronto tra una password in chiaro e una hashata per vedere se corrispondono
# Alla fine viene creato un utente e inserito nella lista

def SaveUser(name: str, surname: str, email: str, password: str)->(statusLabels, dict):
    if findUserByEmail(email) is None:
        id = uuid.uuid4()
        hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        user = {
            'id': id,
            'name': name,
            'surname': surname,
            'email': email,
            'created': datetime.utcnow().isoformat(),
            'password': hashed
        }
        users.append(user.copy())
        user['password'] = ''
        return statusLabels.Result.OK, user
    else:
        return statusLabels.Result.DUPLICATED, None


# La funzione login controlla che esiste un utente con l'email inserita ed usa la funzione bcrypt.checkpw per controllare che la password sia corretta. 
def Login(email: str, password: str)->(statusLabels, dict):
    u = findUserByEmail(email)
    if u is not None and bcrypt.checkpw(password.encode('utf8'), u['password']):
        res = u.copy()
        res ['password'] = ''
        return statusLabels.Result.OK, res
    else:
        return statusLabels.Result.NOT_AUTHORIZED, None

#rivedere
def Authorize(userId: str, authorization: str) -> (statusLabels):
    # Check if authorization is basic
    if authorization is not None and authorization.startswith("Basic ") is True:
        base64AuthString = authorization.replace("Basic ", "")    
        plainTextAuthString = base64ToString(base64AuthString)
        credentials = plainTextAuthString.split(":")
        email = credentials[0]
        password = credentials[1]

        # Check whether user exists by providing the email/password pair
        result, u = Login(email, password)

        if result is not statusLabels.Result.OK:
            return statusLabels.Result.NOT_AUTHORIZED
        elif uuid.UUID(userId) != u["id"]:
            return statusLabels.Result.NOT_AUTHORIZED
        else:
            # Auth is ok, delete the user
            if DeleteUser(u["id"]):
                return statusLabels.Result.OK
            else:
                return statusLabels.Result.GENERIC_ERROR
    else:
        return statusLabels.Result.NOT_AUTHORIZED

#rivedere
def DeleteUser(userId: uuid) -> bool:
    id = userId
    counter = 0
    for user in users:
        if user['id'] == id:
            del users[counter]
            return True

        counter += 1
    else:
        return None

#rivedere
def base64ToString(base64AuthString: str) -> str:
    base64AuthBytes = base64AuthString.encode('ascii')
    plainTextAuthBytes = base64.b64decode(base64AuthBytes)
    return str(plainTextAuthBytes.decode('ascii'))

    