# TakeMeter

## Milestone 1: Community and Label Taxonomy

### Chosen Community

For this project, I will study discourse in `r/nba`, a large Reddit community focused on NBA games, players, trades, awards, statistics, and league news. This community is a strong fit for a discourse-quality classifier because posts and comments vary widely in how they argue: some users make evidence-based basketball analysis, some post confident unsupported takes, some react emotionally to live events, and some ask open discussion questions.

The distinction matters in this community because NBA discussion often turns on whether a comment is adding substance or just expressing a vibe. Regular participants already informally separate "film/stat analysis," "hot takes," "game-thread reactions," and "discussion prompts," so these labels reflect real community norms rather than an outside definition of quality.

### Labels

Each post or comment will receive exactly one label. The labels are designed to describe the main discourse function of the text, not whether I personally agree with it.

#### `analysis`

Definition: The post makes a reasoned basketball argument supported by specific evidence, such as statistics, film observations, tactical details, historical comparisons, or clearly explained cause-and-effect reasoning.

Clear examples:

- "The Wolves are forcing Denver's guards left on every high pick-and-roll, which keeps Jokic from getting the easy short-roll passes he normally uses to punish traps."
- "Brunson's scoring jump is not just higher usage; his free throw rate and pull-up three percentage both improved, so defenses have to guard him differently than they did in Dallas."

Boundary note: A post does not need a citation or formal stat table to count as `analysis`, but it does need to explain why the claim is true with specific basketball reasoning.

#### `hot_take`

Definition: The post makes a bold or strongly worded basketball claim without enough specific evidence or reasoning to support it.

Clear examples:

- "Tatum is never winning a title as the best player. He just does not have that killer mentality."
- "The Suns are cooked. That roster is fake good and everyone should have seen it coming."

Boundary note: A `hot_take` can be plausible or even correct. The label is about how the claim is presented: confident assertion first, support either missing, vague, or mostly decorative.

#### `reaction`

Definition: The post is mainly an immediate emotional response to a specific game event, highlight, trade, injury, award result, or breaking-news moment.

Clear examples:

- "No way he just hit that from the logo. This game is insane."
- "I cannot believe we traded him for that package. I am sick."

Boundary note: `reaction` posts may include an opinion, but the main purpose is to express a feeling in the moment rather than argue a broader claim.

#### `question`

Definition: The post primarily asks the community to explain, compare, predict, rank, or debate an NBA topic.

Clear examples:

- "Who would you rather build around for the next five years, Anthony Edwards or Shai Gilgeous-Alexander?"
- "Why do teams keep going under screens against Haliburton when he is clearly comfortable pulling up?"

Boundary note: A question can include context or a short opinion, but if the main function is inviting answers from the community, it should be labeled `question`.

### Mutual Exclusivity Rules

When a post could fit more than one label, I will use the following priority rules:

1. If the main purpose is asking the community for an answer, label it `question`, even if the question includes a short opinion.
2. If the main purpose is emotional response to a recent event, label it `reaction`, unless it develops a broader argument with specific evidence.
3. If the post makes a claim and gives specific basketball reasoning that would still support the claim without the emotional framing, label it `analysis`.
4. If the post makes a strong claim but the support is vague, missing, or mostly rhetorical, label it `hot_take`.

### Hard Edge Cases

The hardest expected edge case is the boundary between `analysis` and `hot_take`. NBA fans often use one statistic or one observation to make a dramatic claim, and that can look analytical on the surface without actually developing an argument.

Ambiguous example:

> "LeBron is overrated. His playoff win rate against top-seeded opponents is below .500."

Possible labels: `analysis` or `hot_take`.

Decision: I would label this `hot_take`. The post uses a specific statistic, but the stat is presented as a cherry-picked proof for a broad claim rather than as part of a reasoned argument. To count as `analysis`, the post would need to explain why that opponent-seed stat is the right measure, compare it to other players or contexts, or connect it to a clearer basketball argument.

Another difficult case is the boundary between `reaction` and `hot_take`.

Ambiguous example:

> "This team is pathetic. Blow it up tonight."

Possible labels: `reaction` or `hot_take`.

Decision: If this appears during or immediately after a specific loss, I would label it `reaction` because the main function is emotional venting. If it appears in a broader roster discussion thread without a clear immediate event, I would label it `hot_take` because it becomes an unsupported team-building claim.

