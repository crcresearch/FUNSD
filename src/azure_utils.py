#%%
import pandas as pd
import json
import jq
import os
import re
from pathlib import Path
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential


#%%
def analyze_handwritten_content(data):
    # Look for handwritten styles
    query = '.styles[] | select(.is_handwritten == true) | .spans'
    compiled_query = jq.compile(query)
    result = compiled_query.input(data).all()
    
    contains_handwritten = len(result) > 0
    handwritten_elements = []
    handwritten_polygons = []

    if contains_handwritten:
        hw_offsets = [r['offset'] for r in result[0]]
        hw_lengths = [r['length'] for r in result[0]]

        for hw_offset, hw_length in zip(hw_offsets, hw_lengths):
            # Look for content of specific span
            query = f'.content[({hw_offset}):{hw_offset+hw_length}]'
            content = jq.compile(query).input(data).first()
            handwritten_elements.append(content)
            # retrieve the polygon of the span
            query = f'.pages[].lines[] | select(any(.spans[]; .offset == {hw_offset} and .length == {hw_length})) | .polygon'
            polygon = []
            try:
                polygon = jq.compile(query).input(data).all()
            except StopIteration as e:
                pass
            handwritten_polygons.append(polygon)

    return contains_handwritten, handwritten_elements, handwritten_polygons

#%%
def process_and_save_annotations(directory):
    seqnums = []
    contains_hw_elements = []
    hw_elements_list = []
    hw_polygons_list = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            seqnum = int(re.search(r'\d+', filename).group(0))
            file_path = os.path.join(directory, filename)
            with open(file_path) as f:
                data = json.load(f)
            contains_hw, hw_elements, hw_polygons = analyze_handwritten_content(data)
            contains_hw_elements.append(contains_hw)
            hw_elements_list.append(hw_elements)
            hw_polygons_list.append(hw_polygons)
            seqnums.append(seqnum)

    df = pd.DataFrame({
        'imageref': seqnums,
        'contains_hw_elements': contains_hw_elements,
        'hw_elements': hw_elements_list,
        'hw_polygons': hw_polygons_list
    })

    df = df.sort_values('imageref').set_index('imageref')
    
    df = df.explode(['hw_elements','hw_polygons']).reset_index(drop=False)

    # flatten the hw_polygons list
    def flatten(x):
        try:
            return x[0]
        except IndexError:
            return x
        except TypeError:
            return x
    df['hw_polygons'] = df['hw_polygons'].apply(flatten)

    output_file = os.path.join(directory, 'hw_annotations.csv')
    df.to_csv(output_file)
    
    return output_file, df

# # Example usage:
# directory = 'datasets/funsd_plus/training_data/annotations_azure_model__prebuilt_read'
# output_csv = process_and_save_annotations(directory)
# print(f"Annotations saved to: {output_csv}")

def analyze_document_with_layout(client, document_path, output_path=None, output_content_format="markdown", return_dict=False, raw_response=False):
    """
    Analyze a document using Azure's prebuilt-document model which includes
    key-value pairs, tables, and layout information.
    
    Args:
        client: Azure Document Intelligence client
        document_path (str): Path to the document to analyze
        output_path (str, optional): Path to save the JSON result
        output_content_format (str, optional): Format for the content output. 
            Options are "text" or "markdown". Defaults to "markdown".
        return_dict (bool, optional): If True, returns the result as a dictionary
            instead of the Azure result object. Defaults to False.
        raw_response (bool, optional): If True, returns the raw JSON response
            from Azure API. This takes precedence over return_dict. Defaults to False.
        
    Returns:
        The analysis result as an Azure object, dictionary, or raw JSON based on parameters
    """
    # Use prebuilt-document model instead of prebuilt-layout
    model_id = "prebuilt-document"
    
    with open(document_path, "rb") as document:
        poller = client.begin_analyze_document(
            model_id, 
            document=document,
            output_content_format=output_content_format
        )
    
    result = poller.result()
    
    # Save result if output path is provided
    if output_path:
        if raw_response:
            # Save raw JSON response
            raw_json = json.loads(result._raw_response.content)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(raw_json, f, indent=2, ensure_ascii=False)
        else:
            save_azure_result(result, output_path)
    
    # Return raw JSON if requested
    if raw_response:
        return json.loads(result._raw_response.content)
    
    # Return as dictionary if requested
    if return_dict:
        return azure_result_to_dict(result)
    
    return result

