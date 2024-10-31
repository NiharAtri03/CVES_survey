# Description:
# Contains 3 methods that assist with survey generation
# rename_files() --> takes generated images from each model in a folder and preprocesses them for the next stage
# send_images() --> sends generated images from Purdue server to qualtrics
# format_images() --> combines image IDs and prompts into input format for qualtrics survey questions

import requests
import time
import os
import shutil

def rename_files():
    # directory with all the images in it
    root_dir = "/Users/niharatri/Downloads/Output Images"
    output_dir = "/Users/niharatri/Downloads/Images"

    os.makedirs(output_dir, exist_ok=True)

    # iterate through each directory in the root directory
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)

        if os.path.isdir(folder_path):
            images = sorted(os.listdir(folder_path))

            for index, image_name in enumerate(images):
                image_path = os.path.join(folder_path, image_name)

                new_image_name = f"{folder_name}_{index + 1}.png"
                new_image_path = os.path.join(output_dir, new_image_name)

                shutil.copy(image_path, new_image_path)

    print("All images have been renamed and saved to the Images directory.")

def send_images():
    # tokens and IDs
    API_TOKEN = "Zj7CKypLRSlheuPXl3cxOEzGEf0PDyDi2hU21Alx"
    DATACENTER_ID = "yul1"
    USER_ID = "UR_0xroToYK2AWSbsy"

    # folder in qualtrics where images are stored
    graphic_folder = "CVES Images"
    headers = {"x-api-token": API_TOKEN}
    # model names
    models = ["aMUSEd", "Dall-E-Mini", "StableDiffusionXLTurbo", "StableDiffusionV1-4", "StableDiffusionV2-1-base"]
    number_of_images = 5

    start_time = time.time()
    for model in models:
        print(f"Model: {model}")
        for number in range(1, number_of_images + 1):
            # each image is named modelname_imagenumber.png
            image_name = f"{model}_{number}.png"

            # path to images in my local directory
            graphic_path = f"/Users/niharatri/Downloads/Images/{image_name}"
            files = {'file': (image_name, open(graphic_path, 'rb'), 'image/jpeg'), "folder": (None, graphic_folder)}
            baseUrl = "https://{0}.qualtrics.com/API/v3/libraries/{1}/graphics/".format(DATACENTER_ID, USER_ID)
            requests.post(baseUrl, files=files, headers=headers)
    print(time.time() - start_time)

# Copy image IDs from qualtrics library IDs in settings --> replace input_data before running function
# Copy output into loop and merge block in question structure (delete old IDs first, then paste new ones)
def format_images():
    input_data = """aMUSEd_1.png	IM_ekDswSB1GKYKkiW
aMUSEd_2.png	IM_1TxbOJfL6sdQXVc
aMUSEd_3.png	IM_bDdEBV6rXr2NTlc
aMUSEd_4.png	IM_0AjrvcWeTdjHpcO
aMUSEd_5.png	IM_7Q9EZe6bAhIfHFQ
Dall-E-Mini_1.png	IM_8B7ckMqf703h2mO
Dall-E-Mini_2.png	IM_6x6HuSDkIex2aFw
Dall-E-Mini_3.png	IM_9um3GbfrQ2XXoZU
Dall-E-Mini_4.png	IM_eh7f07uEWi3P0HQ
Dall-E-Mini_5.png	IM_bJy0IZeheiypCrY
StableDiffusionV1-4_1.png	IM_diqXVmN1l1ECDNc
StableDiffusionV1-4_2.png	IM_d4KfLmXAeOMXrj8
StableDiffusionV1-4_3.png	IM_a5d2dQLuzEnx0ua
StableDiffusionV1-4_4.png	IM_6fXvESqlekiENX8
StableDiffusionV1-4_5.png	IM_1HNgwpAeGWryvNY
StableDiffusionV2-1-base_1.png	IM_cT7J92G2NmVDAgK
StableDiffusionV2-1-base_2.png	IM_e3bj57gGkFjpWKy
StableDiffusionV2-1-base_3.png	IM_e5uxknd2QbSb17o
StableDiffusionV2-1-base_4.png	IM_0r137V7E5jlqS58
StableDiffusionV2-1-base_5.png	IM_bwlTpad9V0Yo2I6
StableDiffusionXLTurbo_1.png	IM_8CdfSdaKlDlz2V8
StableDiffusionXLTurbo_2.png	IM_1TeXG0gsQMSqvuC
StableDiffusionXLTurbo_3.png	IM_e3vZIngVKpw38mW
StableDiffusionXLTurbo_4.png	IM_6MupoJ5OdSpdrXo
StableDiffusionXLTurbo_5.png	IM_3eH8pfxVZgPapH8
"""

    # assuming these are the 5 prompts in order (modelname_1 = first prompt)
    prompts = [
        "Four cartoon dwarfs playing video games in a cozy living room",
        "A bustling street at night with neon lights reflecting on wet pavement",
        "A cat sleeping on a laptop keyboard, with mouse and coffee mug on the desk, in sketch style",
        "A laptop, coffee mug, and notebook on a desk with a task lamp, in minimalist style",
        "A basket of yarn, knitting needles, and a half-finished scarf on a rocking chair, in watercolor style"]

    # Parse input data into a dictionary where key is model name and value is list of IDs
    model_data = {}
    for line in input_data.strip().split('\n'):
        filename, image_id = line.strip().split('\t')
        model_name = filename.split('_')[0]
        if model_name not in model_data:
            model_data[model_name] = []
        model_data[model_name].append(image_id)

    models = list(model_data.keys())

    output_rows = []
    num_images = len(model_data[models[0]])  # Assume all models have same number of images

    for i in range(num_images):
        row = []
        for model in models:
            row.append(model_data[model][i])
        output_rows.append(row)

    formatted_output = []
    for i, row in enumerate(output_rows):
        line = "\t".join(row)
        if i < len(prompts):
            line += f"\t{prompts[i]}"
        formatted_output.append(line)
    with open("reshaped_ids.txt", 'w') as f:
        for line in formatted_output:
            f.write(line + '\n')

# 3 helper functions
# run first 2 to send images to qualtrics
# run only format_images once you replace the input_data with image IDs from qualtrics library
rename_files()
send_images()
format_images()