### Label Fit Check

Before annotating the full dataset, I will read 30-40 recent `r/nba` posts or comments and check whether at least 90% can be assigned to one of these four labels without needing an "other" category. If one label dominates the sample or if many posts are ambiguous, I will revise the definitions before collecting the full 200-example dataset.

### Initial Data Collection Direction

I plan to collect public Reddit posts and comments from `r/nba`, using a mixture of:

- post-game threads and game threads for `reaction`
- discussion posts and player comparison threads for `question`
- long-form comment chains and statistical posts for `analysis`
- trade, award, and ranking debates for `hot_take`

I will aim for at least 50 examples per label in the initial 200-example dataset so no class is severely underrepresented.

## Milestone 2: Project Spec

### Community

I chose `r/nba` because it is active, public, text-heavy, and full of varied discourse styles. The same community contains short live-game reactions, unsupported player rankings, statistical arguments, tactical breakdowns, and open-ended debate prompts. That makes it a good fit for a classification project because the labels are not arbitrary: they describe discourse patterns that NBA fans already recognize.

This classifier is not trying to decide whether a basketball opinion is correct. It is trying to classify what kind of contribution a post or comment is making to the conversation.

### Labels

The four labels are:

- `analysis`: A reasoned basketball argument supported by specific evidence, statistics, tactical observations, historical comparisons, or cause-and-effect reasoning.
- `hot_take`: A bold or strongly worded basketball claim without enough specific evidence or reasoning to support it.
- `reaction`: An immediate emotional response to a game event, highlight, trade, injury, award result, or breaking-news moment.
- `question`: A post or comment that primarily asks the community to explain, compare, predict, rank, or debate an NBA topic.

These labels are mutually exclusive by using the decision rules from Milestone 1. If a post asks a real question, `question` usually wins. If it is mainly a short emotional response, `reaction` wins. If it makes a claim with specific basketball reasoning, it is `analysis`; if the claim is mostly unsupported assertion, it is `hot_take`.

### Hard Edge Cases

The hardest edge case is the boundary between `analysis` and `hot_take`. NBA comments often include one statistic or one basketball term inside a dramatic claim. I will label these as `analysis` only when the evidence is doing real argumentative work. If the stat is cherry-picked, unexplained, or mostly decorative, I will label the example `hot_take`.

The second hard boundary is `reaction` vs. `hot_take`. A short emotional comment like "Blow it up tonight" is a `reaction` if it appears as immediate venting after a game or transaction. The same phrase in a roster-building debate becomes a `hot_take` because it is functioning as an unsupported team-building claim.

The third hard boundary is `question` vs. `analysis`. Some questions include substantial context. I will label an example `question` if the main purpose is to invite an answer from the community, even if the author gives an opinion first.

### Data Collection Plan

I will collect at least 200 public `r/nba` comments. The dataset will be saved as a single CSV with these columns:

- `text`: the comment text
- `label`: one of `analysis`, `hot_take`, `reaction`, or `question`
- `notes`: collection and annotation notes
- `source_url`: Reddit permalink when available

The target distribution is 50 examples per label. If any label is underrepresented, I will collect targeted examples from threads where that discourse type is more common:

- `analysis`: statistical posts, tactical debates, player-performance discussions
- `hot_take`: award debates, player-ranking threads, trade reactions, legacy debates
- `reaction`: game threads, post-game threads, highlight threads, breaking-news threads
- `question`: discussion posts, comparison prompts, "why" and "who would you rather" threads

If a label accounts for more than 70% of the dataset after collection, I will collect more examples from the smaller classes before training.

### Evaluation Metrics

I will report overall accuracy because it gives a simple view of how often the classifier gets the label right. Accuracy alone is not enough because a model can perform well overall while failing badly on one label.

I will also report per-class precision, recall, and F1. These matter because the labels have different failure modes. Low `analysis` recall would mean the model misses substantive comments. Low `hot_take` precision would mean it wrongly dismisses other comments as unsupported takes. Low `question` recall would suggest the model is not learning the functional role of question-style posts.

I will include a confusion matrix because the most important result is likely not just how many errors happen, but which boundaries fail: `analysis` vs. `hot_take`, `reaction` vs. `hot_take`, or `question` vs. `analysis`.

### Definition of Success