def azure_result_to_dict(result):
    """
    Convert Azure Document Intelligence result to a dictionary.
    
    Args:
        result: Azure Document Intelligence result
        
    Returns:
        dict: Dictionary representation of the result
    """
    # Handle non-object types
    if not hasattr(result, '__dict__'):
        return result
    
    # Convert the result to a dictionary
    result_dict = {}
    
    # Add all public attributes
    for attr in dir(result):
        # Skip private attributes and methods
        if attr.startswith('_') or callable(getattr(result, attr)):
            continue
        
        value = getattr(result, attr)
        
        # Handle lists
        if isinstance(value, list):
            result_dict[attr] = [azure_result_to_dict(item) for item in value]
        # Handle nested objects
        elif hasattr(value, '__dict__'):
            result_dict[attr] = azure_result_to_dict(value)
        # Handle basic types
        else:
            result_dict[attr] = value
            
    return result_dict

def extract_key_value_pairs(result):
    """
    Extract key-value pairs from Azure Document Intelligence result.
    
    Args:
        result: Azure Document Intelligence result
        
    Returns:
        list: List of dictionaries containing key-value pairs
    """
    pairs = []
    
    for kv in result.key_value_pairs:
        pair = {
            'key': kv.key.content if kv.key else None,
            'value': kv.value.content if kv.value else None,
            'key_confidence': kv.confidence if hasattr(kv, 'confidence') else None,
            'key_bounding_box': kv.key.polygon if kv.key else None,
            'value_bounding_box': kv.value.polygon if kv.value else None
        }
        pairs.append(pair)
    
    return pairs

def extract_tables(result):
    """
    Extract tables from Azure Document Intelligence result.
    
    Args:
        result: Azure Document Intelligence result
        
    Returns:
        list: List of pandas DataFrames containing table data
    """
    tables = []
    
    for table in result.tables:
        # Convert table to 2D list
        rows = []
        for i in range(table.row_count):
            row = []
            for j in range(table.column_count):
                cell_content = ''
                # Find cell at position (i,j)
                for cell in table.cells:
                    if cell.row_index == i and cell.column_index == j:
                        cell_content = cell.content
                        break
                row.append(cell_content)
            rows.append(row)
        
        # Convert to DataFrame
        df = pd.DataFrame(rows)
        # If first row contains headers, use it as column names
        if hasattr(table, 'has_header') and table.has_header:
            df.columns = df.iloc[0]
            df = df[1:]
        
        tables.append({
            'data': df,
            'row_count': table.row_count,
            'column_count': table.column_count,
            'cells': [
                {
                    'content': cell.content,
                    'row_index': cell.row_index,
                    'column_index': cell.column_index,
                    'bounding_box': cell.polygon if hasattr(cell, 'polygon') else cell.bounding_regions[0].polygon if cell.bounding_regions else None
                }
                for cell in table.cells
            ]
        })
    
    return tables

def save_azure_result(result, output_path):
    """
    Save Azure Document Intelligence result to a JSON file.
    
    Args:
        result: Azure Document Intelligence result
        output_path (str): Path where to save the JSON file
    """
    # Convert result to dictionary
    result_dict = azure_result_to_dict(result)
    
    # Ensure the directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, indent=2, ensure_ascii=False)
    
    print(f"Azure result saved to: {output_path}")

def inspect_analyze_result(result):
    """
    Inspect and print all available methods and attributes of an Azure AnalyzeResult object.
    
    Args:
        result: Azure Document Intelligence AnalyzeResult object
    
    Returns:
        dict: Dictionary containing categorized methods and attributes
    """
    # Get all attributes and methods
    all_items = dir(result)
    
    # Categorize items
    info = {
        'public_attributes': [],
        'public_methods': [],
        'private_items': []
    }
    
    for item in all_items:
        # Skip private/special methods
        if item.startswith('_'):
            info['private_items'].append(item)
            continue
            
        # Get the attribute/method
        attr = getattr(result, item)
        
        # Check if it's callable (method) or not (attribute)
        if callable(attr):
            info['public_methods'].append(item)
        else:
            info['public_attributes'].append(item)
    
    # Print information
    print("\nPublic Attributes:")
    print("=================")
    for attr in sorted(info['public_attributes']):
        value = getattr(result, attr)
        if isinstance(value, (str, int, float, bool)) or value is None:
            print(f"{attr}: {value}")
        else:
            print(f"{attr}: {type(value)}")
    
    print("\nPublic Methods:")
    print("==============")
    for method in sorted(info['public_methods']):
        print(method)
    
    print("\nPrivate/Special Methods:")
    print("======================")
    for item in sorted(info['private_items']):
        print(item)
    
    return info

# Example usage:
# result = analyze_document_with_layout(client, "document.pdf")
# inspect_analyze_result(result)
