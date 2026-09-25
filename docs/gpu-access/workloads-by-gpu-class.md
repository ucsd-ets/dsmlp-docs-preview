# Workloads by GPU Class

Request the smallest GPU class the work fits within, among the classes the
workspace was granted; see [Choosing a Class](gpu-classes.md#choosing-a-class)
and [Workspace Class Grants](gpu-classes.md#workspace-class-grants). Not every
card or slice listed here backs its class in every quarter.

## Estimating GPU Memory

A model's weights take a fixed amount of GPU memory for each billion
parameters, set by their precision.

| Precision of the weights | GPU memory per billion parameters |
|---|---|
| BF16 or FP16 | About 2 GB |
| INT8 or FP8 | About 1 GB |
| 4-bit | About 0.5 GB |

Inference needs the weights plus a cache that grows with the length of the
context. Training also needs gradients, optimizer state, and the activations
for one batch. Full fine-tuning with the Adam optimizer takes about 16 bytes per
parameter before activations, so a 650M-parameter model needs about 10 GB.
LoRA (low-rank adaptation) freezes the base weights and trains small adapter
matrices, and QLoRA does the same on a base quantized to 4 bits, so both need
far less.

The memory figures in the examples are approximate peaks. They vary with batch
size, sequence length and LoRA rank. Measure a short trial run with
`nvidia-smi` or `torch.cuda.memory_summary()` before sizing a long one.

## Differences Within a Class

The cards and slices behind one class differ in memory, speed and supported
number formats. A `medium` session can run on a 20 GB slice or a 24 GB card, and
a `large` session on a 40 GB slice or a 48 GB card. A run that fits only the
larger device fails with a CUDA out-of-memory error whenever the session lands
on the smaller one. Size work for the smallest device listed for the class.

The Turing cards, the RTX 2080 Ti in `small` and the Titan RTX in `medium`, have
neither BF16 nor FlashAttention 2. Code that requires either fails or runs
slower on those cards. FP16 mixed precision runs on every device listed. See
[GPU Hardware & CUDA](gpu-hardware.md).

## `xsmall`

`xsmall` suits encoder fine-tuning, QLoRA of models up to about 3 billion
parameters, and small vision and graph models.

| Example | Setting | Method and approximate memory |
|---|---|---|
| Sentiment or topic classification with BERT-base or DistilBERT | Course | Full fine-tuning |
| A first instruction-tuning lab with Llama 3.2 3B and a small dataset | Course | QLoRA, about 3.5 GB |
| Image classification by transfer learning from ResNet-50 or EfficientNet | Course | Full fine-tuning |
| Named-entity recognition on PubMed abstracts with BioBERT or PubMedBERT | Research | Full fine-tuning |
| Node or link prediction with a graph neural network on Open Graph Benchmark datasets | Research | Under 2 GB for most architectures |

A 3B model at FP16 needs about 6.5 GB for inference, more than an `xsmall`
slice has. At 8-bit precision it needs about 3.5 GB.

### `xsmall` Hardware

| Card or slice | Memory | Specifications |
|---|---|---|
| A30 MIG 1g.6gb | 6 GB | [Ampere](gpu-hardware.md#ampere) |

## `small`

`small` suits QLoRA of 7B to 9B language models, larger vision models, and
image-generation LoRA training.

| Example | Setting | Method and approximate memory |
|---|---|---|
| Instruction-tuning an 8B or 9B model, such as Llama 3.1 8B or Gemma 2 9B | Course | QLoRA, about 9 to 10 GB |
| Zero-shot image retrieval by fine-tuning CLIP | Course | Full fine-tuning |
| Adapters for a low-resource language on mBERT or XLM-R | Research | Adapter training |
| Image-generation LoRA training on Flux | Research | QLoRA, about 9 GB |

A QLoRA run of an 8B or 9B model is close to the 10 GB of the H100 slice, the
smallest `small` device.

### `small` Hardware

| Card or slice | Memory | Specifications |
|---|---|---|
| H100 MIG 1g.10gb | 10 GB | [Hopper](gpu-hardware.md#hopper) |
| RTX 2080 Ti | 11 GB | [Turing](gpu-hardware.md#turing) |
| A30 MIG 2g.12gb | 12 GB | [Ampere](gpu-hardware.md#ampere) |

## `medium`

`medium` suits LoRA of 7B and 8B models without quantization, INT8 LoRA of 13B
and 14B models, and vision-language models.

| Example | Setting | Method and approximate memory |
|---|---|---|
| LoRA of a 7B model, such as Qwen2.5 7B, without quantization | Course | BF16 LoRA, about 18 GB |
| Visual question answering or chart reading with Qwen2-VL 7B or LLaVA 1.6 | Course | LoRA |
| Adapting a 14B model, such as Qwen2.5 14B, to a field's literature | Research | INT8 LoRA, about 16 GB |
| Protein function prediction with the 3B-parameter ESM-2 model | Research | Fine-tuning |

A 14B model at BF16 needs about 28 GB for its weights alone, more than any
`medium` device has.

### `medium` Hardware

| Card or slice | Memory | Specifications |
|---|---|---|
| H100 MIG 2g.20gb | 20 GB | [Hopper](gpu-hardware.md#hopper) |
| A30 | 24 GB | [Ampere](gpu-hardware.md#ampere) |
| RTX A5000 | 24 GB | [Ampere](gpu-hardware.md#ampere) |
| Titan RTX | 24 GB | [Turing](gpu-hardware.md#turing) |
| RTX PRO 6000 MIG 1g.24gb | 24 GB | [Blackwell](gpu-hardware.md#blackwell) |

## `large`

`large` suits QLoRA of 30B to 34B models, video generation, and protein
structure work.

| Example | Setting | Method and approximate memory |
|---|---|---|
| A graduate fine-tuning practicum on Qwen3 32B | Course | QLoRA, about 22 GB |
| Video generation at 720p with Wan2.1 or CogVideoX-5B | Course | Inference |
| Fine-tuning Qwen2.5-Coder 32B on a lab's bioinformatics pipelines | Research | QLoRA, about 22 GB |
| Protein structure prediction with ESMFold, or fine-tuning ESM-2 15B | Research | Fine-tuning |

QLoRA of a 70B model, such as Llama 3.1 70B, needs about 38 to 42 GB. It fits
the 48 GB devices, but not reliably the 40 GB slice. A 32B model at BF16 needs
about 66 GB for its weights, more than any `large` device has.

### `large` Hardware

| Card or slice | Memory | Specifications |
|---|---|---|
| H100 MIG 4g.40gb | 40 GB | [Hopper](gpu-hardware.md#hopper) |
| L40S | 48 GB | [Ada Lovelace](gpu-hardware.md#ada-lovelace) |
| RTX PRO 6000 MIG 2g.48gb | 48 GB | [Blackwell](gpu-hardware.md#blackwell) |

## `xlarge`

`xlarge` suits fine-tuning 70B models, long-context work, and pretraining
experiments.

| Example | Setting | Method and approximate memory |
|---|---|---|
| Fine-tuning Llama 3.1 70B or Qwen2.5 72B for an advanced seminar or a thesis | Course | FP8 LoRA, about 72 GB |
| Fine-tuning on long documents, with contexts of 128,000 tokens or more | Course | LoRA |
| Genomic language models, such as Nucleotide Transformer or HyenaDNA, on sequences of 100,000 bases or more | Research | Fine-tuning |
| Continued pretraining of a small model on a domain corpus | Research | Pretraining |
| Neural-operator training on fluid-dynamics or climate data with large batches | Research | Full training |

A 70B model at BF16 needs about 140 GB for its weights, more than any single
card has. Work across several GPUs is a separate request; see
[Multiple GPUs](gpu-classes.md#multiple-gpus).

### `xlarge` Hardware

| Card or slice | Memory | Specifications |
|---|---|---|
| H100 PCIe | 80 GB | [Hopper](gpu-hardware.md#hopper) |
| RTX PRO 6000 Blackwell | 96 GB | [Blackwell](gpu-hardware.md#blackwell) |
