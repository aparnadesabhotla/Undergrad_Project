import selectors
import socket
import json
import xml.etree.ElementTree as ET
from topics import topic
from utils import XMLtoDict
from utils import dictToXML
HOST = ''                 
PORT = 18000
sel = selectors.DefaultSelector()
serializacoes = {} # dictionary with information about the type of serialization of each entity
produtores = {} # dictionary with producer sockets and the topics they publish on
root = topic("/")
# topic initialization "/"


def deserialize(conn, messages):
    """ decodes the message

        Parameters:
        message: message to be decoded
        conn: socket that sent the message
    """
    serial = serializacoes[conn] 
# type of serialization associated with the socket

    if serial == 1: # JSON
        msg = messages.decode('utf-8')
        msg = json.loads(msg)
    else: # XML
        msg = XMLtoDict(messages)
    return msg



def serialize(conn, messages):
    """ encodes the message

        Parameters:
        message: message to be sent
        conn: socket that sends the message

    """
    serial = serializacoes[conn] # type of serialization associated with the socket
    if serial == 1: # JSON
        msg = json.dumps(messages)
        msg = msg.encode('utf-8')
    elif serial == 2: # XML
        msg = dictToXML(messages)

    return msg




def dumpsAndSend(conn, data):
    """ creates the header for the messages and sends them

        Parameters:
        conn: socket that sends the message
        data: data to be sent

    """
    dataSerial = serialize(conn, data)  # encode
    header = '{:05d}'.format(len(dataSerial)) # create the header
    conn.sendall(header.encode('utf-8')) # send the header
    conn.sendall(dataSerial)# send the message



def accept(sock, mask):
    """ accepts new connections

        Parameters:
        sock: socket of the broker that receives the calls
        mask: mask

    """
    conn, addr = sock.accept()
    print('Accepted', conn, 'from', addr,'\n')

    conn.setblocking(False) # prevent blocking
    sel.register(conn, selectors.EVENT_READ,read)# register the socket in the selector



def publish(topic, value): # function to send publications to consumers
    """ send publications to consumers

        Parameters:
        topic: topic where it is published
        value: publication value

    """
    usersToSend = topic.getSubs() # consumers who should receive the message

    msg={'TOPIC':topic.getName(), 'VALUE': value}

    for c in usersToSend:
        dumpsAndSend(c, msg)

    topic.setLastMsg(msg) # save the last topic message sent

def closeSocket(conn):
    """ closes the connection and removes the associated data

        Parameters:
        conn: broker socket associated with a given entity

    """
    print('Closing', conn,'\n') 
    del serializacoes[conn] # remove serialization type information
    if conn in produtores: 
        del produtores[conn]# remove information about what topic it was posted in
    else:
        root.deleteFromTree(conn) # remove from a topic's subscriber lists (and children)
    sel.unregister(conn)
    conn.close()


def read(conn, mask):
    """ read events that occurred

        Parameters:
        conn: socket associated with the entity that performed the event
        mask: socket mask

    """
    if conn not in serializacoes: # if you are not registered yet
        serial = conn.recv(1) # serialization type
        if serial:
            serial = int(serial)
            serializacoes[conn] = serial # assign the serialization type to the socket
            return
        else:  # if you don't receive serialization information, terminate the socket
            closeSocket(conn)
            return

    tm = conn.recv(5) # get the header #tamanhomsg: tm
    if tm:
        tm = int(tm.decode('utf-8'))

        dataSerial = conn.recv(tm)

        if not dataSerial: # in case of disconnecting
            closeSocket(conn)   
            return
        tamanhoDataSerial=len(dataSerial) 
        while(tamanhoDataSerial<tm):# ensure that the message is read all the way to the end
            dataSerial=dataSerial+conn.recv(tm-tamanhoDataSerial)
            tamanhoDataSerial=len(dataSerial)

        data = deserialize(conn, dataSerial) # decode message
        print("Messages received: ", data)
        if data['OP'] == 'join': # register
            t = root.getTopic(data['TOPIC']) # returns the topic defined in data['TOPIC'] (if it doesn't exist, it returns None)
            if data['TYPE'] == 1: # if it's a consumer
                if not t is None: # if topic already exists
                    t.addSubs(conn) # add the conusmer to that topic's subscriber list (and child topics)

                else: # if the topic has not been created yet
                    t = root.insertTree(data['TOPIC'])# insert the topic into the structure
                    t.addSubs(conn)# add the consumer

                lastTopicMsgs = t.getAllLastMsgs() # returns a list with the last message published in the topic, as well as the child topics
                
                for msg in lastTopicMsgs:
                    dumpsAndSend(conn, msg) # send these last messages

            else: # if you are a producer

                if t is None: # if the topic doesn't already exist in the tree
                    t = root.insertTree(data['TOPIC']) # create the topic and insert it into the tree

                produtores[conn] = t # add the socket of the producer to the corresponding topic

        elif data['OP'] == 'publish': # publish
            if conn in produtores: #in principle it's always true
                publish(produtores[conn], data['VALUE']) # publish


        elif data['OP'] == 'topics_request': # ask for list of topics
            l = root.getList() # returns the list of all topics
            l = '\n'.join(l) # turn the list into a string with each topic separated by /n

            msg = {'OP' : 'topics_list', 'LIST' : l} # create message
            dumpsAndSend(conn, msg) # envia

        elif data['OP'] == 'leave_topic':# unsubscribe to a thread
            root.deleteFromTree(conn)# remove the socket from the list of subscribers of the topic and its children

    else: # when to disconnect
        closeSocket(conn)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # assign the address and port to the socket
    s.listen(100) # create 1 queue just for 1 connection, while a socket is running the other stays in the list the others are rejected
    s.setblocking(False)
    sel.register(s,selectors.EVENT_READ,accept)

    while True: 
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


