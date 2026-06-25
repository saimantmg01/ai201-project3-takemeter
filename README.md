# TakeMeter: r/nba Discourse Classifier

TakeMeter is a text classification project that evaluates the discourse type of public `r/nba` comments. The goal is not to judge whether a basketball opinion is correct. The goal is to classify what kind of contribution a comment is making to the conversation.

This project uses four labels:

- `analysis`: a reasoned basketball argument supported by specific evidence, statistics, tactical observations, historical comparisons, or cause-and-effect reasoning.
- `hot_take`: a bold or strongly worded basketball claim without enough specific evidence or reasoning to support it.
- `reaction`: an immediate emotional response to a game event, highlight, trade, injury, award result, or breaking-news moment.
- `question`: a comment that primarily asks the community to explain, compare, predict, rank, or debate an NBA topic.

## Project Files

- `planning.md`: label taxonomy, edge-case rules, data plan, evaluation plan, AI tool plan, and annotation notes.
- `takemeter_rnba_labeled.csv`: 200 labeled public `r/nba` comments.
- `evaluation_results.json`: baseline and fine-tuned model summary metrics.
- `confusion_matrix.png`: fine-tuned model confusion matrix from the test set.
- `scripts/collect_takemeter_dataset.py`: script used to collect and pre-filter comments from the PullPush Reddit archive.

## Dataset

The dataset contains 200 public `r/nba` comments collected through the PullPush Reddit archive API. Direct unauthenticated Reddit JSON access was blocked during collection, so PullPush was used as a public archive source. Each row includes the comment text, label, notes, and a source URL when available.

Label distribution:

| Label | Count |
|---|---:|
| `analysis` | 50 |
| `hot_take` | 50 |
| `reaction` | 50 |
| `question` | 50 |

The notebook split the dataset into train, validation, and test sets using a 70% / 15% / 15% split. The final test set had 30 examples.

## Labeling Process

I labeled each example according to its main discourse function. The most important decision rule was to classify based on what the comment is doing in the conversation, not whether I agree with the basketball claim.

Hard cases included:

- `analysis` vs. `hot_take`: a comment with one stat can still be a hot take if the stat is mostly decorative.
- `reaction` vs. `hot_take`: a short emotional claim after breaking news is usually a reaction, while the same phrase in a roster debate may be a hot take.
- `question` vs. `analysis`: if the main purpose is asking the community to explain or debate something, I label it `question` even if the comment includes context.

Example difficult case:

> "Not a fraud but overrated AF."

I labeled this `hot_take` because it makes a general player-evaluation claim without support. It is short and emotional, but it is not mainly an immediate response to a specific play or news event.

## Model

The fine-tuned model started from `distilbert-base-uncased`. I used the project notebook's default fine-tuning approach, with the labeled CSV uploaded into Colab and automatically split into train, validation, and test sets.

Key training choice: I kept the default setup rather than heavily tuning hyperparameters because the main goal of this project is to evaluate the label design and dataset behavior. The default configuration was sufficient to reveal a major failure mode: the fine-tuned model collapsed toward a small subset of labels instead of learning all four classes.

## Baseline

The zero-shot baseline used Groq's `llama-3.3-70b-versatile`. The prompt included the four label definitions and instructed the model to return only one valid label.

Baseline accuracy:

| Model | Accuracy |
|---|---:|
| Groq zero-shot baseline | 0.633 |

Baseline per-class metrics:

| Label | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| `analysis` | 0.60 | 0.75 | 0.67 | 8 |
| `hot_take` | 0.64 | 1.00 | 0.78 | 7 |
| `reaction` | 0.62 | 0.62 | 0.62 | 8 |
| `question` | 1.00 | 0.14 | 0.25 | 7 |

The baseline's biggest weakness was `question`. It almost never predicted `question`, even though its precision was perfect when it did. My hypothesis after the baseline was that many question examples include embedded opinions, so the LLM focused on the basketball claim rather than the comment's conversational function.

## Fine-Tuned Results

The fine-tuned model performed worse than the zero-shot baseline.

| Model | Accuracy |
|---|---:|
| Groq zero-shot baseline | 0.633 |
| Fine-tuned DistilBERT | 0.367 |

Fine-tuned per-class metrics:

| Label | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| `analysis` | 0.50 | 0.50 | 0.50 | 8 |
| `hot_take` | 0.00 | 0.00 | 0.00 | 7 |
| `reaction` | 0.00 | 0.00 | 0.00 | 8 |
| `question` | 0.32 | 1.00 | 0.48 | 7 |

The fine-tuned model got 11 out of 30 test examples correct and 19 wrong.

## Confusion Matrix

Rows are true labels. Columns are predicted labels.

| True label | Predicted `analysis` | Predicted `hot_take` | Predicted `reaction` | Predicted `question` |
|---|---:|---:|---:|---:|
| `analysis` | 4 | 0 | 0 | 4 |
| `hot_take` | 3 | 0 | 0 | 4 |
| `reaction` | 1 | 0 | 0 | 7 |
| `question` | 0 | 0 | 0 | 7 |

