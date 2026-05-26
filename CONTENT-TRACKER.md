# Content Tracker

Private tracker for all blog posts and their current status.

---

## Status Key

| Status | Meaning |
|--------|---------|
| **Published** | Live, public, ready to share |
| **Drafting** | Content written, still iterating |
| **Brainstorming** | Idea stage, outline or rough notes |
| **Needs Visuals** | Content done but visuals missing or need work |

---

## RL Data Pet Peeves Series

### Part 1: Why You Should Be Looking at Your Trajectories
- **Status:** Published
- **URL:** https://aurielws.github.io/posts/rl-pet-peeves-part-1/
- **Notes:** Live on main site. Covers trajectory inspection, why researchers need to look at their data.

### Part 2 (Harness Post): Stop Shipping Low-Quality Harnesses and Calling It an "Environment"
- **Status:** Drafting
- **URL (draft):** https://aurielws.github.io/writing-drafts/harness-failure-v3/
- **Password:** jase
- **Source file:** `harness failures post/v8-restructured.html`
- **Notes:** Static visuals (no JS). Has architecture diagram, 3 trajectory cascades, glossary page. Received two rounds of reviewer feedback. Intro reframed for "fix your broken harness" audience. Glossary at `/writing-drafts/harness-failure-v3/glossary.html`.

### Mini-Post: Your Rubric Was Written by Someone Who Has Never Done the Job
- **Status:** Published
- **URL:** https://aurielws.github.io/writing/rl-pet-peeves-rubric/
- **Source file:** `harness failures post/mini-post-1-rubric.html`
- **Notes:** Standalone post. Surface-Level vs Practitioner-Informed comparison visual. Extracted from Part 2 "Touch Grass" content.

### Mini-Post: Your Tasks Are Not Grounded in Economic Reality
- **Status:** Published
- **URL:** https://aurielws.github.io/writing/rl-pet-peeves-economic/
- **Source file:** `harness failures post/mini-post-2-economic.html`
- **Notes:** Standalone post. $200/hr vs $15/hr value tier visual. BLS data, startup PMF question, hud.ai mention.

### Mini-Post: Your Data Screams "This Is a Simulation"
- **Status:** Published
- **URL:** https://aurielws.github.io/writing/rl-pet-peeves-simulation/
- **Source file:** `harness failures post/mini-post-3-simulation.html`
- **Notes:** Standalone post. Branching flow diagram (Cheats / Reward Hacks / Checks Out). Anthropic introspection link.

### Part 2 (Full): You Should Be Talking to Someone Outside of Your AI Lab
- **Status:** Drafting
- **Source file:** `harness failures post/part2-v1.html`
- **Notes:** Combined version of all 3 mini-posts plus "What's Coming Next" section. Not yet deployed. May be superseded by the 3 standalone mini-posts.

---

## Future Posts (Brainstorming)

### Environment Quality Deep Dive
- **Status:** Brainstorming
- **Notes:** Low-quality harnesses, reward hacking rubrics, tasks that aren't scoped properly. The stuff that's broken before any training starts.

### Benchmarking to Determine Data Quality
- **Status:** Brainstorming
- **Notes:** You don't have a benchmark, you bought data in bulk and most of it is garbage, and you can't show the model actually learned something. Above-the-environment problems.

### RL Loss Analysis on Open Source Trajectories
- **Status:** Brainstorming
- **Notes:** High level example using [nebius/SWE-rebench-openhands-trajectories](https://huggingface.co/datasets/nebius/SWE-rebench-openhands-trajectories). Tutorial-style post for students learning RL.
