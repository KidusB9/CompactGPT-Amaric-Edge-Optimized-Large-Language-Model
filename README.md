# CompactGPT-AMR: Edge-Optimized Large Language Model

## Overview

Discover the future of NLP with CompactGPT-AMR, a revolutionary edge-optimized large language model. This cutting-edge technology brings the power of GPT-3 and GPT-4 to edge devices, enabling robust Amharic language processing capabilities in a compact, efficient design.

## Features

- **Edge-Optimized**: Designed for edge devices, reducing latency and increasing efficiency.
- **Large Language Model**: Leverages the power of GPT-3 and GPT-4 for robust language processing.
- **Amharic Language Support**: Specialized for Amharic language processing.

## Getting Started

### Installation

To get started, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/Kidus-berhanu/CompactGPT-AMR-Edge-Optimized-Large-Language-Model.git
cd CompactGPT-AMR-Edge-Optimized-Large-Language-Model
pip install -r requirements.txt


## Usage
## Training
- **To train the model, use the FullTrainer class in trainer.py**:

``` bash
from trainer import FullTrainer

# Initialize the trainer
trainer = FullTrainer(
    model_path="path/to/model",
    model_size="small",
    learning_rate=1e-5,
    batch_size=60,
    max_iters=6000,
    warmup_iters=300,
    cache_path="path/to/cache",
    checkpoint_dir="path/to/checkpoint",
    tokenizer_path="path/to/tokenizer",
    save_interval=500,
    eval_interval=50,
    gradient_accumulate=6,
    with_lr_scheduler=True,
    with_swa=True
)


### Generation
## To generate text using the trained model, use the generate.py script:
```bash
python generate.py \
    --model_path "path/to/model" \
    --model_size "small" \
    --chat

** This will start an interactive chat session where you can input text and the model will generate responses.**

# Train the model
trainer.train()




## Code Structure

- **finetune**: Fine-tuning scripts and utilities
- **hg_tokenizer**: Tokenizer implementation
- **kidus**: Kidus LLM model implementation
- **pretrain**: Pre-training scripts and utilities
- **scripts**: Miscellaneous scripts and utilities
- **tokenizer**: Tokenizer implementation
- **.gitignore**: Git ignore file
- **README.md**: This README file
- **dataset.py**: Dataset loading and processing script
- **generate.py**: Text generation script
- **requirements.txt**: Dependency requirements file
- **sophia.py**: Sophia model implementation
- **utils.py**: Utility functions




## Contributing

We welcome contributions to CompactGPT-AMR. If you'd like to contribute, please:

1. Fork the repository
2. Make your changes
3. Submit a pull request

## License

Mit License 

## Acknowledgments



