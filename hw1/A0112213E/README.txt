This is the README file for A0112213E's submission

== Personal Information ==
Matric No: A0112213E
Email: a0112213@u.nus.edu

== General Notes about this assignment ==

For each language in training data, a 6-gram language model is constructed with add-one
smoothing. The decision to use a 6-gram is made a simple counting method is used to 
calculate probability of the ngram model. Besides that, padding was not considered 
due to increase in storage space needed and little improvement to overall accuracy of the 
language model. In order to account for "alien" language, a simple threshold on 
the different number of matched ngram is used because there is a possibility that 
the "alien" language may match with a language model due to false positive. 


== Files included with this submission ==

ESSAY.txt		 - answers to essay questions
README.txt		 - readme file
utility.py 	     - utility module wrapping nltk's functions
build_test_LM.py - main module used to get prediction for any input file
eval.py          - compares predicted labels with correct labels  

== Statement of individual work ==

Please initial one of the following statements.

[/] I, A0112213E, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[/] I, A0112213E, did not follow the class rules regarding homework
assignment, because of the following reason:

In my opinion, we should be allowed to produce the code that would produce 
the best result with the resources given. Besides that, I believe the rules 
are there so that we realise the limitation of certain techniques or methodology and 
not to shackle the student from trying their best.

I suggest that I should be graded as follows:

I believe the accuracy of the code should not be used as a primary criteria to 
grade this assignment as we are provided with limited training data and we are required
to follow certain rules such as character-based ngram.

== References ==

1. http://stackoverflow.com/questions/2151517/pythonic-way-to-create-union-of-all-values-contained-in-multiple-lists
2. Discuss with Zhu Liang about possible approach to deal with unseen cases
