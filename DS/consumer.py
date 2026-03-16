import sys
import argparse
import middleware

class Consumer:
    def __init__(self, datatype):
        self.type = datatype
        self.queue = middleware.JSONQueue(f"/{self.type}")
        # self.queue = middleware.PickleQueue("/")
        
    @classmethod
    def datatypes(self):
        return ["temp", "msg"]    

    def run(self, length=10):
        i = 15
        
        while True:
            
          # if i == 0: # unsubscribe to topic
            # self.queue.leaveTopic()
            # print("already out!")

            if i == 10: 
                self.queue.getTopicsList()

            topic, data = self.queue.pull()
            if topic == None: # ask for list of threads
                print("\nList of topics presnt in broker: ")
                print(data) 
                print()
                
            else:
                print(topic, data)
            i -= 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", help="Type of producer: [temp, msg]", default="temp")
    args = parser.parse_args()

    if args.type not in Consumer.datatypes():
        print("Error: not a valid producer type")
        sys.exit(1)

    p = Consumer(args.type)
    
    p.run()
