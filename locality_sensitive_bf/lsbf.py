from __future__ import division
from random import normalvariate,uniform,randint
from bitarray import bitarray
from math import floor
import string
import sys

MAX_CHARS = 20 # the maximum number of characters in a domain name
DIMENSION = 720 # dimension of the vectors hashed
LSBF_SIZE = 83886080 # size of the locality sensitive Bloom filter
HASH_COUNT = 3 # number of hash functions used
W_parameter = 4 # the W parameter of the locality sensitive hash functions

def get_dictionary_of_character_order():
        '''
                Returns the dictionary with the order of letters and digits, e.g. a is 0, b is 1, .... , z is 25, 0 is 26, 1 is 27, 9 is 35
        '''
        character_order_dict = dict()
        letter_list = string.ascii_lowercase
        digit_list = '0123456789'
        concatenated_list = letter_list + digit_list
        position = 0
        for character in concatenated_list:
                character_order_dict[character] = position
                position = position + 1
        return character_order_dict

def convert_string_to_vector(domain_name,character_order_dict,max_characters):
        '''
                A method to convert a string containing letters and digits in a N-Dimensional vector
        '''
        vector_of_string = list()
        vector_of_string = ['0'] * max_characters * 36 # 26 letters in the english alphabet and 10 digits
        character_position = 0
        for character in domain_name:
                vector_of_string[character_position * 36 + character_order_dict[character]] = '1'
                character_position = character_position + 1
        return vector_of_string

def hash_string(domain_name,order_of_characters,dimension,W,A,B,hash_count):
	'''
		A method to hash a string, after it is firstly converted into vector representation
	'''
	hashed_values_list = list()
	converted_string = convert_string_to_vector(domain_name,order_of_characters,MAX_CHARS)
	for index in range(0,hash_count):
		hashed_value = lsh(converted_string,W,A[index],B[index],dimension)	
		hashed_values_list[index] = hashed_value
	return hashed_values_list

def lsh(vector,W,a,b,dimension):
	hashVal = floor((sum(a[i] * float(vector[i]) for  i in range(dimension)) + b)/W)
	return int(hashVal)

def generate_hash_parameters(dimension,W,hash_count):
	'''
		Generates lists A and B containing the parameters of the locality sensitive hash functions
	'''
	A = list()
	B = list()
	for index in range(0,hash_count):
		a = [normalvariate(0,1) for i in range(dimension)]
		b = uniform(0,W)
		A.append(a)
		B.append(b)
	return A,B

def print_lsbf_parameters(dimension,W,size,hash_count):
	'''
		A method to print the parameters of the locality sensitive Bloom filter
	'''
	print("dimension is ",dimension)
	print("W parameter is ",W)
	print("Size of LSBF is ",size)
	print("Number of hash functions used is ",hash_count)
	return None

def set_lsbf_parameters():
	'''
		A method to set the parameters of the locality sensitive Bloom filter
	'''
	dimension = DIMENSION
	W = W_parameter
	size = LSBF_SIZE
	hash_count = HASH_COUNT
	A,B = generate_hash_parameters(dimension,W,hash_count)
	print_lsbf_parameters(dimension,W,size,hash_count)
	return dimension,W,A,B,size,hash_count

def add_domain_name(domain_name,size,W,A,B):
	pass
	

def initialize_locality_sensitive_bf(size,zone_file,dimension,W,A,B,hash_count,order_of_characters):
	lsbf_array = bitarray(size)
	lsbf_array.setall(0)
	for line in open(zone_file,"r"):
		domain_name = line.rstrip()
		
	

def main():
	zone_file = "/home/nkostopoulos/ntua_names"
	dimension,W,A,B,size,hash_count = set_lsbf_parameters()
	order_of_characters = get_dictionary_of_character_order()
	initialize_locality_sensitive_bf(size,zone_file,dimension,W,A,B,hash_count,order_of_characters)
	return None


if __name__ == "__main__":
	print("Executing python script: ",sys.argv[0])
	main()
