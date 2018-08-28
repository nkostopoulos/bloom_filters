import string

MAX_CHARS = 20 # the maximum number of characters in a domain name

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

def read_domain_names_from_file(file_name,order_of_characters):
	write_file = "/home/nkostopoulos/paper/converted_lsbf"
	write_file_descr = open(write_file,"w")
	for line in open(file_name,"r"):
		domain_name = line.rstrip()
		get_vector = convert_string_to_vector(domain_name,order_of_characters,MAX_CHARS)
		spacified_list = ' '.join(get_vector)
		write_file_descr.write(spacified_list + '\n')
	return None

def main():
	'''
		The main method of the Python script
	'''
	read_file_name = "/home/nkostopoulos/paper/lsbf_names"
	order_of_characters = get_dictionary_of_character_order()
	read_domain_names_from_file(read_file_name,order_of_characters)
	return None

if __name__ == "__main__":
	main()
