""" Module with functionalities for blocking based on a dictionary of records,
    where a blocking function must return a dictionary with block identifiers
    as keys and values being sets or lists of record identifiers in that block.
"""

import random
import comparison
import numpy as np

# =============================================================================

def noBlocking(rec_dict):
  """A function which does no blocking but simply puts all records from the
     given dictionary into one block.

     Parameter Description:
       rec_dict : Dictionary that holds the record identifiers as keys and
                  corresponding list of record values
  """

  print("Run 'no' blocking:")
  print('  Number of records to be blocked: '+str(len(rec_dict)))
  

  rec_id_list = list(rec_dict.keys())

  block_dict = {'all_rec':rec_id_list}

  return block_dict

# -----------------------------------------------------------------------------

def simpleBlocking(rec_dict, blk_attr_list):
  """Build the blocking index data structure (dictionary) to store blocking
     key values (BKV) as keys and the corresponding list of record identifiers.

     A blocking is implemented that simply concatenates attribute values.

     Parameter Description:
       rec_dict      : Dictionary that holds the record identifiers as keys
                       and corresponding list of record values
       blk_attr_list : List of blocking key attributes to use

     This method returns a dictionary with blocking key values as its keys and
     list of record identifiers as its values (one list for each block).

     Examples:
       If the blocking is based on 'postcode' then:
         block_dict = {'2000': [rec1_id, rec2_id, rec3_id, ...],
                       '2600': [rec4_id, rec5_id, ...],
                         ...
                      }
       while if the blocking is based on 'postcode' and 'gender' then:
         block_dict = {'2000f': [rec1_id, rec3_id, ...],
                       '2000m': [rec2_id, ...],
                       '2600f': [rec5_id, ...],
                       '2600m': [rec4_id, ...],
                        ...
                      }
  """

  block_dict = {}  # The dictionary with blocks to be generated and returned

  print('Run simple blocking:')
  print('  List of blocking key attributes: '+str(blk_attr_list))
  print('  Number of records to be blocked: '+str(len(rec_dict)))
  
  for (rec_id, rec_values) in rec_dict.items():

    rec_bkv = ''  # Initialise the blocking key value for this record

    # Process selected blocking attributes
    # 
    for attr in blk_attr_list:
      attr_val = rec_values[attr]
      rec_bkv += attr_val

    # Insert the blocking key value and record into blocking dictionary
    # 
    if (rec_bkv in block_dict): # Block key value in block index

      # Only need to add the record
      # 
      rec_id_list = block_dict[rec_bkv]
      rec_id_list.append(rec_id)

    else: # Block key value not in block index

      # Create a new block and add the record identifier
      # 
      rec_id_list = [rec_id]

    block_dict[rec_bkv] = rec_id_list  # Store the new block

  return block_dict

# -----------------------------------------------------------------------------

