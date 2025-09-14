## Task 1 (3 marks): 
Generate two strings of numbers based on your ANU ID (excluding the first character ‘u’):
– s1 is the string ‘123’ concatenated with the first four digits of your ANU ID.
– s2 is the string ‘123’ concatenated with the last four digits of your ANU ID. Include any leading zeros.
For example, if your ANU ID is u9800765 then s1 = ‘1239800’ and s2 = ‘1230765’
Now manually calculate the following similarities between these two strings and include in your assignment both your workings (equations or edit matrices) as well as the final results for:
1. The Dice coefficient similarity based on unigrams (q = 1).
2. The Jaccard similarity based on bigrams (q = 2).
3. The bag distance similarity
4. The Levenshtein edit distance between the two strings, assuming a cost of 2 for substitutions, cost of 1 for inserts,
and cost of 1 for deletes.
5. In a couple of sentences, explain the relationship between the bag distance and the edit distance.
Round the final numerical results to two decimal places. For sub-task 4 you must show the full edit matrix as your workings.

### Answers:
my ANU ID: u7283652
string 1 = 1237283
string 2 = 1233652

1. Dice coefficient of s1 and s2 based on unigrams.
    * s1_{q=1}: '1' '2' '3' '7' '8' (must be sets after extracting unigrams)
    * s2_{q=1}: '1' '2' '3' '6' '5'
    matching_window = floor(max(7,7) / 2) - 1 = 2
    dice_sim = 2 * len(s1_{q=1} & s2_{q=2}) / (len(s1_{q=1}) + len(s2_{q=2}))
    dice_sim = 2 * 3 / (5 + 5) = 6 / 10 = 0.60

2. Jaccard similarity based on bigrams 
    * s1_{q=2}: '12' '23' '37' '72' '28' '83'
    * s2_{q=2}: '12' '23' '33' '36' '65' '52'
    matching_window = floor(max(6, 6) / 2) - 1 = 2 
    dice_jacc = 2 / (6 + 6 - 2) = 0.20
