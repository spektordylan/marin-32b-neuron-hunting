# Marin-32B Neuron Hunting

Exploratory analysis of neuron activations in the Marin-32B language model, as part of the [Station House Community Neuron Hunt](https://github.com/Station-House/marin-neuron-hunt).

This repository contains scripts for querying the [Marin-32B Neuron Atlas](https://huggingface.co/datasets/Station-house/marin-32b-neuron-atlas) and notes on individual neuron investigations.

## Current Investigation: L58-N7828

**Status:** In progress

### Initial Observations

- **Positive pole:** Strong activations frequently occur on function words preceding noun phrases, including `for`, `from`, and `of`.
- **Negative pole:** The strongest activations occur immediately before gerund-participial constructions (fancy way to say -ing words) like `having`, `getting`, `owning`, and `throwing`.
- **Working hypothesis:** Activation polarity may correlate with syntactic expectations, particularly nominal versus gerund-participial continuations.

### Evidence

#### Top three positive activations

| Rank | Activation | Firing Token | Context |
|---|---:|---|---|
| 0 | +29.75 | `for` | a Curriculum Framework for the Development of Catechetical Materials **[[for]]** People of High School Age establishes a specific curriculum framework for |
| 1 | +26.63 | `from` | Each serving delivers 150mg clinically researched Grape Seed Extract **[[from]]** the famous Loire Valley in France, and 500mg |
| 2 | +25.50 | `of` | who is accused of the Feb. 29 choke hold death **[[of]]** Antonio Valenzuela after he fled from a traffic stop, |

#### Top three negative activations

| Rank | Activation | Firing Token | Context |
|---|---:|---|---|
| 0 | -138.00 | `among` | you'll do if there's a significant space inside the timing **[[among]]** having your new home furniture and getting rid of the more aged |
| 1 | -73.50 | `and` | a significant space inside the timing among having your new home furniture **[[and]]** getting rid of the more aged furniture. There are several questions |
| 2 | -55.75 | `conflict` | they can be rather inexperienced and is probably not drawing near the **[[conflict]]** owning the most useful way of thinking. Also, recall the |

Firing tokens are marked with double brackets. Activation values are rounded to two decimal places. Mojibake in the original text has been cleaned where unambiguous.

### Ongoing Questions

- Does the pattern generalize beyond the strongest exemplars?
- Is the neuron sensitive to syntactic expectations or correlated lexical/contextual features?
- Can activation polarity be predicted from the preceding context?

### Experiments

*NotImplementedError*

### Conclusions

*To be determined.*