# A program to generate a smaller data set from a provided master data set.
#
# Important: Must be run under Python 3
#
# Peter Christen, Aug 2020
# Updated by Anushka Vidanage, Jul 2023
# Updated by Charini Nanayakkara, Jul 2024
# Updated by Graham Williams, Jul 2025
#
# Usage:
#
#  python3 generate-student-dataset.py [anu_id] [master_data_set_name]
#
# -----------------------------------------------------------------------------

import gzip
import hashlib
import random
import sys

# Check the program is run under Python3
#
version = sys.version_info[0]
if (version != 3):
  print('*** Program must be run using Python 3 ***')
  sys.exit()

anu_id = sys.argv[1].lower()
assert len(anu_id) == 8, 'Invalid ANU ID provided'
assert anu_id[0] == 'u', ('Invalid ANU ID provided', anu_id[0])
assert anu_id[1:].isdigit() == True, 'Invalid ANU ID provided'

salt = 'sem2/2025'

md5_anu_id = hashlib.md5(anu_id.encode('utf-8')).hexdigest()

master_data_set_name = sys.argv[2]
assert master_data_set_name.endswith('.csv.gz')

student_data_set_name = 'data_wrangling_medical_2025_%s.csv' % (anu_id)

master_data_set_list = []
master_file = gzip.open(master_data_set_name, mode='rt')
header_line = master_file.readline()

for rec in master_file:
  master_data_set_list.append(rec)
assert len(master_data_set_list) == 100000, len(master_data_set_list)
master_file.close()

random.seed(anu_id+salt)

student_data_set_list = random.sample(master_data_set_list, 20000)

student_file = open(student_data_set_name, 'w')
student_file.write(header_line)

md5_str = ''
for rec in student_data_set_list:
  student_file.write(rec)

  md5_str += rec.strip()  # Remove OS depdendent new lines characters

student_file.close()

md5_data_set = hashlib.md5(md5_str.encode('utf-8')).hexdigest()

print('-'*40)
print()
print('Your student data set for the data wrangling 2025 assignments')
print('has been generated and written into file:')
print()
print(' ',student_data_set_name)
print()
print('Your ANU ID check code is:          ', md5_anu_id[:8])
print('Your student data set check code is:', md5_data_set[:12])
print()
print('  *** Check this pair of numbers is in the list provided on Wattle')
print('  *** If not contact the course convenor.')
print()
print('#### ', md5_anu_id[:8],'/',md5_data_set[:12])
print()
