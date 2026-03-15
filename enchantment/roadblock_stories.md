# Roadblock Stories — Problem to Resolution Frameworks
## Pre-Structured for "Tell Me About a Time When..."

---

## How to Use This File

Each story follows the **SCTRW** framework:
- **S**ituation — What were you doing? (10 seconds)
- **C**omplication — What went wrong? (15 seconds)
- **T**ried — What did you try first? (30 seconds)
- **R**esolution — What actually worked? (45 seconds)
- **W**isdom — What principle did you take away? (10 seconds)

Fill in YOUR details. The frameworks below are skeletons — the power comes from your specific context, numbers, and emotions.

---

## Story 1: Data Quality Cascade

**Category:** Data pipeline failure during pre-training

**S:** "I was leading the data pipeline for a pre-training run on [domain] data — [X] billion tokens, [Y] GPU-days planned."

**C:** "Three weeks in, we noticed the model's performance on [specific eval] was degrading instead of improving. Loss was decreasing, but downstream quality was getting worse."

**T:** "My first instinct was that we were overfitting — so I increased dropout and reduced the learning rate. That slowed the degradation but didn't fix it. Then I thought it was a data mix issue, so I adjusted domain weights. Still degrading."

**R:** "I finally wrote a per-shard quality analysis script — computed perplexity against a reference model for each data shard individually. Found that [X]% of shards from one data source had been corrupted during preprocessing — a regex in our cleaning pipeline was silently truncating documents after certain Unicode characters. The model was effectively being trained on sentence fragments. Fixed the regex, rebuilt the affected shards, resumed from a clean checkpoint."

**W:** "I now always run per-shard quality audits before AND during training. Data bugs are silent — loss goes down because the model learns the broken pattern, but downstream quality suffers. The lesson: loss is not quality."

**Key details to add:** Specific data source, exact corruption pattern, how many GPU-hours were lost, how you set up monitoring to prevent recurrence.

---

## Story 2: Training Instability at Scale

**Category:** Scaling from small to large model

**S:** "We had a pre-training recipe that worked perfectly at [small scale] — [X]M parameters, [Y] GPUs. We needed to scale to [larger scale]."

**C:** "At scale, training would diverge after [N]K steps — loss would spike and never recover. The same hyperparameters that were stable at small scale were catastrophically unstable at large scale."

**T:** "First I tried reducing the learning rate proportionally — classic linear scaling rule. That helped but made training unacceptably slow. Then I tried gradient clipping — helped with the spikes but introduced a new problem: clipping was activating so frequently that effective learning rate was oscillating."

**R:** "The root cause was the interaction between our learning rate warmup schedule and the batch size. At large scale, we were using much larger batches (for throughput), which changed the effective noise in gradient estimates. The warmup was too aggressive — the model was learning large updates from noisy gradients in the first few thousand steps, which pushed it into a bad loss basin. The fix was: (1) longer warmup (linear warmup for 2% of total steps instead of 0.5%), (2) mu-parametrization for initialization, which makes hyperparameters more transferable across scales, and (3) a 'spike detection' mechanism that rolls back to the previous checkpoint and reduces LR when loss jumps by more than [X]%."

**W:** "Hyperparameters don't transfer across scales unless you explicitly account for the interaction between batch size, learning rate, and model width. The small-scale ablation is necessary but not sufficient — you need principled scaling rules, not just hoping it works."

---

## Story 3: Domain Adaptation Failure

**Category:** Fine-tuning a general model for domain-specific tasks

**S:** "We tried domain-adaptive pre-training — taking a general [X]B parameter model and continuing pre-training on [domain-specific] data."

**C:** "The domain performance improved initially but then plateaued at a level significantly below what we expected. Worse, the model's general capabilities had degraded — it was forgetting what it knew."

**T:** "Classic catastrophic forgetting. First approach: reduce learning rate to minimize disruption to existing weights. This slowed forgetting but also slowed domain adaptation — we were stuck in a lose-lose tradeoff."

**R:** "Two things fixed it. First, we mixed general data into the domain adaptation phase — not 50/50, but a carefully tuned ratio of [X]% domain, [Y]% general. We found the ratio empirically through small-scale ablations. Second, and more importantly, we realized the tokenizer was the bottleneck. The general model's tokenizer split domain-specific terms into 4-5 sub-tokens, which meant the model was spending capacity on token reconstruction instead of semantic learning. We extended the tokenizer vocabulary with [N]K domain-specific tokens, adjusted the embedding layer, and restarted domain adaptation. Performance jumped [X]% immediately."

**W:** "Domain adaptation isn't just about data — the tokenizer encodes a prior over what the model considers a 'unit of meaning.' If your domain's units of meaning aren't in the vocabulary, you're fighting the tokenizer the entire time."

---

## Story 4: Infrastructure Bottleneck

**Category:** Training speed limited by non-obvious bottleneck

