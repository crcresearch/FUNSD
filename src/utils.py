
import json
import pandas as pd
from typing import List
import azure.ai.formrecognizer
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.patches as patches
import glob

def funsd_plot_annotations(image_path, annotations_path):
    # Load the image
    image = Image.open(image_path)

    # Load the annotations
    with open(annotations_path, 'r') as f:
        annotations = json.load(f)

    # Create a plot
    
    fig, ax = plt.subplots(1, figsize=(15, 20))
    ax.imshow(image)

    # Plot each annotation
    for annotation in annotations['form']:
        box = annotation['box']
        x, y, w, h = box[0], box[1], box[2] - box[0], box[3] - box[1]
        rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        #plt.text(x, y - 5, annotation['text'], color='red', fontsize=12, weight='bold')

    
    # Set the axis limits to fit the image
    ax.set_xlim([0, image.width])
    ax.set_ylim([image.height, 0])
    ax.axis('off')  # Hide the axis
    plt.show()
    
# Function to plot the image with FUNSD+ annotations
def funsd_plus_plot_annotations(image, bboxes, labels):
    # Get the image size
    width, height = image.size

    # Create a figure and axis with the same size as the image
    fig, ax = plt.subplots(1, figsize=(width / 100, height / 100), dpi=100)
    ax.imshow(image)

    # Define colors and alpha values for each label
    label_colors = {0: 'red', 1: 'yellow', 2: 'blue', 3: 'green'}
    alpha_value = 0.3  # Adjust alpha value for transparency

    # Add bounding boxes to the image
    for bbox, label in zip(bboxes, labels):
        # bbox is [x_min, y_min, x_max, y_max]
        x_min, y_min, x_max, y_max = bbox
        width = x_max - x_min
        height = y_max - y_min

        # Create a rectangle patch with alpha background
        rect = patches.Rectangle(
            (x_min, y_min), width, height, linewidth=1,
            edgecolor=label_colors[label],
            facecolor=label_colors[label],
            alpha=alpha_value
        )

        # Add the rectangle to the plot
        ax.add_patch(rect)

    # Turn off the axis labels
    ax.axis('off')

    # Display the plot
    plt.show()
    
    

def create_dataframe_from_key_value_pairs(key_value_pairs: List[azure.ai.formrecognizer._models.DocumentKeyValuePair]):
    data = []
    for pair in key_value_pairs:
        key_content = pair.key.content if pair.key else None
        value_content = pair.value.content if pair.value else None
        key_bounding_regions = [region.page_number for region in pair.key.bounding_regions] if pair.key and pair.key.bounding_regions else None
        value_bounding_regions = [region.page_number for region in pair.value.bounding_regions] if pair.value and pair.value.bounding_regions else None
        key_spans = [(span.offset, span.length) for span in pair.key.spans] if pair.key and pair.key.spans else None
        value_spans = [(span.offset, span.length) for span in pair.value.spans] if pair.value and pair.value.spans else None
        confidence = pair.confidence

        data.append({
            'key_content': key_content,
            'value_content': value_content,
            'key_bounding_regions': key_bounding_regions,
            'value_bounding_regions': value_bounding_regions,
            'key_spans': key_spans,
            'value_spans': value_spans,
            'confidence': confidence
        })
    
    return pd.DataFrame(data)
    
    
def initialize_client(endpoint, key):
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])

def analyze_document(formUrl: str, client: DocumentAnalysisClient, model_id: str):
    poller = client.begin_analyze_document_from_url(model_id, formUrl)
    result = poller.result()
    return result, poller.status

def print_document_result(result):
    
    print("API Version: ", result.api_version)
    print("Model ID: ", result.model_id)
    print("Document contains content: ", result.content)
    
   
    for idx, style in enumerate(result.styles):
        print(
            "Document contains {} content".format(
                "handwritten" if style.is_handwritten else "no handwritten"
            )
        )

    for page in result.pages:
        print("----Analyzing Read from page #{}----".format(page.page_number))
        print(
            "Page has width: {} and height: {}, measured with unit: {}".format(
                page.width, page.height, page.unit
            )
        )
        for line_idx, line in enumerate(page.lines):
            print(
                "...Line # {} has text content '{}' within bounding box '{}'".format(
                    line_idx,
                    line.content,
                    format_bounding_box(line.polygon),
                )
            )
        for word in page.words:
            print(
                "...Word '{}' has a confidence of {}".format(
                    word.content, word.confidence
                )
            )
    print("----------------------------------------")
    
    
def convert_floats_to_ints(data):
    if isinstance(data, list):
        return [convert_floats_to_ints(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_floats_to_ints(value) for key, value in data.items()}
    elif isinstance(data, float):
        return int(data)
    else:
        return data
    
def save_result_to_json(response, file_path):
    # result_dict = extract_data_from_azure_response(response)
    result_dict = response.to_dict()
    result_dict_int = convert_floats_to_ints(result_dict)
    with open(file_path, 'w') as f:
        json.dump(result_dict_int, f, indent=4)    
        
        
def extract_data_from_azure_response(response):
    def to_dict_list(items):
        return [item.to_dict() for item in items] if items else []

    extracted_data = {}
    schema = response.__annotations__.items()
    for key, value_type in schema:
        if hasattr(response, key):
            items = getattr(response, key)
            if isinstance(items, list):
                extracted_data[key] = to_dict_list(items)
            else:
                extracted_data[key] = items

    return extracted_data

def extract_data_from_azure_response_(response):
    return {
        "api_version": response.api_version,
        "model_id": response.model_id,
        "content": response.content,
        "pages": [ page.to_dict() for page in response.pages],
        "languages": [language.to_dict() for language in response.languages],        
        "paragraphs": [paragraph.to_dict() for paragraph in response.paragraphs],        
        "tables": [table.to_dict() for table in response.tables],
        "key_value_pairs": [key_value_pair.to_dict() for key_value_pair in response.key_value_pairs],
        "styles": [style.to_dict() for style in response.styles],
        "documents": [document.to_dict() for document in response.documents],
    }
    
    

def plot_azure_annotations(image_path, annotations_path, show_text=False):
    # Load the image
    image = Image.open(image_path)
    # Correct the orientation of the image
    # image = ImageOps.exif_transpose(image)
    
    # Load the Azure OCR annotations
    with open(annotations_path, 'r') as file:
        annotations = json.load(file)
    
    # Create a plot
    fig, ax = plt.subplots(1, figsize=(15, 20))
    ax.imshow(image)
    
    # Plot each annotation
    for page in annotations['pages']:
        for line in page['lines']:
            polygon = line['polygon']
            # Extract the coordinates
            coords = [(point['x'], point['y']) for point in polygon]
            # Create a polygon patch
            poly_patch = patches.Polygon(coords, closed=True, edgecolor='r', facecolor='none', linewidth=2)
            ax.add_patch(poly_patch)
            # Add text annotation
            x, y = coords[0]
            if show_text:
                ax.text(x, y, line['content'], fontsize=10, color='red', verticalalignment='top')
    
    # Set the axis limits to fit the image
    ax.set_xlim([0, image.width])
    ax.set_ylim([image.height, 0])
    ax.axis('off')  # Hide the axis
    plt.show()
    

def generate_image_urls(img_dir, img_url_base):
    image_file_paths = glob.glob(f"{img_dir}/*.png")
    image_names = [p.split('/')[-1] for p in image_file_paths]
    image_urls = [f"{img_url_base}/{name}" for name in image_names]
    return image_urls
    