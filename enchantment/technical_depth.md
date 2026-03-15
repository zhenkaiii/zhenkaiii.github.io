# Technical Depth — Pre-Training Arsenal
## Organized for Conversational Recall, Not Textbook Recitation

---

## 1. ARCHITECTURE DECISIONS

### Transformer Variants — What to Know and What to Say
| Variant | Key Idea | When to Mention |
|---|---|---|
| Vanilla Transformer (Vaswani et al.) | Self-attention + cross-attention, encoder-decoder | Baseline reference |
| Decoder-only (GPT family) | Causal attention mask, autoregressive generation | Most foundation models today |
| Encoder-only (BERT family) | Bidirectional context, masked language modeling | When discussing MLM pre-training |
| Mixture of Experts (MoE) | Sparse activation, conditional computation | When discussing scaling efficiency |
| State Space Models (Mamba, S4) | Linear-time sequence modeling, long-range deps | When discussing alternatives to attention |

**Conversational framing:**
> "The architecture choice in pre-training isn't just about parameter count — it encodes inductive biases about what relationships the model should learn. For financial data, where causal ordering is critical and context windows need to span entire trading sessions, these biases matter enormously."

### Attention Mechanisms — Deep Cuts
- **Multi-Head Attention (MHA)**: Standard. Each head learns different relationship patterns.
- **Grouped-Query Attention (GQA)**: Shares key-value heads across query heads. Inference-efficient. Used in Llama 2/3.
- **Multi-Query Attention (MQA)**: Single KV head shared across all queries. Faster but slightly lower quality.
- **Flash Attention**: IO-aware exact attention. Fuses operations to reduce memory bandwidth bottleneck. Not an approximation — same math, better systems engineering.
- **Sliding Window Attention**: Local attention windows (Mistral). Good for long sequences where most relevant context is nearby.

**If asked about choosing attention for financial data:**
> "Financial time-series have both local structure (intraday patterns, order book dynamics) and long-range dependencies (regime shifts, macro cycles). I'd consider a hybrid — sliding window for local context efficiency, with periodic global attention tokens that capture regime-level information. Similar spirit to Longformer's design, but adapted for the temporal structure of market data."

### Positional Encodings
- **Sinusoidal (original)**: Fixed, no learned parameters. Limited generalization to unseen positions.
- **Learned absolute**: Simple but poor length generalization.
- **RoPE (Rotary Position Embedding)**: Relative position encoded as rotation in embedding space. Generalizes well to longer sequences. Standard in modern models (Llama, Mistral).
- **ALiBi (Attention with Linear Biases)**: Adds linear bias to attention scores based on distance. Good length extrapolation without extra parameters.

**For financial models specifically:**
> "Position encoding in financial foundation models is interesting because you have multiple notions of 'position' — sequence position, calendar time, trading time (excluding market closures), and relative position within a trading session. RoPE handles sequence position well, but you might want auxiliary temporal encodings that capture calendar structure."

---

## 2. PRE-TRAINING OBJECTIVES

### Causal Language Modeling (CLM)
- Predict next token given all previous tokens
- Standard for GPT-family models
- Natural fit for autoregressive generation
- **Financial angle**: Good for generating scenarios, extrapolating patterns, but doesn't natively learn bidirectional context

### Masked Language Modeling (MLM)
- Mask 15% of tokens, predict them from context
- Bidirectional context encoding
- **Financial angle**: Good for understanding relationships in financial documents (filings, earnings calls), but doesn't generate well

### Denoising Objectives (T5-style)
- Corrupt input, reconstruct original
- Span corruption, token deletion, sentence permutation
- **Financial angle**: Robust to noisy data — useful when pre-training on messy financial text (analyst notes, trading floor transcripts)

### Domain-Adaptive Pre-Training (DAPT)
- Continue pre-training a general model on domain-specific data
- Key paper: Gururangan et al. (2020) "Don't Stop Pretraining"
- **Critical nuance to mention:**
> "DAPT is powerful but has a fundamental limitation — the general model's tokenizer and representations were optimized for web text. Financial terminology, ticker symbols, numerical expressions, and structured data formats are often poorly tokenized, which creates an efficiency ceiling. This is why pre-training from scratch on curated domain data, with a domain-aware tokenizer, can be worth the compute cost."

### Contrastive Objectives
- Learn representations by pushing similar examples together, dissimilar apart
- SimCLR, CLIP-style
- **Financial angle**: Useful for multi-modal financial models — aligning text representations (news, filings) with time-series representations (price action, order flow)

---

## 3. DATA PIPELINE DESIGN — The Unsexy Superpower

### Curation Philosophy
> "Pre-training data isn't just fuel — it's the curriculum. How you compose, filter, and weight your data mix encodes your beliefs about what the model should learn. In my experience, data curation decisions have more impact on model quality than architecture decisions."