def phoneticBlocking(rec_dict, blk_attr_list):
  """Build the blocking index data structure (dictionary) to store blocking
     key values (BKV) as keys and the corresponding list of record identifiers.

     A blocking is implemented that concatenates Soundex encoded values of
     attribute values.

     Parameter Description:
       rec_dict      : Dictionary that holds the record identifiers as keys
                       and corresponding list of record values
       blk_attr_list : List of blocking key attributes to use

     This method returns a dictionary with blocking key values as its keys and
     list of record identifiers as its values (one list for each block).
  """

  block_dict = {}  # The dictionary with blocks to be generated and returned

  print('Run phonetic blocking:')
  print('  List of blocking key attributes: '+str(blk_attr_list))
  print('  Number of records to be blocked: '+str(len(rec_dict)))
  
  for (rec_id, rec_values) in rec_dict.items():
    #print(f'record dictionary: {rec_id} and {rec_values}')

    rec_bkv = ''  # Initialise the blocking key value for this record

    # Process selected blocking attributes
    # 
    for attr in blk_attr_list:
      attr_val = rec_values[attr]

      # *********** Implement Soundex function here *********

      # Add your code here
      if attr_val == '':
        rec_bkv += 'z000'  # Often used as Soundex code for empty values
      else: 
        attr_val = attr_val.lower()
        sndx_val = attr_val[0] # keep first letter

        for char in attr_val[1:]:
            if char in 'aeiouyhw':
                pass
            elif char in 'bfpv':
                if sndx_val[-1] != '1': # dont add duplicates of digits
                    sndx_val += '1'
            elif char in 'cgjkqsxz':
                if sndx_val[-1] != '2':  # Don't add duplicates of digits
                    sndx_val += '2'
            elif char in 'dt':
                if sndx_val[-1] != '3':  # Don't add duplicates of digits
                    sndx_val += '3'
            elif char in 'l':
                if sndx_val[-1] != '4':  # Don't add duplicates of digits
                    sndx_val += '4'
            elif char in 'mn':
                if sndx_val[-1] != '5':  # Don't add duplicates of digits
                    sndx_val += '5'
            elif char in 'r':
                if sndx_val[-1] != '6':  # Don't add duplicates of digits
                    sndx_val += '6'
        if len(sndx_val) < 4:
                    sndx_val += '000'
        # set max lenth to four 
        sndx_val = sndx_val[:4]
        rec_bkv += sndx_val

      # ************ End of your Soundex code *********************************

    # Insert the blocking key value and record into blocking dictionary
    # 
    if (rec_bkv in block_dict): # Block key value in block index

      # Only need to add the record
      # 
      rec_id_list = block_dict[rec_bkv]
      rec_id_list.append(rec_id)

    else: # Block key value not in block index

      # Create a new block and add the record identifier
      # 
      rec_id_list = [rec_id]

    block_dict[rec_bkv] = rec_id_list  # Store the new block

  return block_dict

# -----------------------------------------------------------------------------

