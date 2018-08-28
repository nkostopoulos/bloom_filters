from __future__ import division
from random import normalvariate,uniform,randint
from bitarray import bitarray
from math import floor
import string
import sys

class LocalitySensitiveBloomFilter:

	def __init__(self, size, dimension, W_parameter, hash_count):
		'''
			contrustor of class LocalitySensitiveBloomFilter. Arguments:
			- size: the size of the locality sensitive Bloom filter
			- dimension: the dimension of the input
			- W_parameter: the W parameter of the hash functions
			- hash_count: the number of hash functions
		'''
		self.size = size # the size of the locality sensitive Bloom filter in bits
		self.dimension = dimension # the dimension of the vectors
		self.W_parameter =  W_parameter # the W parameter of the locality sensitive Bloom filter
		self.hash_count = hash_count # the number of hash function the filter uses
		self.A,self.B = self.generate_A_and_B_parameters() # parameters A and B of the filter
		self.bit_array = bitarray(self.size) # the filter itself, it is a bitarray
		self.bit_array.setall(0) # initialize lsbf with zeroes

	def print_parameters(self):
		'''
			A method to print the parameters of the Locality Sensitive Bloom filter
		'''
		print("Printing the parameters of the locality sensitive Bloom filter")
		print("Size of the locality sensitive Bloom filter is: ",self.size)
		self.size_in_KB,self.size_in_MB = self.print_size_in_KB_MB()
		print("Size of filter in KB: ",self.size_in_KB)
		print("Size of filter in MB: ",self.size_in_MB)
		print("Dimension of vectors is: ",self.dimension)
		print("The W parameter of the locality sensitive Bloom filter is: ",self.W_parameter)
		print("The number of hash functions the locality sensitive Bloom filter uses is: ",self.hash_count)
		return None
	
	def print_size_in_KB_MB(self):
		'''
			Transform size of filter in kiloBytes and megaBytes
		'''
		try:
			size_in_bytes = self.size/8
			size_in_KB = size_in_bytes/1024
			size_in_MB = size_in_KB/1024
			return size_in_KB,size_in_MB
		except:
			print("Exception occurred. Termination")
			sys.exit(1)

	def generate_A_and_B_parameters(self):
		'''
			A method to generate the A and B parameters of the Locality Sensitive Bloom filter
		'''	
		A = list()
		B = list()
		for index in range(0,self.hash_count):
			a = [normalvariate(0,1) for i in range(self.dimension)]
			b = uniform(0,self.W_parameter)
			A.append(a)
			B.append(b)
		return A,B

	def lsh(self,vector):
		'''
			Locality Sensitive Hashing based on p-stable distributions of a given vector
		'''
		hashed_values = list()
		for index in range(0,self.hash_count):
			a = self.A[index]
			b = self.B[index]
			hashVal = floor((sum(a[i] * float(vector[i]) for i in range(self.dimension)) + b)/self.W_parameter)
			hashed_values.append(int(hashVal))
		return hashed_values
			
	def add_element(self,domain_name,character_order):
		'''
			Add element in the filter
		'''
		vector = convert_string_to_vector(domain_name,character_order)
		hashed_values = self.lsh(vector)
		for value in hashed_values:
			position = value % self.size
			self.bit_array[position] = 1
			print(position)
		print("\n")
		return None

	def query_element(self,domain_name,character_order):
		'''
			Query for an element to answer the approximate membership test
		'''
		vector = convert_string_to_vector(domain_name,character_order)
		hashed_values = self.lsh(vector)
		for value in hashed_values:
			position = value % self.size
			print(position)
			if self.bit_array[position] != 1:
				if self.bit_array[position - 1] != 1 and self.bit_array[position + 1] != 1:
					return False
		return True
	
def get_dictionary_of_character_order():
        '''
                Returns the dictionary with the order of letters and digits, e.g. a is 0, b is 1, .... , z is 25, 0 is 26, 1 is 27, 9 is 35. We also include hyphen in position 36.
        '''
        character_order_dict = dict()
        letter_list = string.ascii_lowercase
        digit_list = '0123456789-'
        concatenated_list = letter_list + digit_list
        position = 0
        for character in concatenated_list:
                character_order_dict[character] = position
                position = position + 1
        return character_order_dict

def convert_string_to_vector(domain_name,character_order_dict):
        '''
                A method to convert a string containing letters and digits in a N-Dimensional vector
        '''
        vector_of_string = list()
        vector_of_string = [0] * 37 * 37 # 26 letters in the english alphabet, 10 digits, 1 special character (hyphen)

        for index in range(0,len(domain_name) - 1):
                bigram = domain_name[index] + domain_name[index + 1]
                bigram_position = 37 * character_order_dict[bigram[0]] + character_order_dict[bigram[1]]
                vector_of_string[bigram_position] = vector_of_string[bigram_position] + 1

        return vector_of_string

def fill_filter(lsbf,zone_file,character_order):
	'''
		Fill the filter with the names from the zone file
	'''
	for line in open(zone_file,"r"):
		domain_name = line.rstrip()
		lsbf.add_element(domain_name,character_order)
	return lsbf

def set_filter_parameters():
	'''
		Set the parameters of the Locality Sensitive Bloom Filter
	'''
	size = 10000
	dimension = 1369
	W = 4
	hash_functions = 15
	return size,dimension,W,hash_functions

def check_results(lsbf,zone_file,character_order):
	trues = 0
	falses = 0
	for line in open(zone_file,"r"):
		domain_name = line.rstrip()
		result = lsbf.query_element(domain_name,character_order)
		if result == True:
			trues = trues + 1
		else:
			falses = falses + 1
	return trues,falses

def main_function():
	'''
		The main functions of the python script
	'''
	zone_file = "/home/nkostopoulos/ntua_names"
	parameters = set_filter_parameters()
	lsbf = LocalitySensitiveBloomFilter(parameters[0],parameters[1],parameters[2],parameters[3])
	lsbf.print_parameters()
	character_order = get_dictionary_of_character_order()
	# lsbf = fill_filter(lsbf,zone_file,character_order)

	'''
	# time to check the results
	zone_file = "/home/nkostopoulos/typo_names"
	trues,falses = check_results(lsbf,zone_file,character_order)
	false_negative = falses/(trues + falses)
	print("false negatives: ",false_negative)
	zone_file = "/home/nkostopoulos/random_names"
	trues,falses = check_results(lsbf,zone_file,character_order)
	false_positive = trues/(trues + falses)
	print("false positives: ",false_positive)
	'''
	return None

if __name__ == "__main__":
	print("Executing python script: ",sys.argv[0])
	main_function()
