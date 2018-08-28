import string
import sys

def get_dictionary_of_character_order():
	'''
		Returns the dictionary with the order of letters and digits, e.g. a is 0, b is 1, .... , z is 25, 0 is 26, 1 is 27, 9 is 35
	'''
	character_order_dict = dict()
	letter_list = string.ascii_lowercase
	digit_list = '0123456789-\\'
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
	vector_of_string = [0] * 38 # 26 letters in the english alphabet, 10 digits, 2 special characters
	for character in domain_name:
		character_position = character_order_dict[character]
		vector_of_string[character_position] = vector_of_string[character_position] + 1
	return vector_of_string

def spacify_list(vector):
	out = str(vector[0])
	for index in range(1,len(vector)):
		out = out + " " + str(vector[index])
	return out

def read_domain_names_from_file(file_name,order_of_characters):
	write_file = "/home/nkostopoulos/LSBF/dataset/dns_million_random_converted"
	write_file_descr = open(write_file,"w")
        counter = 0
	for line in open(file_name,"r"):
                counter = counter + 1
                if (counter % 100000) == 0:
                    print(counter)
		domain_name = line.rstrip()
		get_vector = convert_string_to_vector(domain_name,order_of_characters)
		spacified_list = spacify_list(get_vector)
		write_file_descr.write(spacified_list + '\n')
                del domain_name,get_vector,spacified_list
	return None


def main():
	'''
		The main method of the Python script
	'''
	read_file_name = "/home/nkostopoulos/LSBF/dataset/dns_million_DGAs"
	order_of_characters = get_dictionary_of_character_order()
	read_domain_names_from_file(read_file_name,order_of_characters)
	return None

if __name__ == "__main__":
	main()
