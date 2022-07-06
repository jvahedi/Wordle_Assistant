$$ \textbf{Use the "Wordle\_Assistant.ipynb"and click on "Open in Colab" button at the top. Follow the instructions at the top}$$

Also there is a, still in construction, project on creating letter groups for a strategy guide in the secondary jupyter notebook files described below.

In here I try finding inter-character associations. The idea is that people playing the game should be able to know, if they got a hit on a specific letter, what other letter or cluster of letters are likely to be implicated in the 5-letter word. I created my original matrix using a multi-hot encoding for the 26 possible letters in each word. So the matrix was  (15,918 x 26) in size. 

At first approach I attempt to just build matrices that tell us how letters associate with one another such as a few kinds of cosine similarities and covariances. Yet this did not seem to strongly suggest much. It would not be something someone playing the game could digest in advance very well as it was too many discrete bits of information scattered across many letter to letter associations. I decided to change my approach. I wondered: a player does not play the game only via single letter to letter associations but rather possibly with letter chunks such as 3 letter that appear often together.

At first I used Latent Semantic Indexing to cast the original matrix into a low 2 or 3 dimensional space. After doing so I perceived a periodic and clustered pattern. I coded from scratch a clustering via a k-means classifier and ten additionally by hand using ellipses. Then I looked into each class, its frequency of letters. Unfortunately the seemed to be the issue that the letters were not sparse enough to be meaningful and I could not find strong patterns between clusters. Therefore the periodicity still remains a mystery at the moment. It may be the case that since the original matrix was organized alphabetically this periodicity would be an artifact of the column space decomposition. 

Finally I attempted a different cluster/semantic approach. I coded from scratch a number of different Non-Negative Matrix Factorization techniques for the original matrix. The idea was that the original matrix could be recreated using clusters of letters with weights for which of the words contributed to the emergence of these clusters.  Worse case scenario the matrix could be recreated using 26 semantics i.e. the letters of the alphabet. I aimed for 5-10. I used multiplicative updates and incorporated into this method explicit sparsity one one factor and normalization on another (normalization is required otherwise sparsity is trivially achieved by letting the other factor be large and the former small). I coded a total of about 5 different NMFs with different iterative schemes. 

Some notes on sparsity as I am trying to achieve a specific number of letters in a cluster (i.e. 3):
Since we are incentivized to match the original matrix closely as opposed to (relatively) achieving the regularization: we notice that one singular column is busy (low sparsity) while allowing the others to be practically sparse. This way it gets to be as sparse as it can be, while maintaining a close product match to the original matrix still. My guess is that as we reduce our restriction on regularization the difference between all the columns will disappear to similarly busy. In a comparable way if we increase the regularization constant our requirement to closely match the original matrix disappears and similar sparsity across all the columns can be enforced.
Sparsity coefficient needs to be re-tuned depending on the k rank of the factorization. One might want to find the relationship between the regularization and k to achieve similar sparsity on each column. More importantly, one can achieve both sparsity and semi-orthogonality buy simply increasing 'k'. 

I did find some success via NMF. I did not always get the same 'clusters' due to the stochasticity of initializations (and not tight enough constraints). Yet I did find some strong  repeated clusters such as letters 's t u' more consistently. There are ways to run many iterations and see if letters tend to end up in the same cluster of not, I read a paper on this but did not implement it.

I looked up, via another program I wrote (see char_hit_dist), how many letters have 's t u' in them out of the total words. It was 272 out of the total possible words 272/15,918 = .0171 . For comparison, I calculated what the probability of having any, of a specific three letters set (with possible repetition) show up in all possible made up 5 letter words are given there 26 letters; a binomial sum which I confirmed using a simulation had a value of .0128 . That ratio .0171/.0128 = 1.33 so that combo is 133% more likely than a random three letter combination. That value goes up if you do not allow for repetition a more accurate comparison to  4.37, over a 400% increase in probability to choosing a random three letter set!

The work ends here for now but I am continuing to look up new methods to improving the solution of this problem. I saw the wordle problem in certain ways in gaining a lot of popularity. My favorite math blogger recently approached the problem from an entropy/information theory perspective, although his goal is qualitatively different then mine. 
