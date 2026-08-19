# CS50 AI "PageRank" project
## by Dyan Ahmadi

This project implements Google's PageRank algorithm in Python using two different approaches:

1. Sampling
2. Iteration

The project is part of CS50's Introduction to Artificial Intelligence with Python.

## Overview

PageRank assigns an importance score to each webpage based on the links between pages.

The project models a random web surfer who moves between pages by following links. A page that receives links from important pages has a higher probability of being visited and therefore receives a higher PageRank.

The implementation also includes an iterative mathematical approach that repeatedly recalculates PageRank values until they converge.

A page with no outgoing links is treated as though it links to every page in the corpus, including itself.

This ensures that the random surfer can always move to another page and that the probability distribution remains valid.

## PageRank Formula

The PageRank of a page is calculated using:

$$
PR(p) = \frac{1-d}{N} + d \sum_{i \in I_p} \frac{PR(i)}{NumLinks(i)}
$$
Where:

- `PR(p)` is the PageRank of page `p`
- `d` is the damping factor
- `N` is the total number of pages
- `Iₚ` is the set of pages linking to page `p`
- `PR(i)` is the PageRank of page `i`
- `NumLinks(i)` is the number of links from page `i`

# transition_model()
Calculates the probability distribution for the page visited next by the random surfer.

# sample_pagerank()
Estimates PageRank by generating random samples from the transition model.

# iterate_pagerank()
Calculates PageRank by repeatedly applying the PageRank formula until the values converge.

## Running the Program

Run the program by providing the corpus directory:

```bash
python pagerank.py corpus0
```

Other provided corpora can be tested in the same way.

For example:

```bash
python pagerank.py corpus1
python pagerank.py corpus2
```

The program prints PageRank results calculated using both sampling and iteration.

### Example Output

```text
PageRank Results from Sampling (n = 10000)
1.html: 0.2223
2.html: 0.4303
3.html: 0.2145
4.html: 0.1329

PageRank Results from Iteration
1.html: 0.2202
2.html: 0.4289
3.html: 0.2202
4.html: 0.1307
```


### Testing

CS50 provides automated tests for the project.

```bash
check50 ai50/projects/2024/x/pagerank
```

You can also check the code style with:

```bash
style50 pagerank.py
```

## Project Structure

```text
.
├── pagerank.py
├── corpus0/
├── corpus1/
├── corpus2/
└── README.md
```

# Course

CS50's Introduction to Artificial Intelligence with Python

Project: PageRank
