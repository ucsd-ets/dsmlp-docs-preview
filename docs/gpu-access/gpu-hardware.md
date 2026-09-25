# GPU Hardware & CUDA

The cards and Multi-Instance GPU (MIG) slices listed here cover the many
configurations that can back a GPU class, and not every configuration is in
service in every quarter. A session requests a class, not a card; see
[GPU Class Sizes](gpu-classes.md#gpu-class-sizes).

## Specifications

The tables group cards by architecture, oldest first, and list the MIG slices
cut from a card after it. [Workloads by GPU Class](workloads-by-gpu-class.md)
lists the cards and slices behind each class.

Bandwidth is peak memory bandwidth. A slice's bandwidth is its share of the
card's and is nominal; see [MIG Slices](#mig-slices). The chip column gives the
GPU chip and its compute capability, written as the `sm_` target that CUDA
builds and error messages use.

### Turing

Turing cards have second-generation tensor cores, which run FP16 and INT8 but
not BF16. FlashAttention 2 does not support Turing.

| Card or slice | Memory | Bandwidth | Chip | Notes |
|---|---|---|---|---|
| RTX 2080 Ti | 11 GB GDDR6 | 616 GB/s | TU102, `sm_75` | Slower for training than the A30 and H100 slices with similar memory |
| Titan RTX | 24 GB GDDR6 | 672 GB/s | TU102, `sm_75` | Less bandwidth than the 24 GB Ampere cards |

### Ampere

Ampere cards have third-generation tensor cores, which add BF16 and TF32.
FlashAttention 2 supports Ampere.

| Card or slice | Memory | Bandwidth | Chip | Notes |
|---|---|---|---|---|
| RTX A5000 | 24 GB GDDR6 | 768 GB/s | GA102, `sm_86` | Workstation card. No MIG |
| A30 | 24 GB HBM2 | 933 GB/s | GA100, `sm_80` | FP64 tensor cores. Supports MIG, up to 4 slices. The most bandwidth of the 24 GB cards listed here |
| A30 MIG 2g.12gb | 12 GB HBM2 | ~466 GB/s | GA100, `sm_80` | Half of an A30 |
| A30 MIG 1g.6gb | 6 GB HBM2 | ~233 GB/s | GA100, `sm_80` | A quarter of an A30 |

### Ada Lovelace

Ada Lovelace cards have fourth-generation tensor cores, which add FP8.

| Card or slice | Memory | Bandwidth | Chip | Notes |
|---|---|---|---|---|
| L40S | 48 GB GDDR6 | 864 GB/s | AD102, `sm_89` | 91.6 TFLOPS FP32. No NVLink and no MIG. Less bandwidth than the H100 |

### Hopper

Hopper cards have fourth-generation tensor cores and the Transformer Engine,
which runs FP8. The H100s on DSMLP are the PCIe variant, with HBM2e memory at
2,000 GB/s. The SXM variant has HBM3 at 3,350 GB/s, so a PCIe H100 has about 60
percent of an SXM H100's bandwidth.

| Card or slice | Memory | Bandwidth | Chip | Notes |
|---|---|---|---|---|
| H100 PCIe | 80 GB HBM2e | 2,000 GB/s | GH100, `sm_90` | Supports MIG, up to 7 slices |
| H100 MIG 4g.40gb | 40 GB HBM2e | ~1,000 GB/s | GH100, `sm_90` | Four-sevenths of the card's compute and half its memory. More bandwidth than the 48 GB cards listed here, and 8 GB less memory |
| H100 MIG 2g.20gb | 20 GB HBM2e | ~500 GB/s | GH100, `sm_90` | Two-sevenths of the compute and a quarter of the memory. Less bandwidth than a full A30, with newer tensor cores |
| H100 MIG 1g.10gb | 10 GB HBM2e | ~250 GB/s | GH100, `sm_90` | One-seventh of the compute and an eighth of the memory. Less bandwidth than an RTX 2080 Ti, but faster for compute-bound training |

### Blackwell

Blackwell cards have fifth-generation tensor cores, which add FP4 (NVFP4) to
FP8.

| Card or slice | Memory | Bandwidth | Chip | Notes |
|---|---|---|---|---|
| RTX PRO 6000 Blackwell | 96 GB GDDR7 | 1,792 GB/s | GB202, `sm_120` | 188 streaming multiprocessors. Supports MIG, up to 4 slices. The most memory of any card listed here, and about 90 percent of the H100 PCIe's bandwidth |
| RTX PRO 6000 MIG 2g.48gb | 48 GB GDDR7 | ~896 GB/s | GB202, `sm_120` | Half of the card. 8 GB more memory than the H100 MIG 4g.40gb slice, with slightly less bandwidth |
| RTX PRO 6000 MIG 1g.24gb | 24 GB GDDR7 | ~448 GB/s | GB202, `sm_120` | A quarter of the card. Its tensor cores speed up INT8 and FP8 work, which offsets its lower bandwidth |

## MIG Slices

Multi-Instance GPU (MIG) divides one card into isolated slices. Each slice has
its own memory, cache and compute, and a session on a slice can use only that
slice. Sessions on different slices of one card do not share memory or
bandwidth.

A slice's name gives its compute and its memory: `2g.20gb` is two compute units
and 20 GB. A compute unit is a seventh of an H100's compute, or a quarter of an
A30's or an RTX PRO 6000's. A slice's bandwidth follows its share of the card's
memory rather than its compute. MIG divides an H100's memory into eighths, so
the `2g.20gb` slice has two-eighths of the card's bandwidth.

Inside a session, `nvidia-smi -L` lists the card and, on a slice, the slice's
profile.

## CUDA Versions

As of Fall 2026, DSMLP supports CUDA 12 and CUDA 13. The standard GPU image,
`scipy-ml-notebook`, includes CUDA 12. The image's Dockerfile records its exact
toolkit version; see
[Finding the Package List](../environments/standard-images.md#finding-the-package-list).
For a custom image that carries its own toolkit, see
[Custom CUDA Toolkits](../environments/building-a-custom-image.md#custom-cuda-toolkits).

## CUDA Profiling

Three profilers work on DSMLP. GPU performance counters are open to users
inside the container, so each can collect hardware metrics.

| Profiler | Shows | Output |
|---|---|---|
| Nsight Systems, `nsys` | A timeline of CPU threads, CUDA API calls, kernels, and memory copies, including where the GPU sits idle | A `.nsys-rep` report |
| Nsight Compute, `ncu` | Per-kernel metrics read from the GPU's performance counters | A `.ncu-rep` report |
| PyTorch profiler, `torch.profiler` | Time and memory by PyTorch operator | A printed table or a trace file |

The standard images do not include Nsight Systems or Nsight Compute. NVIDIA's
container images at `nvcr.io` are fully supported on DSMLP and include both.
The PyTorch profiler is part of PyTorch, which `scipy-ml-notebook` includes.

### Nsight Systems and Nsight Compute

Launch an NVIDIA image, such as `nvcr.io/nvidia/pytorch`, with `-i`. `-s` starts
a shell and no notebook server, because these images are not built on the
standard images:

```bash
launch-scipy-ml.sh -W <WORKSPACE> -g 1 -l gpu-class=medium -i nvcr.io/nvidia/pytorch:<tag> -s
```

These images are large, so the first launch on a node is slow. See
[Pulling a Large Image Ahead of a Session](../environments/building-a-custom-image.md#pulling-a-large-image-ahead-of-a-session).

Profile the whole run with Nsight Systems to find where the time goes, then
profile the kernels that dominate with Nsight Compute:

```bash
nsys profile -o timeline python train.py
ncu --launch-count 20 -o kernels python train.py
```

Nsight Compute replays each kernel many times to read its counters, so a run
under `ncu` is far slower than a normal one. `--launch-count` limits it to the
first kernels launched. Both reports open in NVIDIA's desktop applications of
the same names.

### PyTorch Profiler

In a PyTorch script, wrap a few training steps:

```python
import itertools

from torch.profiler import ProfilerActivity, profile

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
    for batch in itertools.islice(loader, 10):
        train_step(batch)

print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
```
