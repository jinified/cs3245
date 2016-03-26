This is the README file for A0112213E's submission

== Personal Information ==
Matric No: A0112213E
Email: a0112213@u.nus.edu

== General Notes about this assignment ==

1. Third-party libraries and services used

lxml		- XML parser for both query and corpus 
whoosh		- full-text indexing and searching library  
terrier 	- open source IR platform with indexing and searching capability
WordNet		- large lexical database for English words
Wikipedia	- extra information about particular patent for query expansion
IPC			- retrieves definition for classes in corpus

2. XML Parsing

Uses lxml to parse query and corpus into native dictionary format. Fields without 
any content is set as empty string for ease of computation

3. Document Representation
 - includes `title`, `abstract`, `patent number` 

## Indexing 
## Query processing 
## Searching
## Evaluation

== Files included with this submission ==

ESSAY.txt		 - answers to essay questions
README.txt		 - readme file
util.py 	     - utility module for indexing and searching operation
index.py 	     - indexes files to dictionary and posting 
search.py        - searches dictionary and posting given a free text query
vector.py		 -
evaluator.py	 - 

== Statement of individual work ==

Please initial one of the following statements.

[x] I, A0112213E certify that we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, We
expressly vow that We have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[] I, A0112213E did not follow the class rules regarding homework
assignment, because of the following reason:

I suggest that We should be graded as follows:

== References ==

1. Al-Shboul, B., & Myaeng, S. H. (2014). Wikipedia-based query phrase expansion in patent class search. Information Retrieval, 17(5-6), 430-451.

2. Andersson, L., Mahdabi, P., Hanbury, A., & Rauber, A. (2013). Exploring patent passage retrieval using nouns phrases. In Advances in Information Retrieval (pp. 676-679). Springer Berlin Heidelberg.

3. Kim, J. (2007). Cluster-based patent retrieval. Inf. Process. Manage., 43(5).

4. Mahdabi, P. (2014). Query refinement for patent prior art search (Doctoral dissertation, Università della Svizzera italiana).

5. Mahdabi, P., & Crestani, F. (2014). Patent query formulation by synthesizing multiple sources of relevance evidence. ACM Transactions on Information Systems (TOIS), 32(4), 16.

6. Mahdabi, P., & Crestani, F. (2014). The effect of citation analysis on query expansion for patent retrieval. Information Retrieval, 17(5-6), 412-429.

7. Mahdabi, P., Keikha, M., Gerani, S., Landoni, M., & Crestani, F. (2011). Building queries for prior-art search (pp. 3-15). Springer Berlin Heidelberg.

8. Mahdabi, P., Gerani, S., Huang, J. X., & Crestani, F. (2013, July). Leveraging conceptual lexicon: query disambiguation using proximity information for patent retrieval. In Proceedings of the 36th international ACM SIGIR conference on Research and development in information retrieval (pp. 113-122). ACM.

9. Magdy, W., Lopez, P., & Jones, G. J. (2011). Simple vs. sophisticated approaches for patent prior-art search. In Advances in Information Retrieval (pp. 725-728). Springer Berlin Heidelberg.

10. Pal, D., Mitra, M., & Bhattacharya, S. (2015). Exploring Query Categorisation for Query Expansion: A Study. arXiv preprint arXiv:1509.05567.

11. Tannebaum, W., & Rauber, A. (2014). Using query logs of USPTO patent examiners for automatic query expansion in patent searching. Information Retrieval, 17(5-6), 452-470.

12. Xiao, T., Cao, F., Li, T., Song, G., Zhou, K., Zhu, J., & Wang, H. (2008). KNN and Re-ranking Models for English Patent Mining at NTCIR-7. In NTCIR.

13. Verma, M., & Varma, V. (2011, October). Patent search using IPC classification vectors. In Proceedings of the 4th workshop on Patent information retrieval (pp. 9-12). ACM.

