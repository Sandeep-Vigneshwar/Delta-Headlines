import os
import language_tool_python
import torch.cuda
from transformers import pipeline, AutoTokenizer


def split_text_into_chunks(text, tokenizer, max_tokens=512):
    sentences = text.split(". ")
    chunks, current_chunk = [], ""

    for sentence in sentences:
        temp_chunk = current_chunk + sentence + ". "
        token_count = len(tokenizer(temp_chunk)["input_ids"])

        if token_count <= max_tokens:
            current_chunk = temp_chunk
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def summarize_text(text, summarizer, tokenizer):
    text_chunks = split_text_into_chunks(text, tokenizer, max_tokens=512)
    summaries = []

    for chunk in text_chunks:
        try:
            input_text = "summarize: " + chunk
            summary = summarizer(input_text, max_length=300, min_length=150, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            print(f"Error summarizing chunk: {e}")

    combined_summary_text = " ".join(summaries)
    combined_tokens = len(tokenizer(combined_summary_text)["input_ids"])

    if combined_tokens > 512:
        input_text = "summarize: " + combined_summary_text
        final_summary = summarizer(input_text, max_length=400, min_length=250, do_sample=False)
        return final_summary[0]['summary_text']

    return combined_summary_text


def summarize_folder(input_folder, output_folder, model_name="t5-large"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    dev=0
    if(torch.cuda.is_available()!=True):
        dev = 1
    summarizer = pipeline("summarization", model=model_name, device=dev)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    txt_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    total_files = len(txt_files)

    for idx, file_name in enumerate(txt_files, start=1):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        with open(input_path, "r", encoding="utf-8") as file:
            text = file.read()

        summary = summarize_text(text, summarizer, tokenizer)
        tool = language_tool_python.LanguageTool('en-US')
        summary = tool.correct(text)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(summary)

        print(f"[{idx}/{total_files}] Processed: {file_name}")


if __name__ == "__main__":
    input_folder = "ocr_data"
    output_folder = "summarized_data"
    summarize_folder(input_folder, output_folder)