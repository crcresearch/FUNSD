# <a id='toc1_'></a>[FUNSD Datasets](#toc0_)

**Table of contents**<a id='toc0_'></a>    
- [FUNSD Datasets](#funsd-datasets)
	- [FUNSD Dataset (Original) \[1\] ↑](#funsd-dataset-original-1-)
		- [Data statistics](#data-statistics)
		- [Getting the Dataset](#getting-the-dataset)
	- [FUNSD Revised Dataset \[2\] ↑](#funsd-revised-dataset-2-)
	- [FUNSD+ Dataset \[3\] ↑](#funsd-dataset-3-)
- [References](#references)

<!-- vscode-jupyter-toc-config
	numbering=false
	anchor=true
	flat=false
	minLevel=1
	maxLevel=6
	/vscode-jupyter-toc-config -->
<!-- THIS CELL WILL BE REPLACED ON TOC UPDATE. DO NOT WRITE YOUR TEXT IN THIS CELL -->





This repository's content is intended to provide a guide on the [original **FUNSD** dataset](https://guillaumejaume.github.io/FUNSD/) and its versions.
Alongside the original dataset, there are two additional datasets derived from the it: the [FUNSD Revised Dataset](https://arxiv.org/pdf/2010.05322) and the [FUNSD+ Dataset](https://konfuzio.com/de/funsd-plus/).


The **FUNSD** (_Form Understanding in Noisy Scanned Documents_) dataset is commonly used to understand documents and extract information from scanned documents. 
It is particularly useful for tasks involving _Text Detection_, _Optical Character Recognition_, _Spatial Layout Analysis_, and _Form Understanding_.

<div style="text-align: center;">
    <img src="https://guillaumejaume.github.io/FUNSD/img/two_forms.png" alt="s" width="800"/>
    <p><em>Figure 1: Example of forms from the FUNSD dataset from https://guillaumejaume.github.io/FUNSD/img/two_forms.png. 
        The labels indicate different types of information: questions (blue), answers (green), headers (yellow), and other elements (orange).</em></p>
</div>


## <a id='toc1_1_'></a>FUNSD Dataset (Original) [[1]](#1) [&#8593;](#toc0_)

The FUNSD dataset was published by [Jaume et al. (2019)](https://arxiv.org/pdf/1905.13538) for form understanding in noisy scanned documents. It is available on [Guillaume Jaume's homepage](https://guillaumejaume.github.io/FUNSD/) and is licensed for non-commercial, research, and educational purposes.

The FUNSD dataset consists of `199 document images`, which is a subset sampled from the [RVL-CDIP dataset](https://adamharley.com/rvl-cdip/) introduced by [Harley et al. (2015)](https://arxiv.org/abs/1502.07058)[[4]](#4). The RVL-CDIP dataset comprises 400,000 grayscale images of various documents from the 1980s and 1990s. These scanned documents have a low resolution of 100 dpi and suffer from low quality due to various types of noise introduced by successive scanning and printing procedures. The RVL-CDIP dataset categorizes its images into four classes: letter, email, magazine, and form.

The authors of the FUNSD dataset manually reviewed 25,000 images from the "form" category, discarding unreadable and duplicate images. This process resulted in a refined set of 3,200 images, from which 199 images were randomly sampled for annotation to create the FUNSD dataset. 
The RVL-CDIP dataset is itself a subset of another dataset called the [Truth Tobacco Industry Document (TTID)](https://www.industrydocuments.ucsf.edu/tobacco)[[5]](#5), an archive collection of scientific research, marketing, and advertising documents from the largest tobacco companies in the US.

### <a id='toc1_1_1_'></a>[Data statistics](#toc0_)

In the original FUNSD dataset, the metadata of each image is contained in a separate JSON file, in which the form is represented as a list of interlinked **semantic entities**. Each **entity** consists of a group of words that belong together both _semantically_ and _spatially_. 

Each **semantic entity** is associated with:
- a **unique identifier**,
- a **label** which can be `header`, `question`, `answer`, or `other`,
- a **bounding box**,
- a **list of words** belonging to said entity,
- and a **list of links** with other entities.

Each `word` is described by its contextual content: a **OCR label** and its **bounding box**.

Please keep in mind the following information: 

- the `question` and `answer` labels are similar to `key` and `value`; 
- the bounding boxes are represented as `[left, top, right, bottom]`;
- and the links are formatted as a pair of entity identifiers, with the identifier of the current entity being the first element.

The dataset contains `199 images`, with over `30,000 word-level annotations` and approximately `10,000 entities`, 
and it was pre-divided into a `training set of 149 images` and a `testing set of 50 images`.

### <a id='toc1_1_2_'></a>[Getting the Dataset](#toc0_)

- The FUNSD dataset can be downloaded from the [original source](https://guillaumejaume.github.io/FUNSD/dataset.zip).

- We generated annotations from *Azure AI Document Intelligence service* for the images in the FUNSD dataset. \
  You also can use `git` with `dvc` to download the dataset containing the Azure annotations.:
  ```bash
  # in your virtual environment
  pip install dvc-gdrive
  dvc get https://github.com/crcresearch/FUNSD datasets/FUNSD
  ```
  Note: After the last command, a window will open to authenticate with your Google account. Once you do it, you can close the window and return to the terminal.

- You can also download it from the following link: https://www.crc.nd.edu/~pmoreira/funsd.zip

- To plot the annotations on the image, you can use the following notebook: [FUNSD notebook Instructions](nbs/funsd.ipynb)
- Find the code used to generate the Azure annotations at [here](./nbs/azure_generate_annotations_for_funsd_dataset.ipynb).


## <a id='toc1_2_'></a>FUNSD Revised Dataset [[2]](#2) [&#8593;](#toc0_)

- [FUNSD Revised notebook Instructions](nbs/funsd_revised.ipynb)

Vu et al. (2020) in [2] reported several inconsistencies in labeling, which could hinder the applicability of FUNSD to the key-value extraction problem. They revised the dataset by correcting the labels and adding new annotations.

## <a id='toc1_3_'></a>FUNSD+ Dataset [[3]](#3) [&#8593;](#toc0_)

The [FUNSD+](https://konfuzio.com/de/funsd-plus/) dataset is an enhanced version of the original [FUNSD (Form Understanding in Noisy Scanned Documents)](https://arxiv.org/pdf/1905.13538) dataset, designed for more comprehensive document understanding tasks.

- [FUNSD+ notebook Instructions](nbs/funsd_plus.ipynb)

# <a id='toc2_'></a>[References](#toc0_)

<a id="1"></a>
[1] Jaume, Guillaume, Ekenel, Hazim Kemal, and Thiran, Jean-Philippe. "FUNSD: A Dataset for Form Understanding in Noisy Scanned Documents," 2019. https://arxiv.org/pdf/1905.13538

<a id="2"></a>
[2] Vu, Hieu M., and Nguyen, Diep Thi-Ngoc. "Revising FUNSD Dataset for Key-Value Detection in Document Images," 2020. https://arxiv.org/pdf/2010.05322

<a id="3"></a>
[3] Zagami, Davide, and Helm, Christopher. "FUNSD+: A Larger and Revised FUNSD Dataset," 2022. https://konfuzio.com/de/funsd-plus/

<a id="4"></a>
[4] A. W. Harley, A. Ufkes, K. G. Derpanis, "Evaluation of Deep Convolutional Nets for Document Image Classification and Retrieval," in ICDAR, 2015. https://arxiv.org/abs/1502.07058

<a id="5"></a>
[5] Truth Tobacco Industry Documents Library. https://www.industrydocuments.ucsf.edu/tobacco
