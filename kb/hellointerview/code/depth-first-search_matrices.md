# Matrices

> Source: https://www.hellointerview.com/learn/code/depth-first-search/matrices
> Scraped: 2026-03-30



Bo Liu
Premium
• 5 months ago

Another common way to represent a graph is as a matrix (2D-grid). Each cell in the grid represents a node. The neighbors of each node are the cells that are adjacent to it (in the up, down, left, and right directions).

Is my understanding correct that you are saying in this representation a cell can have and only have 4 connected nodes? How is this enough to represent a graph?

1

Reply
W
WoodenAquamarineSnipe931
Top 10%
• 3 months ago

Not really, what they probably mean is that a matrix can be thought of as a graph with surrounding/adjacent cells as connected nodes. In this case, only 4 cells are being considered since only 4 directions are commonly relevant.

0

Reply
Ashley Yeong
Premium
• 2 months ago

page brief index not correct

0

Reply
I
InterestingAmethystFowl390
Premium
• 1 year ago

Another minor correction, the comment and initialized values of directions array don't match. It should be #left, #right, #down, #up

0

Reply
Xavier Elon
Premium
• 1 year ago

No it is correct as up, down, left, right

1

Reply
retr0
• 1 year ago

As @Xavier Elon said, it is correct. We are used to see coordinates in the format (x,y) so it is a little bit confusing. However in a matrix represented with a list of lists [[], [], []] your coordinates would be (y,x)

0

Reply
E
ExtendedBlackSheep683
• 1 year ago

Just a quick very minor correction! the line that initializes "directions" is missing a closing square bracket ].

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

