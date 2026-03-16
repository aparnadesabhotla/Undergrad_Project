class topic:
    def __init__(self, name):
        """Constructor Parameters: name: name of the topic"""
        self._name = name
        self._childTopics = [] # list of child topics
        self._subscribers = set() # set of subscribers (sockets) to the topic
        self._lastMsg = None # last message published to the topic
        self._parent = None # parent topic of the topic

    def addChild(self, topic): #filho to child
        """ Adds a new topic to the list of child topics  Parameters:topic: topic (child) to be added """
        self._childTopics.append(topic)
        for sub in self._subscribers:
            topic.addSubs(sub) # children inherit subscribers frrom the parent topic
        
        
    def addSubs(self, conn):
        """Adds a consumer to the list of subscribers for the topi
        Parameters:
            conn: Socket representing the consumer (subscriber).
        """
        self._subscribers.add(conn) 
        for t in self._childTopics:
            t.addSubs(conn) # Children inherit subscribers from parents.


    def getSubs(self):
        """ returns the set of subscribers for topic """
        return self._subscribers

    def getName(self):
        """ returns the topic name """
        return self._name

    def getParent(self): ##getPai to get parent
        """ returns the parent topic of topic """
        return self._parent

    def setLastMsg(self, value):
        """ saves/sets the last message published in the topic

            Parameters:
            value: msg value

        """
        self._lastMsg = value    


    def getAllLastMsgs(self):
        """ returns a list of the last message published in the topic, including the children """
        if not self._lastMsg == None:
            list = [self._lastMsg]
        else:
            list = []
        for t in self._childTopics:
            list = list + t.getAllLastMsgs()
        return list


    def getLastMsg(self):
        """ returns the last message published in the topic """
        return self._lastMsg   #returns None if it doesn't exist


    def getTopic(self, name): 
        """ returns a topic (or None if it doesn't exist)

            Parameters:
            name: name of the topic we want to receive

        """
        if self._name == name: # if you find
            return self

        for t in self._childTopics:# if not search child topics

            resp = t.getTopic(name)
            if not resp is None:
                return resp
        return None # if not found (does not exist)

        
    def insertTree(self, name, temp=""): # string
        """Inserts a topic in the tree structure.

        Parameters:
        name: name of the topic to be inserted
        temp: temporary topic name (used for recursive calls)

        Returns:
        The inserted topic
        """

        if self._name == name:
            return self
        
        name_list = name.split("/") # separate the topic name by "/"
        temp_list = temp.split("/") # separate the temporary topic name (parent of parent/etc) by "/"

        if not len(name) == len(temp):
            temp += "/" + name_list[len(temp_list)] # add the name of a child to the temporary topic

        for child in self._childTopics:
            if child.getName() == temp:
                return child.insertTree(name, temp) # insert into the tree as a child of this topic
            
        # if there are no children with the temporary name
        new_topic = topic(temp)
        self.addChild(new_topic) # add it to this topic's children

        if not len(name) == len(temp):
            temp_list = temp.split("/")
            temp += "/" + name_list[len(temp_list)] # add the name of a child to the temporary topic
            return new_topic.insertTree(name, temp)
        else:
            return new_topic # return the new topic


    def setParent(self, parent):#pai to parent
        """Sets the parent topic of this topic Parameters: parent: the parent topic"""
        self._parent = parent
        self._subscribers.update(parent.getSubs())


    def deleteFromTree(self, c):
        """ Removes a subscriber from the list of subscribers of a topic

            Parameters:
            c: subscriber to be removed
        """
        
        if c in self._subscribers:
            self._subscribers.remove(c)
        for t in self._childTopics: #children topics inherit subscribers from their parents.
            t.deleteFromTree(c)
            

    def __str__(self):
        return "Topic: " + self._name

    def print_topics(self):
        """ Prints all the topics contained in the structure """
        print(self)
        for t in self._childTopics:
            t.print_topics()


    def getList(self):
        """ Returns all the descendants of a topic including itself """
        list = [self._name]
        for t in self._childTopics:
            list = list + t.getList()
        return list
