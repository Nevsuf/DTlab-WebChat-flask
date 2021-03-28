# Questo modulo utilizza Flask per realizzare un web server. L'applicazione può essere eseguita in vari modi
# FLASK_APP=server.py FLASK_ENV=development flask run
# python server.py se aggiungiamo a questo file app.run()

from flask import Flask, request, jsonify
import user
import statusLabels
import message
import saveData

# viene creata l'applicazione con il nome del modulo corrente.
app = Flask(__name__)

# getErrorCode è una funzione di utilità che mappa i valori ritornati dal modulo user con quelli del
# protocollo HTTP in caso di errore. 
# 404 - Not Found: una risorsa non è stata trovata sul server;
# 403 - Forbidden: accesso negato;
# 409 - Conflict: è violato un vincolo di unicità. Ad esempio, esiste già un utente con la stessa mail registrata;
# Come ultima spiaggia è buona norma ritornare "500 - Internal Server Error" per indicare che qualcosa è andato storto
def getErrorCode(response: statusLabels)->int:
    
    if response is statusLabels.Result.NOT_FOUND:
        code = 404
    elif response is statusLabels.Result.NOT_AUTHORIZED:
        code = 403
    elif response is statusLabels.Result.DUPLICATED:
        code = 409
    else:
        code = 500

    return code


@app.route('/user', methods=['POST']) #crea un nuovo utente
def createUser():
    data = request.get_json()
    name = data['name']
    surname = data['surname']
    email = data['email']
    password = data['password']
    
    res, dic = user.SaveUser(name, surname, email, password)

    if res is not statusLabels.Result.OK:
        code = getErrorCode(res)
        return '', code
    else:
        return dic, 201


@app.route('/login', methods=['POST']) #effettua il login
def loginUser():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    res, dic = user.Login(email, password)
    
    if res is not statusLabels.Result.OK:
        code = getErrorCode(res)
        return '', code
    else:
        return dic, 200


@app.route('/inbox', methods=['POST']) #invia messaggio da mittente a destinatario
def sendMessage():
    data = request.get_json()
    sender = data['emailS']
    receiver = data['emailR']
    content = data['contentM']
    
    res, dic = message.SaveMessage(sender, receiver, content)
    
    if res is not statusLabels.Result.OK:
    	code = getErrorCode(res)
    	return '', code
    else:
    	return dic, 201


#rivedere: problema su visualizzazione dei messaggi da postman.
@app.route('/inbox/<string:id_utente>', methods=['GET']) #cerca tutti i messaggi dell'utente
def getMessage(id_utente: str):
    res, mess = message.GetMessage(id_utente)
        
    if res is not statusLabels.Result.OK:
    	code = getErrorCode(res)
    	return '', code
    else:
    	return jsonify(mess), 200 
        #serializzazione delle email in formato Json


#rivedere
@app.route('/user/<string:userId>', methods=['DELETE']) #cancella utente
def deleteUser(userId):
    res = user.Authorize(userId, request.headers["Authorization"])

    if res is not statusLabels.Result.OK:
        code = getErrorCode(res)
        return '', code
    else:
        return '', 204


@app.route('/save/<string:command>', methods=['GET']) #salva utenti o messaggi su file.csv
def writeDataOnFile(command: str):
    if command == "write_users":
        res = saveData.writeUsers()
    elif command == "write_messages":
        res = saveData.writeMessages()
        
    if res is not statusLabels.Result.OK:
    	code = getErrorCode(res)
    	return '', code
    else:
    	return '', 201

        
if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
    #se lasciamo 'localhost' indica che il server accetta richieste solo dal localhost (127.0.0.1) sulla porta 5000
    #'docker run -it -p 5000:5000 --name DTLab-chat python392slim'
    #usiamo tale comando con '-p 5000:5000'
