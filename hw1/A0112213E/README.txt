This is the README file for A0112213E's submission

== Personal Information ==
Matric No: A0112213E
Email: a0112213@u.nus.edu

== General Notes about this assignment ==

A language model is constructed for { malaysian, indonesian, tamil } with 
add-one smoothing to 4-gram from training data. Language models are stored in a
dictionary and the probability is calculated via nltk's FreqDist class which tabulates
each occurence of a 4-gram in training data. 

== Result of experimenting ==
1. Increasing N does not yield significantly better result due to limited amount of training data.
2. I have decided to use the number of matched ngram instead of probability because it may 
occur that an unknown may match with a particulat category.Therefore, the number of different match 
is used as a criteria and determined via trial and error.

== Files included with this submission ==

utility.py 	     - utility module wrapping nltk's functions
build_test_LM.py - main module used to get predection for any input file
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
to follow certain rules such as using 4-gram and character-based ngram.

== References ==

N/A
