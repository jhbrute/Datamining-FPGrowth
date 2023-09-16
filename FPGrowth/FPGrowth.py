
# FP-Growth algorithm using FP-tree data structure to find Frequent Patterns from input data.
# Running this script will create an FP-tree based on the input file, and will output a text file
# named "frequent_itemsets.txt" listing all frequent patterns based on the minimum support value.

# Undergraduate Project for COMP 5130, Auburn University, Dr. Yang Zhou
# Created by Joseph Hall
# Using Python3.10 on Visual Studio 2022

# Sample usage: run python script "FPGrowth.py" (IDE shell, windows powershell, command-line, etc.)
# Script requires input data file:
file_path = r"C:\Users\YOU\Documents\DATASETS\...\DATASET_NAME.csv"
# !!!Must replace above path with the actual path to your data file!!!
# If "copying as path" from windows' File Explorer, remember to keep the "r" before the path.
# To determine frequent patterns at different levels of minimum support, modify below:
min_support = 15
# To change default name of output text file, modify below:
output_file_name = 'frequent_itemsets.txt'

import os
import csv

# Class: linked list data structure
class FPNode:
    def __init__(self, item, count, parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None  # Link to the next node with the same item in the header table


# Loads input data from file path. Handles either .csv or .txt files.
def load_data_from_file(file_path):
    try:
        data = []
        with open(file_path, 'r') as file:
            # Detect file format based on extension
            if file_path.lower().endswith('.csv'):
                # Handle csv files
                csv_reader = csv.reader(file)
                for line in csv_reader:
                    # Skip empty or comment lines starting with '#'
                    if not line or line[0].startswith('#'):
                        continue
                    # Add elements to data list, removing empty fields from transaction
                    transaction = [str(item) for item in line if item.strip()]
                    data.append(transaction)
            else:
                # Assume it's text file instead of csv
                for line in file:
                    # Skip comment lines starting with '#'
                    if line.startswith('#'):
                        continue
                    # Split the line into two columns: FromNodeId and ToNodeId
                    # !!txt file must be formatted with tabs separating columns!!
                    from_node, to_node = map(int, line.strip().split('\t'))
                    data.append([from_node, to_node])
        return data
    #Error Handling
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred while loading the file '{file_path}': {e}")
        return None


# Constructs FP tree from data, only including items that are greater than or equal to min support.
def construct_initial_fp_tree(data, min_support):
    # Count the support of each item
    item_counts = {}
    for transaction in data:
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1

    # Filter out infrequent items based on min_support (prune)
    frequent_items = {item: count for item, count in item_counts.items() if count >= min_support}

    # Sort frequent items by support in descending order
    frequent_items = dict(sorted(frequent_items.items(), key=lambda x: x[1], reverse=True))

    # Construct the initial FP-tree
    root = FPNode(None, 0)
    header_table = {}
    for transaction in data:
        transaction = [item for item in transaction if item in frequent_items]
        transaction.sort(key=lambda x: frequent_items[x], reverse=True)
        insert_transaction(transaction, root, header_table)

    return root, header_table


# Handles transaction insertion used to contstruct FP-trees.
def insert_transaction(transaction, root, header_table):
    current_node = root
    for item in transaction:
        if item in current_node.children:
            current_node.children[item].count += 1
        else:
            new_node = FPNode(item, 1, parent=current_node)
            current_node.children[item] = new_node

            if item in header_table:
                last_node = header_table[item]
                while last_node.next is not None:
                    last_node = last_node.next
                last_node.next = new_node
            else:
                header_table[item] = new_node

        current_node = current_node.children[item]

# Extracts frequent patterns from the FP-tree based on min_support
def mine_frequent_itemsets(header_table, min_support, prefix=[]):
    frequent_itemsets = []
    for item, node in header_table.items():
        support_count = node.count
        if support_count >= min_support:
            current_itemset = prefix + [item]
            frequent_itemsets.append(current_itemset)

            # Create a conditional FP-tree for the current itemset
            conditional_tree_data = []
            while node is not None:
                path = get_prefix_path(node)
                if len(path) > 1:
                    conditional_tree_data.append(path[:-1])
                node = node.next

            conditional_tree, conditional_header_table = construct_initial_fp_tree(conditional_tree_data, min_support)
            if conditional_header_table is not None:
               conditional_frequent_itemsets = mine_frequent_itemsets(conditional_header_table, min_support, current_itemset)
               if conditional_frequent_itemsets:
                   frequent_itemsets.extend(conditional_frequent_itemsets)

    return frequent_itemsets
    
# Supporting function used in constructing/mining conditional trees.
# Finds the path to the root for input node.
def get_prefix_path(node):
    # Follow the node's parent links to build the prefix path
    prefix_path = []
    while node is not None:
        prefix_path.append(node.item)
        node = node.parent
    prefix_path.pop()  # Remove the root node
    prefix_path.reverse()

    return prefix_path

# Generates frequent itemsets output file based on found frequent itemsets and output_file_name.
def write_frequent_itemsets_to_file(frequent_itemsets, output_file_name):
    # Creates the 'output' folder if it doesn't exist
    output_folder = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Output frequent itemsets to a text file inside the output folder
    out_path = os.path.join(output_folder, output_file_name)
    out_base, out_ext = os.path.splitext(out_path)
 
    # If a file already exists with same name, add a suffix to this filename
    suffix = 1
    while os.path.exists(out_path):
        out_path = f"{out_base}_{suffix}{out_ext}"
        suffix += 1
    
    with open(out_path, 'w') as out_file:
        # Writes input data set file name and support value as comments at the top
        out_file.write(f"# Dataset: {dataset_name}\n# Minimum Support: {min_support}\n")

        # Writes the frequent itemsets to the file
        for itemset in frequent_itemsets:
            # Check if itemset is empty or contains only empty elements
            if any(item is not None for item in itemset):
                out_file.write(",".join(map(str, itemset)).rstrip() + "\n")
    print(f"Output can be found in: '{out_path}'.")


# Begin Script run
# Load data from the file
print("Loading data from file.")
data = load_data_from_file(file_path)
if data is None:
    # Error handling - file load error
    print("Exiting the program due to file loading error.")
    exit(1)

# Extract dataset file name from full path
dataset_name = os.path.basename(file_path)

# Construct the initial FP-tree and header table
print("Constructing Initial FP-tree.")
root, header_table = construct_initial_fp_tree(data, min_support)

# Mine frequent itemsets from the FP-tree
print("Mining Frequent Patterns.")
frequent_itemsets = mine_frequent_itemsets(header_table, min_support)

# Write frequent itemsets to output file
write_frequent_itemsets_to_file(frequent_itemsets, output_file_name)
