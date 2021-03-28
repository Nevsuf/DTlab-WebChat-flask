# Questo modulo implementa la gestione dei messaggi nel sistema.
import user
import statusLabels
from datetime import datetime

messages = []
    # Messaggi memorizzati come dizionari
    # message = {
    #    'messageID: '001'
    #    'created': '9-02-2021',
    #    'emailSender': 'karlo-k@email.it'
    #    'emailReceiver': 'johnM40@hotmail.it',
    #    'contentMess': 'ciao, sono io!'
    # }

def SaveMessage(sender: str, receiver: str, content: str)->(statusLabels, dict):
    if (user.findUserByEmail(sender) is not None):
        senderID = user.findUserByEmail(receiver)['id']
    else:
        return statusLabels.Result.NOT_FOUND, None
    
    if (user.findUserByEmail(receiver) is not None):
        receiverID = user.findUserByEmail(receiver)['id']
    else:
        return statusLabels.Result.NOT_FOUND, None

    id = len(messages) #messageID
    message = {
            'messageID': id,
            'created': datetime.utcnow().isoformat(),
            'emailSender': senderID,
            'emailReceiver': receiverID,
            'contentMess': content
    }

    messages.append(message.copy())
    return statusLabels.Result.OK, message
    
def GetMessage(id_utente: str)->(statusLabels, list):
    if (user.findUserByID(id_utente) is not None):
        targetEmail = user.findUserByID(id_utente)['email']
    else:
        return statusLabels.Result.NOT_FOUND, None
    
    emails = []
    
    for i in range(len(messages)):
        if messages[i]['emailReceiver'] == targetEmail:
            mex = messages[i]['contentMess']
            emails.append(mex)
        
    return statusLabels.Result.OK, emails     
    