### Key Pipeline Components

**Data Collection & Ingestion**
- Web crawls (Common Crawl filtering), document stores, APIs
- For financial: Market data feeds, SEC filings (EDGAR), earnings call transcripts, news wire services, order book snapshots, research reports
- Data provenance tracking — know where every training example came from

**Quality Filtering**
- Perplexity-based filtering (use a small reference model to score quality)
- Heuristic filters (document length, language detection, boilerplate removal)
- Deduplication: Exact (hash-based) and near-duplicate (MinHash / SimHash)
- **Critical insight:**
> "Most quality filtering pipelines have a hidden assumption — that 'high quality' means 'well-written.' In financial data, some of the most informative signals come from terse, poorly formatted sources like trader chat logs, raw order book data, or abbreviated analyst notes. Overly aggressive filtering throws away signal."

**Data Mixing**
- Domain weight ratios (e.g., 40% general text, 30% financial text, 20% code, 10% structured data)
- Curriculum learning: changing the mix over training (start general, become more domain-specific)
- DoReMi (Xie et al. 2023): Learning optimal domain weights using a small proxy model
- **Taste statement:**
> "I'm a strong believer in empirically validating data mix ratios through small-scale ablations rather than relying on intuition or proportional representation. A 10% change in domain weighting can have a 2x impact on downstream task performance."

**Tokenization**
- BPE (Byte-Pair Encoding): Standard, good compression
- SentencePiece: Language-agnostic, works well for multilingual
- Domain-specific considerations:
  - Financial numbers: "1,234.56" should ideally be tokenized in a way that preserves numerical meaning
  - Ticker symbols: $AAPL, $MSFT should be single tokens, not fragmented
  - Temporal expressions: "Q3 2024", "FY23" need consistent handling
  - **Key point:** "If your tokenizer fragments domain-critical entities, the model has to learn to reconstruct them from sub-tokens before it can even start learning their meaning. That's wasted capacity."

**Data Decontamination**
- Remove benchmark/evaluation data from training set
- N-gram overlap detection against eval datasets
- Critical for credible evaluation — especially with financial benchmarks where overlap is common

---

## 4. TRAINING INFRASTRUCTURE

### Distributed Training
- **Data Parallelism (DDP)**: Replicate model across GPUs, split data. Synchronize gradients via all-reduce.
- **Fully Sharded Data Parallelism (FSDP)**: Shard model parameters, gradients, and optimizer states across GPUs. Memory-efficient.
- **Tensor Parallelism (TP)**: Split individual layers across GPUs. Good for very large layers.
- **Pipeline Parallelism (PP)**: Split model layers across GPUs in stages. Requires micro-batching to keep GPUs busy.
- **3D Parallelism**: Combine DP + TP + PP. Standard for large-scale training (Megatron-LM, DeepSpeed).

**Conversational level:**
> "The parallelism strategy is driven by the ratio of model size to available per-GPU memory. For models that fit in a single GPU with FSDP sharding, you don't need the complexity of tensor or pipeline parallelism. But once you exceed that, you need to think carefully about the communication topology — tensor parallelism wants high-bandwidth intra-node links (NVLink), while data parallelism is more tolerant of inter-node latency."

### Mixed Precision Training
- FP16/BF16 for forward/backward pass, FP32 for master weights and optimizer states
- BF16 preferred: larger dynamic range, less overflow risk, no loss scaling needed
- **Practical tip:**
> "BF16 is almost always the right choice for pre-training. FP16 requires loss scaling to avoid gradient underflow, and getting the scaling factor wrong can silently degrade training quality. BF16 trades mantissa bits for exponent bits, so you lose some precision but gain dynamic range — and for pre-training, dynamic range matters more."

### Gradient Accumulation & Checkpointing
- Gradient accumulation: Simulate larger batch sizes across micro-batches
- Gradient/activation checkpointing: Trade compute for memory by recomputing activations during backward pass
- **When to mention:** When discussing how to train large models on limited hardware

### Training Stability
- Learning rate warmup + cosine decay (standard recipe)
- Gradient clipping (typically 1.0)
- Weight decay (typically 0.1)
- Loss spikes: usually data-related (corrupted batches, distribution shifts in data pipeline)
- **War story territory:** If you've debugged a training instability, this is where to tell the story

### Checkpointing & Recovery
- Save checkpoints every N steps (balance between recovery granularity and storage cost)
- Optimizer state checkpointing for seamless resumption
- Evaluation checkpoints: periodic eval on held-out data to detect quality regressions
- **Practical wisdom:**
> "I learned the hard way to always validate checkpoint integrity immediately after saving. A corrupted checkpoint that you discover three days later can cost you an entire training run."

---

