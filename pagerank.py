import os
import random
import re
import sys
 
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distrbution = dict()
    num_pages = len(corpus)
    links = corpus[page]
    
    # if a page has no outgoing links, 
    # we treat it as having links to all pages in the corpus
    if len(links) == 0:
        probability = 1 / num_pages
        for p in corpus:
            distrbution[p] = probability
        return distrbution
    
    base_probability = (1 - damping_factor) / num_pages
    for p in corpus:
        distrbution[p] = base_probability
    
    link_probability = damping_factor / len(links)    
    for linked_pages in links:
        distrbution[linked_pages] += link_probability
        
    return distrbution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    visits = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))
    visits[current_page] += 1

    for _ in range(n - 1):
        distribution = transition_model(corpus, current_page, damping_factor)
        population = list(distribution.keys())
        weights = list(distribution.values())
        current_page = random.choices(population, weights=weights, k=1)[0]
        visits[current_page] += 1
    
    pagerank = {page: visits[page] / n for page in visits}
    return pagerank    



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    # we keep iterating until the page ranks change by less than 0.001
    # it was specified in the assignment pdf
    THRESHOLD = 0.001
    
    links_out = dict()
    for page in corpus:
        if len(corpus[page]) == 0:
            links_out[page] = set(corpus.keys())
        else:
            links_out[page] = corpus[page]
        
    linked = {page: set() for page in corpus}
    for page in corpus:
        for link in links_out[page]:
            linked[link].add(page)
    
    ranks = {page: 1 / num_pages for page in corpus}
    
    while True:
        new_ranks = dict()
        for page in corpus:
            # the pagerank formula :
            # R(p) = (1 - d) / N + d * sum( PR(i) / NumLinks(i) )
            first_term = (1 - damping_factor) / num_pages
            second_term = 0
            for linked_page in linked[page]:
                second_term += ranks[linked_page] / len(links_out[linked_page])
            second_term *= damping_factor
            new_ranks[page] = first_term + second_term
            
        max_change = max(abs(new_ranks[page] - ranks[page]) for page in corpus)
        ranks = new_ranks    
        if max_change < THRESHOLD:
            break
        
        total = sum(ranks.values())
        ranks = {page: rank / total for page, rank in ranks.items()}
    return ranks

if __name__ == "__main__":
    main()