For this small, subjective dataset, I would consider the fine-tuned model successful if it reaches at least 70% test accuracy and improves over the zero-shot Groq baseline by at least 5 percentage points. I would also want each label to have an F1 score of at least 0.60 so the model is not simply winning by over-predicting one easy class.

For a real community tool, "good enough" would require stronger performance: at least 80% accuracy, no class below 0.70 F1, and a review workflow for low-confidence predictions. I would not deploy this as an automatic moderation system. At best, it could help sort or summarize discourse types for human review.

### AI Tool Plan

For label stress-testing, I will give an AI tool the label definitions and ask it to generate borderline NBA comments between `analysis`/`hot_take`, `reaction`/`hot_take`, and `question`/`analysis`. If those examples are hard to classify, I will revise the decision rules before training.

For annotation assistance, I will use a script to pre-filter public comments into likely labels based on strong textual signals, then review the results and document difficult cases. I will not treat the script's label as automatically correct; the purpose is to speed up sorting while keeping the final taxonomy decision grounded in the definitions.

For failure analysis, after fine-tuning I will give the misclassified test examples to an AI tool and ask it to look for patterns, such as sarcasm, short comments, stat-heavy hot takes, or question posts with embedded opinions. I will verify any suggested pattern myself by rereading the examples before including it in the README.

## Milestone 3: Dataset Collection and Annotation

### Collection Source

I collected public `r/nba` comments using the PullPush Reddit archive API because direct unauthenticated Reddit JSON access was blocked by Reddit's network security during collection. The examples still come from public Reddit comment permalinks, and each row includes a `source_url` when the archive returned one.

The final dataset is saved as `takemeter_rnba_labeled.csv`.

### Annotation Process

I collected comments with targeted search terms for each label, then filtered out deleted comments, removed comments, link-heavy comments, very short fragments, and very long comments. I used the label definitions from Milestone 1 to assign each example one of the four labels.

The initial filtering script looked for strong cues such as question marks for `question`, evidence and basketball-reasoning terms for `analysis`, emotional phrases for `reaction`, and evaluative terms like "overrated," "washed," or "fraud" for `hot_take`. I then spot-checked the resulting rows and tightened the rules where the first pass mislabeled long argumentative comments as `reaction` only because they contained phrases like "no way."

### Label Distribution

The final CSV contains 200 examples:

| Label | Count |
|---|---:|
| `analysis` | 50 |
| `hot_take` | 50 |
| `reaction` | 50 |
| `question` | 50 |

No label is above 70% of the dataset, and each label has enough examples for the notebook's automatic 70% / 15% / 15% train-validation-test split.

### Difficult Annotation Examples

Example 1:

> "i think this stat is only counting players that make the team in the same season that they play with jokic. still dumb because murray has played to an all-star level throughout his playoff career, even if he isn't officially an all-star."

Possible labels: `analysis` or `hot_take`.

Decision: `analysis`. The tone includes "still dumb," but the comment explains a specific issue with how a stat is being counted and uses that to reason about Murray's playoff performance. The evidence is doing real work.

Example 2:

> "Not a fraud but overrated AF."

Possible labels: `hot_take` or `reaction`.

Decision: `hot_take`. It is short and emotional, but it makes a general player-evaluation claim rather than responding to a single moment. There is no supporting evidence, so it fits the unsupported-assertion definition.

Example 3:

> "No way he's getting paid more than brunson. Bobby lacking something up there and it's not his hair."

Possible labels: `reaction` or `hot_take`.

Decision: `reaction`. The comment is a short immediate response to a reported contract number. It contains an implied take, but the main function is surprise and disbelief about a specific news item.

Example 4:

> "Is this a real take? Jokic uses his forearm as a battering ram to post guys up . It goes both ways physicality on the post is part of ball So why does jokic need to use his forearm club in the post ?"

Possible labels: `question`, `analysis`, or `hot_take`.

Decision: `question`. The comment includes an argument about physicality in the post, but its main structure is challenging another user and asking why Jokic should be treated differently. Because it is framed as a request for explanation, `question` wins under the decision rules.

### Files Produced

- `planning.md`: project plan, label definitions, edge-case rules, evaluation plan, AI tool plan, and dataset documentation
- `takemeter_rnba_labeled.csv`: 200 labeled public `r/nba` comments with notes and source URLs
