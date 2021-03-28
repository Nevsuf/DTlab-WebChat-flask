import user
import statusLabels
import message 
  

def writeMessages()->(statusLabels):
    messages_file = open("messages.txt", "w")
    messages_file.write("ID-CREATED-SENDER-RECEIVER-CONTENT\n")
    for i in range(len(message.messages)):
        if str(message.messages[i]).startswith('{'):
            line = message.messages[i]
            lista = list() #lista di appoggio
            lista.append(line['messageID'])
            lista.append(line['created'])
            lista.append(line['emailSender'])
            lista.append(line['emailReceiver'])
            lista.append(line['contentMess'])
            for j in range(len(lista)):
                messages_file.write(str(lista[j]))
                messages_file.write(";")
            messages_file.write("\n")
        else:
            return statusLabels.Result.NOT_FOUND
        
    messages_file.close()
    return statusLabels.Result.OK


def writeUsers()->(statusLabels):
    users_file = open("users.txt", "w")
    users_file.write("ID-NAME-SURNAME-EMAIL-CREATED\n")
    for i in range(len(user.users)):
        if str(user.users[i]).startswith('{'):
            line = user.users[i]
            lista = list() #lista di appoggio
            lista.append(line['id'])
            lista.append(line['name'])
            lista.append(line['surname'])
            lista.append(line['email'])
            lista.append(line['created'])
            for j in range(len(lista)):
                users_file.write(str(lista[j]))
                users_file.write(";")
            users_file.write("\n")
        else:
            return statusLabels.Result.NOT_FOUND
        
    users_file.close()
    return statusLabels.Result.OK