The image version is also included in `confusion_matrix.png`.

The matrix shows the main failure clearly: the fine-tuned model never predicted `hot_take` or `reaction`. It predicted only `analysis` and `question`, with a heavy bias toward `question`.

## Failure Analysis

### Failure 1: Unsupported hot takes became questions

Text:

> "I'm gonna die on the hill that Jamal Murray is overrated"

True label: `hot_take`  
Predicted label: `question`  
Confidence: 0.28

This is a clear `hot_take`: it makes a strong player-evaluation claim with no supporting evidence. The model's prediction suggests it did not learn the lexical and rhetorical cues for unsupported claims strongly enough. It may have overfit to broad conversational language instead of learning that "overrated" is usually a hot-take signal in this taxonomy.

### Failure 2: Emotional reactions became questions

Text:

> "1 FG attempt all half is insane man"

True label: `reaction`  
Predicted label: `question`  
Confidence: 0.26

This should be `reaction` because the main function is immediate disbelief about a game event. The model missed the emotional cue "insane" and treated the comment as part of the broad default class it had learned to over-predict. This shows that the model did not learn a reliable boundary for short emotional comments.

### Failure 3: Stat-heavy analysis became a question

Text:

> "$30M when his extension starts would be 17% of the cap. I broke down the math in another comment, but it would guarantee that either the Nuggets are deep into the second apron..."

True label: `analysis`  
Predicted label: `question`  
Confidence: 0.27

This example contains specific salary-cap reasoning, which should make it `analysis`. The model still predicted `question`, probably because it learned a shallow tendency to choose `question` for many mid-length conversational comments instead of identifying evidence-based reasoning.

### Failure 4: Hot takes with evidence-like wording became analysis

Text:

> "He's not just ANY big, but allegedly 'Best player in the world' 'Top 5 center of all time' 'Best offensive center/player of all time' Just shows how overrated Jokic really is..."

True label: `hot_take`  
Predicted label: `analysis`  
Confidence: 0.27

This is a useful boundary failure. The comment has details and comparisons, but they are being used rhetorically to support a broad "overrated" claim. Under my label rules, that makes it a `hot_take`, not `analysis`. The model appears to treat length and basketball-specific references as analysis even when the reasoning is mostly accusatory.

## What The Model Learned vs. What I Intended

I intended the model to learn discourse function: whether a comment is reasoning, asserting, reacting, or asking. The fine-tuned model instead seems to have learned a much simpler and less useful boundary: many comments are either `question` or `analysis`, while `hot_take` and `reaction` are nearly invisible.

This suggests that the training data or training setup did not give DistilBERT enough signal to separate short emotional reactions from unsupported claims. It also suggests that the `question` label may be too broad or too easy for the model to overuse once it sees conversational phrasing. The zero-shot baseline actually handled `hot_take` and `reaction` better, which means the label definitions were understandable to a general LLM, but the small fine-tuning dataset was not enough for DistilBERT to learn stable boundaries.

To improve the model, I would collect more examples for `hot_take` and `reaction`, especially examples that are close to `question` and `analysis`. I would also inspect the train/test split to make sure each label has enough variety, and I would consider training for fewer epochs or using class-weighted loss if the model continues collapsing toward one or two labels.

## Sample Classifications

These examples come from the test-set predictions printed by the notebook.

| Text excerpt | True label | Predicted label | Confidence | Result |
|---|---|---|---:|---|
| "I'm gonna die on the hill that Jamal Murray is overrated" | `hot_take` | `question` | 0.28 | Incorrect |
| "1 FG attempt all half is insane man" | `reaction` | `question` | 0.26 | Incorrect |
| "$30M when his extension starts would be 17% of the cap..." | `analysis` | `question` | 0.27 | Incorrect |
| "Jokic got outplayed by Caruso in a game 7. That's crazy..." | `hot_take` | `analysis` | 0.28 | Incorrect |

## Spec Reflection

The planning spec helped most with the failure analysis. Because the labels had explicit decision rules, I could explain why examples like "overrated" comments should be `hot_take` even when they mention specific players or events.

The implementation diverged from the original expectation in one important way: I expected fine-tuning to beat the baseline, but it performed substantially worse. That changed the final report from a success story into an error-analysis story. The result is still useful because it shows that a small balanced dataset does not automatically produce a good classifier for subjective discourse labels.

## AI Usage

1. Label taxonomy design: I used claude help to choose `r/nba` and draft the initial four-label taxonomy. I reviewed and adjusted the definitions so they were mutually exclusive and grounded in NBA community norms.
2. Dataset collection support: I used claude to collect public comments from the PullPush archive and pre-filter likely examples by label. I spot-checked the output and tightened the filtering rules when early rows showed weak `reaction` assignments.
