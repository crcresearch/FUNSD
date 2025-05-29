#!/usr/bin/env python3

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Union

# Get the directory of this script and import schema
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from schema import FUNSDQAPair, FUNSDQADataset


def validate_qa_file(file_path: Union[str, Path]) -> bool:
    """
    Validate a QA JSON file against the schema.
    
    Args:
        file_path: Path to the QA JSON file
        
    Returns:
        bool: True if validation succeeds, False otherwise
    """
    try:
        # Load the JSON data
        path = Path(file_path)
        if not path.exists():
            print(f"Error: File {path} does not exist")
            return False
            
        json_data = json.loads(path.read_text())
        
        # Check if it's a list (array of QA pairs)
        if isinstance(json_data, list):
            # Validate each QA pair
            valid_pairs = []
            for i, qa_pair in enumerate(json_data):
                try:
                    validated_pair = FUNSDQAPair(**qa_pair)
                    valid_pairs.append(validated_pair)
                except Exception as e:
                    print(f"Error in QA pair #{i+1} (ID: {qa_pair.get('id', 'unknown')}): {str(e)}")
                    return False
            
            # Create dataset from validated pairs
            dataset = FUNSDQADataset(qa_pairs=valid_pairs)
            print(f"Validation successful! Found {len(valid_pairs)} valid QA pairs.")
            return True
            
        else:
            print("Error: JSON file should contain a list of QA pairs")
            return False
            
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not a valid JSON file")
        return False
        
    except Exception as e:
        print(f"Error during validation: {str(e)}")
        return False


def main():
    """Main function to validate QA files from command line."""
    if len(sys.argv) < 2:
        print("Usage: python validate_qa.py <qa_file.json> [qa_file2.json ...]")
        sys.exit(1)
        
    all_valid = True
    for file_path in sys.argv[1:]:
        print(f"\nValidating {file_path}...")
        if not validate_qa_file(file_path):
            all_valid = False
            
    if all_valid:
        print("\nAll files validated successfully!")
        sys.exit(0)
    else:
        print("\nValidation failed for one or more files.")
        sys.exit(1)


if __name__ == "__main__":
    main() 