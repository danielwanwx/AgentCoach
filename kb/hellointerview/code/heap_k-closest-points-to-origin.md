# K Closest Points to Origin

> Source: https://www.hellointerview.com/learn/code/heap/k-closest-points-to-origin
> Scraped: 2026-03-30


Heap
K Closest Points to Origin
medium
DESCRIPTION (inspired by Leetcode.com)

Given a list of points in the form [[x1, y1], [x2, y2], ... [xn, yn]] and an integer k, find the k closest points to the origin (0, 0) on the 2D plane.

The distance between two points (x, y) and (a, b) is calculated using the formula:

√(x1 - a2)2 + (y1 - b2)2

Return the k closest points in any order.

Example 1:

Inputs:

points = [[3,4],[2,2],[1,1],[0,0],[5,5]]
k = 3

Output:

[[2,2],[1,1],[0,0]]

Also valid:

[[2,2],[0,0],[1,1]]
[[1,1],[0,0],[2,2]]
[[1,1],[2,2],[0,0]]
...
[[0,0],[1,1],[2,2]]
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List
    [int]]:
        # Your code goes here
        pass
Results

AI Feedback

Past Submissions

Reset
View Answer
Run

Run your code to see results here

Have suggestions or found something wrong?

Explanation
Approach 1: Sorting
The simplest approach is to sort calculate the distance of each point from the origin and sort the points based on their distance. This approach has a time complexity of O(n log n) where n is the number of points in the array, and a space complexity of O(n) (to store the sorted array of distances).
Approach 2: Max Heap
This problem can be solved using a similar approach to the one used to solve Kth Largest Element in an Array. The key difference is that we need to store the k closest points to the origin, rather than the k largest elements. Since we are looking for the k smallest elements, we need a max-heap, rather than a min-heap.
By default, python's heapq module implements a min-heap, but we can make it behave like a max-heap by negating the values of everything we push onto it.
We add the first k points to the heap by pushing a tuple containing the negative of the distance from the origin, and the index of the point. After that is finished, our heap contains the k closest points to the origin that we've seen so far, with the point furthest from the origin at the root of the heap.
k = 3
VISUALIZATION
Python
Language
Full Screen
def k_closest(points, k):
    heap = []
    for i in range(len(points)):
        x, y = points[i]
        distance = x * x + y * y
        
        if len(heap) < k:
            heapq.heappush(heap, (-distance, i))
        elif distance < -heap[0][0]:
            heapq.heappushpop(heap, (-distance, i))
    
    return [points[p[1]] for p in heap]
[3, 4]
[2, 2]
[1, 1]
[0, 0]
[5, 5]

initialize heap

0 / 6

1x
Pushing the first `k = 3` elements onto the heap. The root of the heap after this is done holds a tuple containing the negative of the distance of the point furthest from the origin, and the index of that point (-25, 0).
For each point after the first k, we calculate the distance from the origin and compare it with the root of the heap. If the current point is closer to the origin than the root of the heap, we pop the root and push the current point into the heap. This way, the heap will always contain the k closest points to the origin we've seen so far.
k = 3
VISUALIZATION
Python
Language
Full Screen
def k_closest(points, k):
    heap = []
    for i in range(len(points)):
        x, y = points[i]
        distance = x * x + y * y
        
        if len(heap) < k:
            heapq.heappush(heap, (-distance, i))
        elif distance < -heap[0][0]:
            heapq.heappushpop(heap, (-distance, i))
    
    return [points[p[1]] for p in heap]
-25,0
-8,1
-2,2
[3, 4]
[2, 2]
[1, 1]
[0, 0]
[5, 5]
i = 2

push to heap

0 / 2

1x
At the end of the iteration, the heap will contain the k closest points to the origin. We can iterate over each point in the heap and return the point associated with each tuple.
k = 3
VISUALIZATION
Python
Language
Full Screen
def k_closest(points, k):
    heap = []
    for i in range(len(points)):
        x, y = points[i]
        distance = x * x + y * y
        
        if len(heap) < k:
            heapq.heappush(heap, (-distance, i))
        elif distance < -heap[0][0]:
            heapq.heappushpop(heap, (-distance, i))
    
    return [points[p[1]] for p in heap]
-8,1
-2,2
0,3
[3, 4]
[2, 2]
[1, 1]
[0, 0]
[5, 5]
i = 4

distance = 50

0 / 1

1x
Solution
nums
​
|
nums
list of integers
k
​
|
k
integer
Try these examples:
Origin
Spread
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def k_closest(points, k):
    heap = []
    for i in range(len(points)):
        x, y = points[i]
        distance = x * x + y * y
        
        if len(heap) < k:
            heapq.heappush(heap, (-distance, i))
        elif distance < -heap[0][0]:
            heapq.heappushpop(heap, (-distance, i))
    
    return [points[p[1]] for p in heap]
[3, 4]
[2, 2]
[1, 1]
[0, 0]
[5, 5]

k closest points to origin

0 / 11

1x
What is the time complexity of this solution?
1

O(1)

2

O(n log n)

3

O(n log k)

4

O(2ⁿ)

Mark as read

