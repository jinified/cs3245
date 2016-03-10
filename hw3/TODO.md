## Knowledge

### Indexing
1. Dictionary - (term, doc frequency)
2. Posting list - (docID, term frequency) 

### Weighting
1. Term frequency - sum(1 + log10(tf))
2. Inverse Document Frequency - log10(N/df). N is total number of docs in corpus
3. tf-idf - tf * idf
4. SMART notation - ddd.qqq.
5. Implement lnc.ltc

### Similarity
1. Lenght normalize. Divide by L2 Norm
2. cosine similarity. dot product 

### Optimizations
1. Effective cosine ranking
 - no weighting on query
 - use max heap data structure 
2. Pruning non-contender 
 - index elimination
  - consider high idf query terms: like stopwording. ignore query term like "in"
  - consider doc containing many terms: computer score for doc with multiple terms
 - champion list: r docs of highest weight in term's posting list. if r < k, look from "low" list
3. Tiered-index
 - early termination
  - descending posting with w(tf)
  - stop after certain w(tf) threshold or docs
  - take union of all docs and compute score
 - idf ordered term
  - look from highest idf term 
4. Clustered pruning
 - pick sqrt(N) docs as leader at random 
 - for other docs, compute nearest leader
 - attach query to nearest L leader. Seek K nearest docs from L
5. Additional Information
 - model authority: query-independent score [0,1] 

### Metadata
1. Posting for each field value such as date and author. Conjunct with query 
2. Zone is region part of text. Encodes dictionary in zone
 
