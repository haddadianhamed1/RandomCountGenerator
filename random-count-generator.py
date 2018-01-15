import numpy
from collections import defaultdict
import abc
import Queue
from datetime import datetime
import threading
import argparse

"""
Create a function that prints a random number between 1 and 5 to stdout (or console). The probability distribution of the numbers should be as follows:

1 - 50%
2 - 25%
3 - 15%
4 - 5%
5 - 5%


numpy.random.choice(numpy.arange(1, 6), p=[0.5, 0.25, 0.15, 0.05, 0.05])

# good verification

random_number= defaultdict(int)
for i in (range(100)):
    random_number[numpy.random.choice(numpy.arange(1, 6), p=[0.5, 0.25, 0.15, 0.05, 0.05])] += 1
print random_number

"""

# using numpy printing random number with specific weight
def random_number():
    rn=numpy.random.choice(numpy.arange(1, 6), p=[0.5, 0.25, 0.15, 0.05, 0.05])
    print rn

# random_number()


# abstract class for tracking
class GetterSetter(object):
    __masterclass__ = abc.ABCMeta
    @abc.abstractmethod
    def generator(self):
        """generates random number"""
        return

    @abc.abstractmethod
    def get_history(self):
        """list of last n random numbers"""

        return

    @abc.abstractmethod
    def append_history(self):
        """adds number to the list of random numbers and removes oldest entry if list goes above 100 numbers"""

        return

    @abc.abstractmethod
    def cal_stat(self):
        """calculates the frequency of generated numbers"""

        return

    @abc.abstractmethod
    def write_event(self):
        """write the random number and timestamp to disk"""

        return


# class to generate and queue the history
# abstract class from GetterSetter
class Generator(GetterSetter):
    history = Queue.Queue(maxsize=100)
    event_writer = Queue.Queue()
    def generator(self, cond):
        with cond:
            cond.notify()
        #print("hi")
        rn = numpy.random.choice(numpy.arange(1, 6), p=[0.5, 0.25, 0.15, 0.05, 0.05])
        #print rn
        # after generating number calling write_Event method to time stamp and save to a file
        self.write_event(rn, datetime.utcnow())
        #print("hi")


        # after generating number calling append_history method
        self.append_history(rn)
        # print random number
        #print rn

    def get_history(self):
        return list(self.history.queue)
    def append_history(self,number):
        if self.history.qsize() >= 100:
            self.history.get()
        self.history.put(number)

    def cal_stat(self):
        random_number = defaultdict(int)
        for numbers in list(self.history.queue):
            random_number[numbers]+=1

        for key,value in random_number.iteritems():
            print key, str(value/float(self.history.qsize())*100) + '%'

    # worker refactor for starting a new thread
    def worker(self,cond):
        with open("allhistory.txt", "a") as file:
            obj = self.event_writer.get()
            #file.write("{}\t{}\n".format(obj[0], obj[1].strftime("%m/%d/%Y %H:%M:%S")))
            file.write("{}\t{}\n".format(obj[0], obj[1]))
            #print(obj[0], obj[1])
            # print the threads spun up
            #for thread in threading.enumerate():
            #   print(thread.name)
            #print ("$################")
            with cond:
                cond.notify()

    # write events to a file with time appeneded
    def write_event(self, number, now):
        # print number
        # adding a new thread to call write_event
        self.event_writer.put((number, now))
        cond = threading.Condition()
        t = threading.Thread(target=self.worker, args=(cond, ))
        t.daemon = True
        t.start()
        t.join()


def run_threads():
    cond = threading.Condition()
    y = Generator()
    t = threading.Thread(target=y.generator, args=(cond, ))
    # t.daemon = True
    t.start()
    t.join()
    # testing
    """
    x = Generator()
    for y in range (500):
        x.generator()

    print x.get_history()
    print len(x.get_history())

    x.cal_stat()
    """



def main():
    parser = argparse.ArgumentParser(description='This program generates random number and writes to a file.')
    parser.add_argument('--nt', default=5, type=int,
                        help='number of threads that you would like to run')
    args = parser.parse_args()
    for n in range(args.nt):
        run_threads()
if __name__ == "__main__":
    main()
