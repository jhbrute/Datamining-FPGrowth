Overview:
	This script (FPGrowth.py) will take a dataset as input and will output frequent patterns in the dataset based on a support value.

Datasets:
	The datasets can be either .csv or .txt files.  Each row in the dataset should 	represent a single transaction, and each column or entry in the row represents an 	item in a transaction. The input dataset's rows should be comma-separated in a .csv 	file, or tab-separated 	in a .txt file. The script needs the location of an input 	dataset, which must be changed in the source code under the variable named 	"file_path".

Running the Script:
	Before running the python (3.10) file "FPGrowth" it is recommended to first open it 	with a python IDE such as Visual Studio. This is because the "file_path" variable 	must be changed to represent the file path to your input dataset.  

Minimum Support Values:
	In this implementation, support values are integers representing frequency 	thresholds. They are not normalized by total transactions, and thus do not represent 	ratios of transactions. The minimum support value "min_support" can and should be 	changed to generate different frequent itemsets.

Output:
	The output .txt file is named by default "frequent_patterns.txt" but the name can 	also be changed in source code by modifying the variable "output_file_name".
	If an output .txt file already exists with the same name, successive files will be 	generated with the same name plus a suffix (integer).

All of these variables (file_path, min_support, output_file_name) are available to change at the top of the source code.