**S:** "We were running a pre-training job on [N] GPUs across [M] nodes. Theoretical throughput should have been [X] tokens/second, but we were getting [Y] — less than half."

**C:** "GPU utilization was only [Z]%. The GPUs were spending more time waiting than computing."

**T:** "First suspect: data loading bottleneck. Increased DataLoader workers, added prefetching, switched to memory-mapped data. Improved by [A]%, but still nowhere near theoretical. Second suspect: all-reduce communication overhead. Profiled with PyTorch profiler — communication was overlapping well with compute, not the bottleneck."

**R:** "The actual bottleneck was subtle: our gradient checkpointing implementation was forcing CUDA synchronization at every checkpoint boundary. Each sync point created a pipeline bubble where the GPU waited for the CPU to catch up. The fix was switching to PyTorch's native `torch.utils.checkpoint` with `use_reentrant=False`, which properly handles async execution. Additionally, I found that our custom loss function was inadvertently copying tensors to CPU for logging every step — a single `.item()` call in the wrong place was triggering a sync. After both fixes, throughput jumped to [X]% of theoretical."

**W:** "Performance debugging in distributed training is about finding synchronization points — places where async pipelines are forced to wait. The bottleneck is almost never where you first look. Always profile before optimizing."

---

## Story 5: Evaluation Gap

**Category:** Model appears to work but fails in deployment/application

**S:** "We pre-trained a model on [domain] data. It achieved strong perplexity on held-out data and scored well on standard benchmarks."

**C:** "When we evaluated it on actual downstream tasks — [specific task] — performance was poor. There was a gap between our proxy metrics and real-world utility."

**T:** "First thought: fine-tuning recipe was wrong. Tried different learning rates, prompt formats, few-shot configurations. Marginal improvements but the fundamental gap remained."

**R:** "The problem was in what we *weren't* evaluating during pre-training. Our evaluation suite tested language understanding and domain knowledge, but the downstream task required [specific capability — e.g., numerical reasoning, temporal ordering, causal inference] that we never measured. When I built a targeted evaluation for that capability, the model scored near random. The pre-training data had plenty of examples of this capability in context, but the model wasn't learning it — likely because the pre-training objective (next-token prediction) didn't create sufficient gradient signal for that specific skill. We addressed it by (1) adding targeted evaluation to our pre-training eval suite, (2) upweighting training data that exercised that capability, and (3) adding an auxiliary pre-training objective that explicitly trained for [capability]."

**W:** "Pre-training evaluation must be downstream-aware. Perplexity tells you the model learned the training distribution, not that it learned the capabilities you care about. Build evaluations for the capabilities you need, not just the metrics that are easy to compute."

---

## Story 6: Team & Process Challenge

**Category:** Coordination and decision-making under uncertainty

**S:** "Our team was split on a fundamental pre-training design decision — [decision, e.g., from-scratch vs. DAPT, data mix strategy, architecture choice]. Both options had merit and neither had clear evidence."

**C:** "We spent [X] weeks debating without converging. Meanwhile, compute allocation was burning — we had a deadline for [internal milestone], and indecision was the biggest risk."

**T:** "I initially tried to resolve it by gathering more evidence — reading more papers, running more analyses. But the evidence was genuinely ambiguous — this was a decision that required judgment, not just data."

**R:** "I proposed a structured approach: (1) define the decision criteria upfront — what metrics would we use to compare the two approaches? (2) run both as parallel small-scale experiments with a strict 1-week time box, (3) commit to whichever won on the pre-agreed criteria, even if we had second thoughts. I also framed it as a reversible decision — we could always change direction at the next checkpoint. This lowered the stakes, made people comfortable committing, and gave us concrete evidence to decide. Approach [X] won, we committed, and it worked out."

**W:** "In research-heavy teams, the biggest risk isn't choosing wrong — it's not choosing at all. Structured experimentation with pre-committed decision criteria turns debates into learning opportunities. And framing decisions as reversible makes teams braver."

---

## META-ADVICE: How to Tell These Stories

1. **Be specific** — Numbers, dates, tool names, exact error messages. Specificity = credibility.
2. **Show the wrong turns** — Horia wants to see your debugging process, not just the answer.
3. **Include emotions** — "That was genuinely frustrating" or "I found that really satisfying" makes you human.
4. **Credit others** — "A teammate suggested X" or "I asked [person] for help" shows collaboration.
5. **Land the principle** — Every story should end with a reusable insight, not just "and then it worked."
6. **Keep it conversational** — These aren't scripted monologues. Practice telling them naturally, not reciting them.

---

## ADAPTING ON THE FLY

If Horia asks about a roadblock you don't have a prepared story for:

1. Pause — "That's a great question, let me think of the best example..."
2. Pick the closest story and adapt the framing
3. Be honest if you haven't faced that specific challenge — then reason about how you *would* approach it
4. "I haven't hit that exact problem, but in a related situation I [story]. If I faced [his scenario], I'd start by [first-principles reasoning]."