## 5. FINANCIAL DOMAIN SPECIFICS

### What Makes Financial Foundation Models Different

**Multi-modal by necessity**
Financial data isn't just text. A trading foundation model needs to integrate:
- Natural language (news, filings, analyst reports, earnings calls)
- Time-series (price, volume, order flow, volatility surfaces)
- Structured data (financial statements, economic indicators, corporate actions)
- Graph data (company relationships, supply chains, sector hierarchies)

> "The challenge isn't just handling multiple modalities — it's learning the *interactions* between them. A price move means something different depending on whether it coincides with an earnings release, a macro event, or just noise. The model needs to learn these cross-modal dependencies during pre-training, not just at the fine-tuning stage."

**Temporal structure matters**
- Markets have nested temporal hierarchies: tick-level, intraday, daily, weekly, seasonal, regime-level
- Non-stationarity: the data distribution shifts over time (regime changes, structural breaks)
- **Key insight:**
> "Pre-training on financial data requires careful handling of time. You can't just shuffle all your data randomly — temporal order contains information. But you also can't be purely sequential, or the model overfits to historical regimes. The right approach is somewhere in between: preserve local temporal structure while mixing across time periods for robustness."

**Signal-to-noise ratio is low**
- Financial data is noisy. Most price movements are random.
- The learnable signal is subtle — statistical edges are small but persistent
- **Implication for pre-training:**
> "In NLP pre-training, the model learns clear linguistic structure — syntax, semantics, discourse. In financial pre-training, the 'structure' is often statistical regularities buried in noise. This means you need much more data, longer training, and careful evaluation to know if the model is learning signal or memorizing noise."

### Vertical LLMs — The CitSec Edge

> "What's interesting about CitSec's approach to vertical LLMs is the data moat hypothesis — general LLMs are trained on public data that everyone has access to. But a foundation model pre-trained on proprietary healthcare data, or granular market microstructure data, develops representations that can't be replicated by fine-tuning a general model. The pre-training data IS the competitive advantage."

Key areas to discuss:
- **Healthcare data**: Clinical notes, lab results, imaging reports, genomic data — highly specialized vocabulary and reasoning patterns
- **Financial data**: Order book data, trade execution logs, internal research — not available in public pre-training corpora
- **The moat**: These models learn domain-specific "common sense" that general models can never develop from public data alone

### Trading Foundation Models — What They Do Differently

1. **Representation learning for alpha**: The model learns dense representations of market state that capture predictive signal
2. **Multi-horizon prediction**: Pre-train to predict at multiple time horizons simultaneously (next tick, next minute, next day)
3. **Conditional generation**: Generate scenarios conditioned on current market state (stress testing, risk analysis)
4. **Cross-asset learning**: A foundation model pre-trained across asset classes can transfer structural knowledge (e.g., yield curve dynamics inform equity factor models)

> "The vision for a trading foundation model isn't to replace quantitative researchers — it's to give them a richer feature space. Instead of hand-engineering factors, you extract learned representations from a model that has seen the full breadth of market data. The researchers then build strategies on top of these representations."

---

## 6. KEY PAPERS TO REFERENCE NATURALLY

Don't namedrop papers gratuitously. But if a topic comes up, showing you've read the primary literature is high-signal.

| Topic | Paper | Key Contribution |
|---|---|---|
| Scaling laws | Kaplan et al. (2020) "Scaling Laws for Neural Language Models" | Power-law relationships between compute, data, params, and loss |
| Chinchilla scaling | Hoffmann et al. (2022) "Training Compute-Optimal LLMs" | Optimal token-to-parameter ratio; most models are undertrained |
| Domain-adaptive PT | Gururangan et al. (2020) "Don't Stop Pretraining" | Continued pre-training on domain data improves downstream tasks |
| Data mixing | Xie et al. (2023) "DoReMi" | Learning optimal domain weights for pre-training data |
| Flash Attention | Dao et al. (2022) | IO-aware exact attention; practical speedup |
| LoRA | Hu et al. (2021) | Low-rank adaptation for efficient fine-tuning |
| Financial LLMs | Wu et al. (2023) "BloombergGPT" | 50B param model pre-trained on financial data; showed domain pre-training value |
| Time-series transformers | Nie et al. (2023) "PatchTST" | Patching + channel independence for time-series; relevant to financial modeling |

---

## 7. ANTI-PATTERNS — What NOT to Say

- Don't say "we just used GPT-4" — this interview is about building, not using
- Don't hand-wave over data work — "we cleaned the data" without specifics signals inexperience
- Don't oversimplify scaling — "we just added more GPUs" ignores the real engineering challenges
- Don't confuse fine-tuning with pre-training — they are fundamentally different optimization problems
- Don't claim expertise you don't have — Horia will probe, and honesty + reasoning > fake depth
