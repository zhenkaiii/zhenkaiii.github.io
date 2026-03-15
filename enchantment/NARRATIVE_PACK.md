# NARRATIVE PACK
## CitSec — Financial Foundation Model Pre-Training Role

---
> **FORMAT UPDATE:** This interview includes **CoderPad coding** alongside discussion. Horia is mainly interested in how you **reason through problems, structure code, and debug** — not just the final answer. Thinking out loud is critical. See `pytorch_prep.txt` for coding prep.

> I am a hands-on Senior AI Researcher on Amazon AGI’s Frontier Foundation Model Training team, working end to end on large-scale foundation model pre-training.

> I am a core contributor to building Nova models from the ground up, covering both dense and Mixture-of-Experts systems across multiple training stages, including constant learning rate phases, ramp-down, and long-context extension. I have deep experience building pre-training data pipelines for curation, deduplication, and lineage tracking. I design targeted ablation studies to optimize training dynamics across stages and scaling regimes, and I have led domain-aware expert routing efforts that produced clear performance gains. 

> My background extends naturally to financial intelligence systems, where model quality, iteration speed, and efficiency directly shape decision outcomes. 

> I am particularly interested in applying these capabilities in trading environments such as Citadel Securities, where latency, reliability, and decision quality are first-order constraints. I have experience designing incrementally adaptable LLM systems that support both low-latency inference and longer-horizon reasoning.

> I am an independent, execution-focused researcher, comfortable owning real problems end to end and translating frontier model research into production systems with immediate, measurable impact.
---

---

One such role is of a Sr Research Scientist with the most advanced computational firms in the market, namely Citadel Securities. CitSec from a personnel perspective hire true best in class professionals and have developed a truly unique culture as a result of hiring individuals from AI and Tech. This particular business is being driven by a former Founding Member of Open AI who saw the opportunity AI can present within finance.

In terms of mandate, this Sr Research Scientist will be contributing to a new and highly critical Research initiative. The role will see the individual build out LLM’s and additional research infrastructure for different trading teams, trading at different latencies and asset classes. This position is centred around applying frontier deep learning/AI research to FS markets - you will be working on fine-tuning, evaluating and scaling models with a focus on models that advance financial intelligence, reasoning, and decision-making. 
As a result, we need an individual with a deep understanding of Large Language Models, Long context work, Pre-training and commercial gravitas. At CitSec you would have full ownership of real problems end to end, the scope is wide and the impact would be immediate.
---

Horia will ask you about the problems you have faced in these projects & how did you overcome these. 

He will be quite interested in your ambitions and how ambitious you are. 

He will not ask anything propriety but would like you to talk through your projects in details, the roadblocks experienced and how did you overcome these?

Essentially he wants to understand how you think and how you do things. 

They absolutely LOVE when people ask questions about their work, projects, application of pre-training, the big picture etc

This will not be a 'quant based' interview :) 

 I also know that Horia will ask how and why you got into pre-training, your rationale behind that, why you enjoy the area. 

Good to know:
This team are currently building really nuanced Foundational Models, which are essentially Trading Foundation Models. They are doing this by using Deep Learning and really modern machine learning to be at the forefront of the LLM world. In addition to this CitSec are also executing more vertical LLM's or specialised LLM's by using very specific and special data (i.e. Healthcare data being a prime example) which is where they have found an edge over so many other finance firms. It is certainly more focused at CitSec in terms of LLM's and data than it is in tech where the breadth of data tech firms are covering are far wider and broader if that makes sense. 

You may be asked a Pytorch question on the call. This has only happened with one other candidate so far so it is incredibly rare.
---
## 1. ORIGIN STORY — "Why Pre-Training?"

### The Core Thread
Your answer to "how and why did you get into pre-training" is the single most important narrative beat in this interview. Horia wants to hear *conviction*, not a career summary.

### Framework: The Three Layers

**Layer 1 — The Intellectual Hook** (what grabbed you)
> "I realized that pre-training is where you encode a model's *ontology* — its understanding of what the world is. Fine-tuning teaches it what to do. But pre-training teaches it what to see. That distinction fascinated me."

Personalize this with YOUR moment of realization. When did it click? Was it a paper? A failed experiment? A conversation? Be specific — specificity is what makes stories believable.

**Layer 2 — The Craft Obsession** (why you stayed)
> "What keeps me in pre-training is that it's simultaneously the most empirical and the most taste-driven part of ML. You can't A/B test your way to a good pre-training recipe — you need intuition about data, architecture, and compute tradeoffs. Then you validate that intuition at scale. That feedback loop is addictive."

