from transformers import AutoTokenizer
import json
import h5py
import tqdm
import numpy as np
import argparse


tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_path", type=str, default="./tmp/finetuning_dataset.json")

args = parser.parse_args()

with open(args.dataset_path, "r", encoding="utf8") as f:
    data = json.load(f)

# English prompt templates
PROMPT_DICT = {
    "prompt_input": (
        "Write a response that appropriately completes the request.\n"
        "### Instruction:\n{instruction}\n{input}\n\n### Response:\n"
    ),
    "prompt_no_input": (
        "Write a response that appropriately completes the request based on the instruction.\n\n"
        "### Instruction:\n{instruction}\n\n### Response:\n"
    ),
}

def _preprocess_hg(strings, tokenizer, block_size=256):
    kwargs = {"max_length": block_size + 1, "truncation": True, "padding": "max_length"}

    tokenized_list = []
    for text in tqdm.tqdm(strings):
        id = tokenizer.encode(f"<s> {text} </s>", **kwargs)
        tokenized_list.append(id)

    return tokenized_list

prompt_input, prompt_no_input = PROMPT_DICT["prompt_input"], PROMPT_DICT["prompt_no_input"]

sources = [
    prompt_input.format_map(example) if example.get("input", "") != "" else prompt_no_input.format_map(example)
    for example in data
]
targets = [f"{example['output']}" for example in data]

data = [source + target for source, target in zip(sources, targets)]

print(f"Sample Item:\n {data[0]}")

input_ids = _preprocess_hg(data, tokenizer)
np_ids = np.array(input_ids)

print(f"Sample Item:\n {np_ids[0]}")

total_dataset_size = np_ids.shape[0]
eval_size = 600 if total_dataset_size > 600 else 0
train_size = total_dataset_size - eval_size
print(f"Total Dataset: {total_dataset_size} | Train: {train_size} | Eval: {eval_size}")

np.random.shuffle(np_ids)
training_ds, eval_ds = np_ids[:train_size,:], np_ids[train_size:,:]

with h5py.File('./tmp/sft-cache.hdf5', 'w') as f:
    f.create_dataset("train", data=training_ds, dtype=np.int16)
    f.create_dataset("eval", data=eval_ds, dtype=np.int16)