def slkBlocking(rec_dict, fam_name_attr_ind, giv_name_attr_ind, 
                dob_attr_ind, gender_attr_ind):
  """Build the blocking index data structure (dictionary) to store blocking
     key values (BKV) as keys and the corresponding list of record identifiers.

     This function should implement the statistical linkage key (SLK-581)
     blocking approach as used in real-world linkage applications:

     http://www.aihw.gov.au/WorkArea/DownloadAsset.aspx?id=60129551915

     A SLK-581 blocking key is the based on the concatenation of:
     - 3 letters of family name
     - 2 letters of given name
     - Date of birth
     - Sex

     Parameter Description:
       rec_dict          : Dictionary that holds the record identifiers as
                           keys and corresponding list of record values
       fam_name_attr_ind : The number (index) of the attribute that contains
                           family name (last name) 
       giv_name_attr_ind : The number (index) of the attribute that contains
                           given name (first name)
       dob_attr_ind      : The number (index) of the attribute that contains
                           date of birth
       gender_attr_ind   : The number (index) of the attribute that contains
                           gender (sex)

     This method returns a dictionary with blocking key values as its keys and
     list of record identifiers as its values (one list for each block).
  """

  block_dict = {}  # The dictionary with blocks to be generated and returned

  print('Run SLK-581 blocking:')
  print('  Number of records to be blocked: '+str(len(rec_dict)))
  
  for (rec_id, rec_values) in rec_dict.items():

    rec_bkv = ''  # Initialise the blocking key value for this record
 
    # *********** Implement SLK-581 function here ***********

    # Family Name (2nd, 3rd, 5th letters)
    fam_name = rec_values[fam_name_attr_ind]
    slk_fam_name_part = ""
    if not fam_name:
        slk_fam_name_part = "222" # 3 chars for family name
    else:
        alpha_chars_fam = [char for char in fam_name.lower() if char.isalpha()]
        
        # 2nd letter (index 1)
        if 1 < len(alpha_chars_fam):
            slk_fam_name_part += alpha_chars_fam[1]
        else:
            slk_fam_name_part += '2'
            
        # 3rd letter (index 2)
        if 2 < len(alpha_chars_fam):
            slk_fam_name_part += alpha_chars_fam[2]
        else:
            slk_fam_name_part += '2'
            
        # 5th letter (index 4)
        if 4 < len(alpha_chars_fam):
            slk_fam_name_part += alpha_chars_fam[4]
        else:
            slk_fam_name_part += '2'
            
    rec_bkv += slk_fam_name_part.upper()

    # Given Name (2nd, 3rd letters)
    giv_name = rec_values[giv_name_attr_ind]
    slk_giv_name_part = ""
    if not giv_name:
        slk_giv_name_part = "22" # 2 chars for given name
    else:
        alpha_chars_giv = [char for char in giv_name.lower() if char.isalpha()]
        
        # 2nd letter (index 1)
        if 1 < len(alpha_chars_giv):
            slk_giv_name_part += alpha_chars_giv[1]
        else:
            slk_giv_name_part += '2'
            
        # 3rd letter (index 2)
        if 2 < len(alpha_chars_giv):
            slk_giv_name_part += alpha_chars_giv[2]
        else:
            slk_giv_name_part += '2'
            
    rec_bkv += slk_giv_name_part.upper()

    # DoB structure we use: dd/mm/yyyy

    # Get date of birth
    # 
    dob = rec_values[dob_attr_ind]
    if dob == '':
        dob = '01/01/1900'

    dob_list = dob.split('/')

    # Add some checks
    # 
    if len(dob_list[0]) < 2:
        dob_list[0] = '0' + dob_list[0]  # Add leading zero for days < 10
    if len(dob_list[1]) < 2:
        dob_list[1] = '0' + dob_list[1]  # Add leading zero for months < 10

    dob = ''.join(dob_list)  # Create: dd/mm/yyyy

    assert len(dob) == 8, dob

    rec_bkv += dob

    # Get gender
    # 
    gender = rec_values[gender_attr_ind].lower()

    if gender == 'm':
        rec_bkv += '1'
    elif gender == 'f':
        rec_bkv += '2'
    else:
        rec_bkv += '9'

    # ************ End of your SLK-581 code ***********************************

    # Insert the blocking key value and record into blocking dictionary
    # 
    if (rec_bkv in block_dict): # Block key value in block index

      # Only need to add the record
      # 
      rec_id_list = block_dict[rec_bkv]
      rec_id_list.append(rec_id)

    else: # Block key value not in block index

      # Create a new block and add the record identifier
      # 
      rec_id_list = [rec_id]

    block_dict[rec_bkv] = rec_id_list  # Store the new block

  return block_dict

# -----------------------------------------------------------------------------

# Extra task if you have time:
# - Implement canopy clustering based blocking as described in the lectures
#   and the Data Matching book

def _calculate_record_distance(record1, record2, blk_attr_list, distance_metric):
  """
  Calculates the combined distance between two records based on specified attributes.

  Parameters:
    record1 (list): The first record (list of attribute values).
    record2 (list): The second record (list of attribute values).
    blk_attr_list (list): List of attribute indices to use for distance calculation.
    distance_metric (function): A function that takes two attribute 
                                values and returns a distance (float).

  Returns:
    float: The average distance between the two records 
           across the specified attributes.
  """
  distances = []
  for attr_index in blk_attr_list:
    val1 = record1[attr_index] if attr_index < len(record1) else ''
    val2 = record2[attr_index] if attr_index < len(record2) else ''

    # Ensure values are lowercased for consistent comparison
    val1 = val1.lower()
    val2 = val2.lower()

    distances.append(distance_metric(val1, val2))

  if not distances:
    return 0.0 # Or handle as an error, depending on desired behavior for empty blk_attr_list
  return sum(distances) / len(distances)


