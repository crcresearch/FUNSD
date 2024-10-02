#%%
import pandas as pd
import json
import jq
import os
import re


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
