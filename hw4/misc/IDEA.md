## Automatic refinement of patent queries

1. Overview
 - extracts single term from patent using KL-divergence with collection 
 - expand query with selected key concepts
 - query dependent way of expanding 

2. Create a unigram language model
 - weighted log-likelihood with KL-divergence as normalization factor