def canopy_clustering(rec_dict, blk_attr_list, distance_metric, T1, T2):
  """
  Implements canopy clustering for blocking records.

  Parameters:
    rec_dict (dict): Dictionary that holds the record identifiers as keys and
                     corresponding list of record values.
    blk_attr_list (list): List of attribute indices to use for clustering.
    distance_metric (function): A function that takes two attribute values and returns a distance (float).
    T1 (float): The loose distance threshold.
    T2 (float): The tight distance threshold (T2 < T1).

  Returns:
    dict: A dictionary with block identifiers as keys and values being lists of
          record identifiers in that block.
  """
  block_dict = {}
  unassigned_records = set(rec_dict.keys())

  # This set will track which attribute-based blocking keys have already been used
  # to prevent duplicate blocks if multiple canopy centers generate the same BKV
  generated_bkv_to_canopy_center = {}


  while unassigned_records:
    canopy_center_id = random.choice(list(unassigned_records))
    current_canopy_records = []

    # Generate the blocking key value for this canopy based on its center's attributes
    # This is the key that will be used to match blocks across datasets A and B
    canopy_bkv = ""
    for attr_index in blk_attr_list:
        val = rec_dict[canopy_center_id][attr_index] if attr_index < len(rec_dict[canopy_center_id]) else ''
        canopy_bkv += val.lower().strip() # Added .strip() for robustness


    # If this specific attribute-based BKV has already been used by a previous canopy,
    # we might want to skip creating a new canopy centered here, or merge.
    # For now, let's allow it to create a new entry if the actual center is different.
    # The 'block_dict' will handle merging if the 'canopy_bkv' is the same.


    records_to_check = list(unassigned_records) # Iterate over a copy

    for record_id in records_to_check:
      distance = _calculate_record_distance(
          rec_dict[canopy_center_id],
          rec_dict[record_id],
          blk_attr_list,
          distance_metric
      )

      if distance <= T1:
        current_canopy_records.append(record_id)

      if distance <= T2:
        unassigned_records.discard(record_id)


    # Add all records in the current canopy to the block_dict under the generated canopy_bkv
    # This is critical for cross-dataset compatibility.
    if canopy_bkv in block_dict:
        block_dict[canopy_bkv].extend(current_canopy_records)
    else:
        block_dict[canopy_bkv] = current_canopy_records

  print(f"  Generated {len(block_dict)} blocks based on canopy clustering.") # Added for debug

  return block_dict
# -----------------------------------------------------------------------------

def printBlockStatistics(blockA_dict, blockB_dict):
  """Calculate and print some basic statistics about the generated blocks
  """

  print('Statistics of the generated blocks:')

  numA_blocks = len(blockA_dict)
  numB_blocks = len(blockB_dict)

  block_sizeA_list = []
  for rec_id_list in blockA_dict.values():  # Loop over all blocks
    block_sizeA_list.append(len(rec_id_list))

  block_sizeB_list = []
  for rec_id_list in blockB_dict.values():  # Loop over all blocks
    block_sizeB_list.append(len(rec_id_list))

  print('Dataset A number of blocks generated: %d' % (numA_blocks))
  if numA_blocks > 0:
    print('    Minimum block size: %d' % (min(block_sizeA_list)))
    print('    Average block size: %.2f' % \
          (float(sum(block_sizeA_list)) / len(block_sizeA_list)))
    print('    Maximum block size: %d' % (max(block_sizeA_list)))
  else:
    print('    No blocks generated for Dataset A.')
  print('')

  print('Dataset B number of blocks generated: %d' % (numB_blocks))
  if numB_blocks > 0:
    print('    Minimum block size: %d' % (min(block_sizeB_list)))
    print('    Average block size: %.2f' % \
          (float(sum(block_sizeB_list)) / len(block_sizeB_list)))
    print('    Maximum block size: %d' % (max(block_sizeB_list)))
  else:
    print('    No blocks generated for Dataset B.')
  print('')

# -----------------------------------------------------------------------------

# End of program.