Next: Find K Closest Elements

How would you rate the quality of this article?

0.5 Stars
1 Star
1.5 Stars
2 Stars
2.5 Stars
3 Stars
3.5 Stars
4 Stars
4.5 Stars
5 Stars
Empty
Comments

(25)

Comment
Anonymous
​
Sort By
Popular
Sort By
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    public double distance(int x, int y) {
        double d = Math.sqrt(x * x + y * y);
        return d;
    }

    public int[][] kClosest(int[][] points, int k) {
        PriorityQueue<Pair<Integer, Double>> pq = new PriorityQueue<>((a, b) -> Double.compare(b.getValue(), a.getValue()));

        for(int i=0;i<points.length;i++){
            int x = points[i][0], y = points[i][1];
            double d = distance(x, y);

            pq.add(new Pair(i, d));

            if(pq.size() > k){
                pq.poll();
            } 
        }

        int[][] ans = new int[k][2];
        int i = 0;
        while(!pq.isEmpty()){
            Pair<Integer, Double> p = pq.poll();
            int idx = p.getKey();

            int[] point = {points[idx][0], points[idx][1]};

            ans[i++] = point;
        }

        return ans;
    }
}
Show More

5

Reply
Anxirex DEAD
• 1 year ago

Yes the answer does seems wrong !

5

Reply
M
ModerateRoseGrouse516
Premium
• 11 months ago

I was asked this question, and after implementing the max heap solution was asked for improvement still. With some prompting i arrived at the quickselect answer but couldnt code it up. Would it be a negative feedback that i could not come up with O(N) on my own and couldnt code it up?

3

Reply
VK
Varun Kolanu
Top 10%
• 5 months ago

Thanks for informing! I have learnt QuickSelect algorithm on your suggestion and the corresponding solution in CPP:

class Solution {
public:
    // QuickSelect Algorithm
    int getDistance(vector<int> point) {
        return point[0]*point[0] + point[1]*point[1];
    }

    int getPivot(vector<pair<int, int>> &distances, int l, int r) {
        int rightDist = distances[r].first;
        int i = l;
        for (int j=l; j<=r-1; ++j) {
            if (distances[j].first < rightDist) {
                swap(distances[i], distances[j]);
                ++i;
            }
        }
        swap(distances[i], distances[r]);
        return i;
    }

    void fillKSmallestIndices(vector<pair<int, int>> &distances, vector<int> &indices, int l, int r, int k) {
        int pivotIndex = getPivot(distances, l, r);
        if (pivotIndex - l == k -1) {
            for (int i=l; i<=pivotIndex; ++i) {
                indices.push_back(distances[i].second);
            }
            return;
        }

        if (pivotIndex-l >= k) {
            fillKSmallestIndices(distances, indices, l, pivotIndex-1, k);
            return;
        }

        for (int i=l; i<= pivotIndex; ++i) {
            indices.push_back(distances[i].second);
        }
        fillKSmallestIndices(distances, indices, pivotIndex+1, r, k - (pivotIndex - l + 1));
    }

    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        vector<pair<int, int>> distances;
        for (int i=0; i<points.size(); ++i) {
            distances.push_back({getDistance(points[i]), i});
        }

        vector<int> indices;
        fillKSmallestIndices(distances, indices, 0, points.size()-1, k);

        vector<vector<int>> ans;
        for (auto &ind: indices) ans.push_back(points[ind]);
        return ans;
    }
};
Show More

2

Reply
Johan Ospina
Premium
• 4 months ago

your code can be made a lot simpler and more legible

You don't need to pass an indices vector by reference, if you mutate the distances you will get a partition at k whose k - 1 elements to the left are left than k.
not sure how your idx logic is working, but I also don't think you need to do all that since the whole point of the partition step is to give you a global index in the array bounded by low and high

Here's a version that I believe works, except the test cases do imply ordering matters unlike in the problem statement where it does say that the order does not matter.

regardless it would be like a O(N) average case O(N^2) worst case for the quick select steps.

if you add sort step at the end it would be like a O(k log k) step.

using DistMapping = vector<pair<int, int>>;
class Solution {
public:
    int partition(DistMapping& points, int low, int high) {
        int partitionVal = points[high].first;
        int p = low;
        for (int i = low; i < high; i++) {
            if (points[i].first <= partitionVal) {
                swap(points[i], points[p]);
                p += 1;
            }
        }
        swap(points[p], points[high]);
        return p;
    }

    void quickSortLite(DistMapping& points, int low, int high, int k) {
        // invalid bounds 
        if (low >= high) {
            return;
        }
        // get pivot idx.
        int pIdx = partition(points, low, high);
        // if pIdx == k, we have partitioned k - 1 elements to the left of k that are at _least_ < distance[k]
        // so all together there are k elements that might not be 
        // in order but all have the following property
        // dist[j] < dist[k] for all j < k. 
        if (pIdx == k) {
            return; 
        }

        // partition index too high, let's try to find another
        // since pidx now guarantees that everything to the right
        // of pidx is greater this is valid. 
        if (pIdx > k) {
            return quickSortLite(points, low, pIdx - 1, k);
        }

        // partition index is too low here, due to previous cases.
        // we know everything to the left of pIdx is dist[j] < dist[p]. 
        return quickSortLite(points, pIdx + 1, high, k);
    }
    
