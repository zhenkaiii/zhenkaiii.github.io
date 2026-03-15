brew upgrade claude-code# Questions to Ask Horia
## Curated for Signal — Each One Shows You Understand Their World

---

## Principles for Asking Questions

1. **Ask about their work, not their company** — "How does your team handle X?" beats "What does CitSec do about X?"
2. **Show you've thought about it** — Frame questions with your hypothesis first: "I'd imagine you face Y challenge — how have you approached that?"
3. **Be genuinely curious** — If you're not actually interested in the answer, don't ask it
4. **Time it right** — Weave questions into the conversation, don't save them all for the end

---

## Tier 1: Trading Foundation Model Architecture

These show you understand what they're building.

> "When pre-training a trading foundation model, how do you think about the tension between learning generalizable market representations versus regime-specific patterns? Do you find that longer pre-training horizons help with generalization, or do you need explicit regime-awareness in the architecture?"

> "I'm curious about how you handle multi-modal inputs during pre-training — do you embed text and time-series into a shared latent space from the start, or do you pre-train separate encoders and fuse them later? I've seen arguments for both, but I'd love to hear what's worked in practice."

> "How does your team think about evaluation for a trading foundation model? Standard NLP benchmarks don't apply, and backtesting on historical data has well-known pitfalls. What does your evaluation flywheel look like?"

---

## Tier 2: Data Strategy & Vertical LLMs

These show you understand their edge.

> "The idea of vertical LLMs with specialized data is compelling — but how do you think about the data freshness problem? Financial data has a shelf life. Do you periodically re-pre-train, or is there a continual learning approach that works?"

> "When building a vertical LLM on healthcare data versus financial data, do the pre-training approaches look fundamentally different, or is the difference mostly in the data pipeline and tokenization?"

> "I'd imagine the data curation pipeline for a trading foundation model is extremely high-touch — what's the ratio of data engineering effort to modeling effort on your team?"

---

## Tier 3: Pre-Training Research Questions

These show you think about the frontier.

> "How do you think about scaling laws in the context of domain-specific foundation models? Do you find that the Chinchilla-optimal compute ratios hold for financial data, or does the lower signal-to-noise ratio change the calculus?"

> "I've been thinking about whether pre-training objectives need to be fundamentally different for financial data — next-token prediction on text captures linguistic structure, but what captures market structure? Have you explored custom pre-training objectives?"

> "What's your team's perspective on the from-scratch versus domain-adaptive pre-training debate? I can see arguments for both — starting from a general model gives you language understanding for free, but starting from scratch lets you design the tokenizer and architecture for the domain."

---

## Tier 4: Team & Process

These show you think about how great work gets done.

> "How does the research-to-production pipeline work for pre-training experiments? I've seen teams struggle with the gap between 'interesting research result' and 'model that actually trades' — how do you bridge that?"

> "What does a typical pre-training experiment cycle look like on your team? How long from hypothesis to validated result?"

> "How do you think about the build-versus-use decision for training infrastructure? Do you build custom training frameworks, or do you leverage existing ones like Megatron-LM or DeepSpeed and customize on top?"

---

## Tier 5: Big Picture

These show you care about where the field is going.

> "Where do you think the biggest unsolved problems are in financial foundation models right now? Is it data, architecture, evaluation, or something else entirely?"

> "How do you think about the competitive landscape — as more firms build foundation models, where does the sustainable edge come from? Is it data, talent, infrastructure, or methodology?"

---

## Questions to AVOID

- "What tech stack do you use?" — Too surface-level
- "How many GPUs do you have?" — Sounds like you're shopping
- "What's your model's accuracy?" — Shows misunderstanding of the problem
- "Do you use RAG?" — Makes it sound like you only know fine-tuning patterns
- Anything you could easily find on their website or LinkedIn
