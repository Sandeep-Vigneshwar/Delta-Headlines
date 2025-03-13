import os
import numpy as np
import re
from paddleocr import PaddleOCR
from sklearn.cluster import DBSCAN
from wordsegment import load, segment

def fix_spacing_with_punctuation(text):
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    corrected_text = []
    for token in tokens:
        if re.match(r"\w+", token):
            corrected_text.append(" ".join(segment(token)))
        else:
            corrected_text.append(token)
    return "".join(
        [" " + token if i > 0 and re.match(r"\w+", token) else token for i, token in enumerate(corrected_text)]
    )

def is_title(text):
    words = text.split()
    if len(words) <= 6 and text.isupper():
        return True
    return False

def pipe1():
    ocr = PaddleOCR(use_angle_cls=True, lang="en", det_db_box_thresh=0.7, table=True)
    load()

    input_folder = "input_imgs"
    output_folder = "ocr_data"
    os.makedirs(output_folder, exist_ok=True)

    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total_files = len(image_files)

    for idx, image_file in enumerate(image_files, start=1):
        image_path = os.path.join(input_folder, image_file)
        results = ocr.ocr(image_path, cls=True)

        text_results = []
        for result in results:
            for line in result:
                bbox, (text, confidence) = line
                x_min, y_min, x_max, y_max = bbox[0][0], bbox[0][1], bbox[2][0], bbox[2][1]
                text_results.append((x_min, y_min, text))

        x_coords = np.array([[x, 0] for x, _, _ in text_results])

        dbscan = DBSCAN(eps=50, min_samples=2)
        column_labels = dbscan.fit_predict(x_coords)

        unique_labels = set(column_labels) - {-1}
        columns = {label: [] for label in unique_labels}

        for (x, y, text), label in zip(text_results, column_labels):
            if label != -1:
                columns[label].append((y, x, text))

        sorted_columns = []
        for col in sorted(columns.keys(), key=lambda c: min(x for _, x, _ in columns[c])):
            column_texts = []
            for _, _, text in sorted(columns[col]):
                corrected_text = fix_spacing_with_punctuation(text)
                if is_title(corrected_text):
                    column_texts.append(corrected_text + "\n")
                else:
                    column_texts.append(corrected_text)
            sorted_columns.append("\n".join(column_texts))

        newspaper_text = "\n\n".join(sorted_columns)
        newspaper_text = newspaper_text.replace("-\n", "")

        # Save the extracted text to a .txt file
        output_filename = os.path.splitext(image_file)[0] + ".txt"
        output_path = os.path.join(output_folder, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(newspaper_text)

        print(f"[{idx}/{total_files}] Processed: {image_file} → {output_filename}")

if __name__ == "__main__":
    pipe1()