    int distance(vector<int>& point) {
        return point[0] * point[0] + point[1] * point[1];
    }

    vector<vector<int>> kClosest(vector<vector<int>> points, int k) {
        
        // distance to index pairs, extract all the info we need
        vector<pair<int, int>> distances;
        for (int i = 0; i < points.size(); i++) {
            distances.push_back({distance(points[i]), i});
        }
        // now I want to do a modified quick sort / quick select
        // this will make distances be 'sorted' to the kth element
        quickSortLite(distances, 0, distances.size() - 1, k);

        vector<vector<int>> res;
        for (int i = 0; i < k; i++) {
            res.push_back(points[distances[i].second]);
        }
        
        return res;
    }
};
Show More

0

Reply
E
ExpensiveMagentaCrocodile897
Premium
• 8 months ago

I think this happened to me too half a year ago. Quickselect wasn't mentioned to me though, and I didn't come up with it (it wasn't taught in the resource I learnt from at the time).
T. I got feedback suggesting that they wanted something else, which must have been quickselect

2

Reply
Janina
• 2 months ago
• edited 2 months ago

Thanks, that's really helpful information! Another Python version of this problem with Quickselect:

import math
import random
from typing import List

class Solution:
    def distance(self, x1: int, y1: int) -> float:
        return math.sqrt(x1 ** 2 + y1 ** 2)

    def partition(self, left: int, right: int, distances: List[tuple]) -> int:
        pivot = distances[right]
        i = left
        for j in range(left, right):
            if distances[j][0] < pivot[0]:
                distances[j], distances[i] = distances[i], distances[j]
                i += 1
        distances[i], distances[right] = distances[right], distances[i]
        return i

    def quickselect(self, left: int, right: int, k: int, distances: List[tuple]) -> None:
        if left == right:
            return
        pivot_index = self.partition(left, right, distances)
        if k == pivot_index:
            return
        elif k < pivot_index:
            self.quickselect(left, pivot_index - 1, k, distances)
        else:
            self.quickselect(pivot_index + 1, right, k, distances)

    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        distances = [(self.distance(x, y), i) for i, (x, y) in enumerate(points)]
        self.quickselect(0, len(points) - 1, k - 1, distances)
        return [points[i] for (dist, i) in distances[:k]]
Show More

0

Reply
Aditya Bhadoriya
• 2 months ago
• edited 2 months ago

This solution is wrong. Attaching the correct one.

vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
    priority_queue<pair<int, int>> heap;
    for (int i = 0; i < points.size(); i++) {
        int x = points[i][0];
        int y = points[i][1];
        int distance = x * x + y * y;
        
        if (heap.size() < k) {
            heap.push({distance, i});
        } else if (distance < heap.top().first) {
            heap.pop();
            heap.push({distance, i});
        }
    }
    
    vector<vector<int>> result;
    while (!heap.empty()) {
        result.push_back(points[heap.top().second]);
        heap.pop();
    }
    return result;
    }
Show More

2

Reply
Daksh Gargas
Premium
• 29 days ago
• edited 29 days ago

Go Lang

import "container/heap"

type Point struct {
	x, y int
}

type PointsHeap []Point

func (h PointsHeap) Len() int { return len(h) }

func sqDistance(p Point) int64 {
	return int64(p.x * p.x) + int64(p.y * p.y)
}

// max distance stays on the top
func (h PointsHeap) Less(i, j int) bool {	
	return sqDistance(h[i]) > sqDistance(h[j])
}

func (h PointsHeap) Swap(i, j int) {
	h[i], h[j] = h[j], h[i]
}

func (h *PointsHeap) Push(val interface{}) {
	*h = append(*h, val.(Point))
}

func (h *PointsHeap) Pop() interface{} {
	old := *h
	n := len(old)
	val := old[n-1]
	*h = old[0:n-1]
	return val
}

func (h *PointsHeap) Peek() interface{} {
	return (*h)[0]
}

func kClosest(points [][]int, k int) [][]int {
    // Your code goes here
	h := &PointsHeap{}

	for _, val := range points {
		if h.Len() < k {
			heap.Push(h, Point {
				x: val[0],
				y: val[1],
			})
			continue
		}

		point := Point {
			x: val[0],
			y: val[1],
		}

		distance := sqDistance(point)

		if distance < sqDistance(h.Peek().(Point)) {
			heap.Pop(h)
			heap.Push(h, point)
		}
	}
	output := [][]int {}

	for h.Len() > 0 {
		val := heap.Pop(h).(Point)
		output = append(output, []int{val.x, val.y})
	}

    return output
}
Show More

1

Reply
Nikita Ivanov
• 8 days ago

I'm confused. the previous topics all taught me to implement the heap interface and use lib. But solution in current topic uses custom ds with own methods, completly bypassing the std library. Thank you for your approach, because it's actually the way i see the solution too.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Approach 1: Sorting

Approach 2: Max Heap

Solution
