""" Module with functionalities for blocking based on a dictionary of records,
    where a blocking function must return a dictionary with block identifiers
    as keys and values being sets or lists of record identifiers in that block.
"""

import random
import comparison
import numpy as np
import cudf

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

def simpleBlocking(gdf, blk_attr_list):
    """Build the blocking index data structure (dictionary) to store blocking
     key values (BKV) as keys and the corresponding list of record identifiers.

     A blocking is implemented that simply concatenates attribute values.

     Parameter Description:
       gdf (cudf.DataFrame): A cuDF DataFrame containing the records.
       blk_attr_list (list): List of blocking key attributes to use.

     This method returns a dictionary with blocking key values as its keys and
     list of record identifiers as its values (one list for each block).
    """

    block_dict = {}

    print('Run simple blocking:')
    print(f'  List of blocking key attributes: {blk_attr_list}')
    print(f'  Number of records to be blocked: {len(gdf)}')

    gdf = gdf.reset_index()
    gdf = gdf.rename(columns={'index': 'rec_id'})

    # Create the blocking key value by concatenating specified attribute columns
    gdf['bkv'] = ''
    for col in blk_attr_list:
        gdf['bkv'] = gdf['bkv'] + gdf[col].astype(str)

    grouped = gdf.groupby('bkv')
    for name, group in grouped:
        block_dict[name] = group['rec_id'].to_arrow().to_pylist()

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

def canopy_clustering(gdf, blk_attr_list, T1, T2):
    """
    Implements an optimized canopy clustering for blocking records using GPU acceleration.

    Parameters:
        gdf (cudf.DataFrame): The DataFrame containing the records.
        blk_attr_list (list): List of attribute names to use for clustering.
        T1 (float): The loose distance threshold.
        T2 (float): The tight distance threshold (T2 < T1).

    Returns:
        dict: A dictionary with block identifiers as keys and values being lists of
              record identifiers in that block.
    """
    block_dict = {}
    
    # Convert the blk_attr_list to cudf series
    #
    gdf_attrs = [gdf[attr].astype(str).str.lower() for attr in blk_attr_list]
    
    # Get the record identifiers
    #
    rec_ids = gdf.index.to_arrow().to_pylist()
    unassigned_rec_indices = set(range(len(rec_ids)))

    total_records = len(rec_ids)
    progress_step = 10
    next_progress = progress_step

    while unassigned_rec_indices:
        assigned_records = total_records - len(unassigned_rec_indices)
        progress = (assigned_records / total_records) * 100
        if progress >= next_progress:
            print(f"  Canopy clustering progress: {int(progress)}%")
            next_progress += progress_step

        center_index = random.choice(list(unassigned_rec_indices))
        
        # Get the canopy center attributes
        #
        center_attrs = [s.iloc[center_index] for s in gdf_attrs]

        # Calculate distances from the center to all other points
        #
        distances = None
        for i, attr_name in enumerate(blk_attr_list):
            
            # Get the attribute values for all records
            #
            all_vals = gdf_attrs[i]
            
            # Create a series with the center attribute value
            #
            center_attr_series = cudf.Series([center_attrs[i]] * len(all_vals))

            # Calculate the distance for the current attribute
            #
            sim = comparison.jaccard_comp_gpu(center_attr_series, all_vals)
            dist = 1.0 - sim
            
            if distances is None:
                distances = dist
            else:
                distances += dist
        
        distances /= len(blk_attr_list)
        
        # Get the indices of records within the loose threshold T1
        #
        canopy_indices = distances[distances <= T1].index.to_arrow().to_pylist()
        
        # Get the indices of records within the tight threshold T2
        #
        close_indices = distances[distances <= T2].index.to_arrow().to_pylist()

        # Remove the close indices from the unassigned set
        #
        unassigned_rec_indices.difference_update(close_indices)

        # Create the block key value from the center attributes
        #
        canopy_bkv = "".join([str(attr) for attr in center_attrs])
        
        # Get the record identifiers for the canopy
        #
        canopy_rec_ids = [rec_ids[i] for i in canopy_indices]

        if canopy_bkv in block_dict:
            block_dict[canopy_bkv].extend(canopy_rec_ids)
        else:
            block_dict[canopy_bkv] = canopy_rec_ids

    print(f"  Generated {len(block_dict)} blocks based on canopy clustering.")

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
