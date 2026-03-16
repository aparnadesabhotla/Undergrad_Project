import sys
import argparse
import middleware
import random
import time

text = ["See, you hear this word and shiver",
"While some of us get problems of the liver",
"yup! Exams are what I'm talking about",
"The reason pupils start howling about",
"Oh exams! What do we do with you",

"Dead were we when we turned the paper",
"Those questions turned us into vapor",
"Students like us had two or three attempted",
"Handed over those 2 sheets and left all exempted",
"You're welcome, now to hell with you",]

class Producer:
    def __init__(self, datatype):
        self.type = datatype

        self.queue = [middleware.XMLQueue(f"/{self.type}", middleware.MiddlewareType.PRODUCER)]
        if datatype == "temp":
            self.gen = self._temp
        elif datatype == "msg":
            self.gen = self._msg

    @classmethod
    def datatypes(self):
        return ["temp", "msg"]    

    def _temp(self):
        time.sleep(0.1)
        yield random.randint(0,40)

    def _msg(self):
        time.sleep(0.2)
        yield random.choice(text)


    def run(self, length=10):
        for _ in range(length):
            for queue, value in zip(self.queue, self.gen()):
                queue.push(value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", help="Type of producer: [temp, msg] : ", default="temp")
    parser.add_argument("--length", help="Number of messages to be Sent : ", default=10)
    args = parser.parse_args()

    if args.type not in Producer.datatypes():
        print("Error: not a valid producer type\n")
        sys.exit(1)

    p = Producer(args.type)

    p.run(int(args.length))
