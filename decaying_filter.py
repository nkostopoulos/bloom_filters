import sched,time
import mmh3
from math import trunc
from math import ceil
import sys
import thread
from time import sleep


class TimeDecayingBloomFilter(object):
	
	def __init__(self,counters,counterSize,hashCount,decayRate,timePeriod):
		if counters <= 0 or counterSize <= 0 or hashCount <= 0:
			raise ValueError("Sorry. Wrong arguments")
		self.counters = counters
		self.counterSize = counterSize
		self.hashCount = hashCount
		self.size = counters * counterSize
		self.decayRate = decayRate
		self.timePeriod = timePeriod
		self.filter = {}
		return None

	def getTimePeriod(self):
		return self.timePeriod

	def add(self, string):
                '''
                        A method to add an element in the Bloom filter
                '''
                for seed in xrange(self.hashCount):
                        result = mmh3.hash(string, seed) % self.counters # modulo the size of the filter to ensure
			if self.filter[result] < self.counterSize:
                        	self.filter[result] = self.filter[result] + 1 # the result is smaller than the size of the filter
                return None

	def query(self, string):
                '''
                        A method to perform a Bloom filter query
                '''
		minimum = self.counterSize + 1
                for seed in xrange(self.hashCount):
                        result = mmh3.hash(string, seed) % self.counters
                       	if self.filter[result] < minimum:
				minimum = self.filter[result]
		minimum = ceil((1 - self.decayRate) * minimum)
                return minimum

		
	def decayBloomFilterValues(self):
		for index in range(0,self.counters):
			self.filter[index] = trunc(self.filter[index] * self.decayRate)
			# decay the counters of the time-decaying bloom filter. The result is truncated.
		return None

	def initializeBloomFilter(self):
                for index in range(0,counters):
                        self.filter[index] = 0
                return None	
			

def operateBloomFilter(args):
	while True:
		stall = bf.getTimePeriod()
		print(bf.filter)
		s.enterabs(time.time() + stall,1,bf.decayBloomFilterValues,())
		s.run()
	return None
	
def get_input(bf):
	return None


if __name__ == "__main__":
	
	print("Executing python script: ",sys.argv[0])
	
	try:
		decayRate = float(sys.argv[1]) # the decay rate of the filter
		timePeriod = float(sys.argv[2]) # the period after which, the counters of the Bloom filter are decayed
		counters = int(sys.argv[3]) # the number of counters of the Bloom filter
		counterSize = int(sys.argv[4]) # the size of the counters in bits
		hashCount = int(sys.argv[5]) # the number of hash functions
	except:
		print("Arguments missing. Script execution is terminated.")
		sys.exit(1)
	
	s = sched.scheduler(time.time, time.sleep)

	bf = TimeDecayingBloomFilter(counters,counterSize,hashCount,decayRate,timePeriod)	

	bf.initializeBloomFilter()
	
	try:
		thread.start_new_thread(operateBloomFilter,(bf, ) )
		thread.start_new_thread(get_input,(bf, ) )
	except:
		print("Error creating threads. Script execution is terminated")
		sys.exit(1)
	
	while 1:
		pass
