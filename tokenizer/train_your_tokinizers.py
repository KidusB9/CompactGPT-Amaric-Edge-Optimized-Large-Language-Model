from tokenizers import ByteLevelBPETokenizer

# Initialize a tokenizer
tokenizer = ByteLevelBPETokenizer()

# Train the tokenizer on your dataset
tokenizer.train(files="path_to_your_corpus.txt", vocab_size=52000, min_frequency=2, special_tokens=[
    "<p>", "<unk>", "<s>", "</s>"
])

# Save the tokenizer - this will generate a vocab file and a merges file
tokenizer.save_model("path_to_save")