**Layer 3 — The Ambition Vector** (where you're going)
> "I believe we're still in the early innings of domain-specific foundation models. General LLMs are impressive, but the real unlock comes when you pre-train on data that captures domain structure — time-series dynamics, market microstructure, clinical pathways. That's where I want to push."

This layer directly connects to CitSec's thesis (trading foundation models, vertical LLMs on specialized data).

---

## 2. PROJECT DEEP DIVES — The SPARK Framework

For every project, prepare to walk through this structure. Horia will probe — he wants to see *how you think*, not just what you built.

### S — Setup (10 seconds)
What was the project? What were you trying to achieve? Keep this brutally short.

### P — Problem (30 seconds)
What was the hard part? Why couldn't you just do the obvious thing? This is where you demonstrate you understood the *real* challenge, not just the surface task.

### A — Approach (60 seconds)
What did you try? Walk through your reasoning. Include dead ends — they show intellectual honesty. Structure:
- "My first instinct was X, because..."
- "That didn't work because..."
- "So I pivoted to Y, which was better because..."

### R — Roadblock (60 seconds)
What nearly killed the project? This is the money section. Horia specifically wants:
- What surprised you
- How you diagnosed the problem
- The creative/rigorous thinking that led to the solution
- Whether you asked for help and how

### K — Key Takeaway (15 seconds)
One sentence. What did you learn that you carry forward? Make it a *principle*, not a fact.

> Example: "I learned that data quality problems always compound nonlinearly — a 5% noise floor in your pre-training data doesn't cause 5% worse performance, it causes catastrophic forgetting in specific capability pockets."

---

## 3. AMBITION ARC — "How Ambitious Are You?"

Horia will probe this. He doesn't want "I want to be a senior engineer." He wants to see that you think about the *frontier*.

### Three Dimensions of Ambition to Convey

**Technical Ambition**
- Where do you think pre-training is going in 2-3 years?
- What's the next architectural breakthrough?
- What data modalities are underexplored?

> "I think the next wave isn't bigger models — it's models pre-trained on *structured* data that captures causal relationships. Markets aren't just text; they're interleaved signals across order books, news, filings, and macro indicators. A foundation model that sees all of these natively during pre-training, not just as fine-tuning adapters, could develop fundamentally different representations."

**Scope Ambition**
- You want to work on things that matter at scale
- You're drawn to CitSec because they're doing domain-specific foundation models with *proprietary data edges*, not just wrapping OpenAI APIs

**Craft Ambition**
- You care about doing things *well*, not just doing them
- You have opinions about training stability, data curation, evaluation methodology
- You find the details beautiful, not tedious

---

## 4. PERSONALITY HOOKS — What Makes You Memorable

### Hook 1: "The Contrarian Insight"
Have one opinion about pre-training that most people would disagree with. Defend it with evidence.

Examples:
- "I think most pre-training data filtering pipelines are too aggressive — they optimize for 'clean' data but throw away the messy, high-entropy examples that actually teach the model robustness."
- "I believe evaluation is the bottleneck, not compute. We don't know what our models can and can't do, so we can't make principled pre-training decisions."
- "I think domain-adaptive pre-training from a general checkpoint is fundamentally limited compared to pre-training from scratch on curated domain data — the general model's representations actively fight the domain signal."

### Hook 2: "The Debugging War Story"
Have one vivid, detailed story about a pre-training bug or failure that took days to diagnose. Include the emotional arc — frustration, the breakthrough moment, the lesson.

Make it *visceral*:
> "We were three weeks into a pre-training run when loss suddenly spiked. It wasn't a gradient explosion — the norms looked fine. It took us four days to figure out that a data pipeline worker had been silently shuffling a corrupted shard into the training mix every ~50k steps. The fix was 2 lines. The lesson was: always checksum your data pipeline outputs, not just your inputs."

### Hook 3: "The Genuine Question"
Ask Horia something you actually don't know the answer to. Not a performance question — a real one that shows you've been thinking about the problem space. (See `questions_to_ask.md` for curated options.)

### Hook 4: "The Taste Statement"
Express a preference about how pre-training *should* be done. Taste signals mastery.

> "I believe strongly in ablation-driven development for pre-training recipes. Before committing GPU-weeks to a full run, I spend real time on small-scale ablations to validate every decision — data mix ratios, learning rate schedules, architecture tweaks. It's tempting to just launch the big run, but cheap experiments are where the actual insights come from."

---

## 5. INTERACTION PIVOTS — Controlling the Conversation

### Pivot Type 1: Expand (when you have depth to show)
When Horia touches on a topic you know well:
> "That's a great question — and actually there's a subtlety there that I found really interesting in my work on [project]..."

### Pivot Type 2: Bridge (redirect to your strength)
When the conversation drifts to weak ground:
> "That's related to something I spent a lot of time on from a different angle — [your area]. What I found was..."

### Pivot Type 3: Elevate (zoom out to big picture)
When a question feels narrow or tactical:
> "At the tactical level, the answer is X. But what I think is more interesting is *why* that's the answer — it comes back to this fundamental tension in pre-training between..."

### Pivot Type 4: Engage (turn the interview into a conversation)
When you want to make it collaborative:
> "I'm curious how your team thinks about this — do you [hypothesis about their approach]?"
> "That's actually something I've been going back and forth on. What's your intuition?"

This is the pivot they love most. It signals confidence and genuine interest.

### Pivot Type 5: Ground (when you don't know something)
Never bluff. Horia will see through it.
> "I haven't worked with that directly, but my mental model would be [first-principles reasoning]. How does that map to what you've seen?"

This turns ignorance into an opportunity to demonstrate reasoning.

---

## 6. CONVERSATION FLOW — Reading the Room

### If Horia goes deep on theory:
Match his depth. Use precise terminology. Reference specific papers or techniques. Show you've done the reading *and* the implementation.

### If Horia goes broad on vision:
Think out loud. Share your view of where the field is headed. Connect it to CitSec's thesis. Be bold.

### If Horia challenges your answer:
Don't get defensive. Say: "That's a fair challenge — let me think about that." Then reason through it in real time. Thinking out loud under pressure is the highest-signal behavior in this format.

### If Horia asks about failures:
Be honest and specific. The story template: "I tried X → it failed because Y → I learned Z → and I've applied that since by doing W." Never frame failures as hidden successes. Frame them as genuine learning.

---

## 7. CLOSING FRAME — The Last Impression

End the conversation by connecting:
1. Your passion for pre-training (why you care)
2. CitSec's specific thesis (trading foundation models + vertical LLMs on specialized data)
3. What you'd be excited to work on day one

> "What excites me most about this role is that you're not just applying existing LLMs — you're building foundation models that see the world differently because they're pre-trained on data that captures market structure. That's the research frontier I want to be at. I'd love to dig into how your team is thinking about the data curation pipeline for these models."
