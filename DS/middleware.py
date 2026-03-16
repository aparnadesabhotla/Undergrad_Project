from enum import IntEnum
import socket
import json
import xml.etree.ElementTree as ET
from utils import XMLtoDict
from utils import dictToXML


class SerializationType(IntEnum): # enum with serialization types
    JSON=1
    XML=2
    


class MiddlewareType(IntEnum):# enum to indentify the type of entities
    CONSUMER = 1
    PRODUCER = 2

class Queue:
    HOST = 'localhost'
    PORT = 18000
    
    def __del__(self):
       """Queue Destruction""" 
       print('closing socket')
       self.socket.close()# end the connection

    def __init__(self, topic, type=MiddlewareType.CONSUMER):
        """Constructor

            Parameters:
            topic: topic associated with the Queue
            type: type of entity that contains the Queue

        """
        self.topic = topic
        self.type = type
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)# register a socket 
        self.socket.connect((self.HOST, self.PORT))#try to connect


    def push(self, value): # Publication
        """ Sends data to broker. """
        header = '{:05d}'.format(len(value)) # header with message size
        self.socket.sendall(header.encode()+value) # send header and message


    """ receives data from the broker"""
    def pull(self):
        sizemsg= self.socket.recv(5)  # get the message size
        sizemsg= int(sizemsg.decode('utf-8')) # decode the header
        dataSerial = self.socket.recv(sizemsg)  # receive the message
        sizeDataSerial=len(dataSerial) # ensure that the msg is read all the way to the end
        while(sizeDataSerial<sizemsg): 
            dataSerial=dataSerial+self.socket.recv(sizemsg-sizeDataSerial) 
            sizeDataSerial=len(dataSerial)
        return dataSerial


    def getJoinTopicMsg(self):
        """returns a message to inform the broker that it wants to participate in the process """
        return {'OP': 'join', 'TOPIC': self.topic, 'TYPE': int(self.type)}


    def getPublishMsg(self, value):
        """ returns a post msg """
        return {'OP': 'publish', 'VALUE': value}

    
    def getTopicsListMsg(self):
        """returns topic list request msg """
        return {'OP': 'topics_request'}
    
    
    def getLeaveMsg(self):
        """ returns unsubscription message for a given topic """
        return {'OP' : 'leave_topic'}


        


class JSONQueue(Queue):
    serial = SerializationType.JSON

    def __init__(self, topic, type=MiddlewareType.CONSUMER):
        super().__init__(topic, type)
        ser = '{:1d}'.format(int(self.serial)) # send serialization type
        self.socket.sendall(ser.encode('utf-8'))
        msg = super().getJoinTopicMsg() # ask for join message
        msg = json.dumps(msg) #convert the message to JSON
        msgReady = msg.encode('utf-8')
        super().push(msgReady) # send the message to the broker
    
    def push(self, value):
        msg = super().getPublishMsg(value)
        msgReady = json.dumps(msg) 
        msgReady = msgReady.encode('utf-8')
        super().push(msgReady)

    def pull(self):
        dataSerial = super().pull() # receive data from broker
        data = dataSerial.decode('utf-8')
        data = json.loads(data) # decode the message

        if 'LIST' in data: # if you receive the list of topics
            return None, data['LIST']

        return data['TOPIC'], data['VALUE']

    def getTopicsList(self):
        msg = super().getTopicsListMsg()
        msgJSON = json.dumps(msg)
        msgReady = msgJSON.encode('utf-8')
        super().push(msgReady)
    
    def leaveTopic(self):
        msg = super().getLeaveMsg()
        msgJSON = json.dumps(msg)
        msgReady = msgJSON.encode('utf-8')
        super().push(msgReady)

# -----------------------------------------------------------------------------

class XMLQueue(Queue):
    serial = SerializationType.XML

    def __init__(self, topic, type=MiddlewareType.CONSUMER):
        super().__init__(topic, type)
        ser = '{:1d}'.format(int(self.serial)) # send serialization type
        self.socket.sendall(ser.encode('utf-8'))
        msg = super().getJoinTopicMsg()
        msgXML = dictToXML(msg) # convert the message to XML
        super().push(msgXML) #send the message to the broker


    def push(self, value):

        msg = super().getPublishMsg(value)
        msgReady = dictToXML(msg)
        super().push(msgReady)

    def pull(self):
        dataSerial = super().pull()
        data = XMLtoDict(dataSerial) # decodes
        if 'LIST' in data: #get list of topics
            return None, data['LIST']
        return data['TOPIC'], data['VALUE']

    def getTopicsList(self):
        msg = super().getTopicsListMsg()
        msgReady = dictToXML(msg)
        super().push(msgReady) # create the header and send

    def leaveTopic(self):
        msg = super().getLeaveMsg()
        msgReady = dictToXML(msg)
        super().push(msgReady)



