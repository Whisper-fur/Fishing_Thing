# Interesting Bugs
I wanted to have a space where I could share some of the interesting bugs I run across in this project and how I went about fixing them. I figure this is a decent way to show the process of coding this project and reminds me how to workk through them in the future.

## "Tangled up Lines"
If you are someone who fishes, this graph probably reminds you of when you let your friend borrow your baitcaster and you get it handed back with a bird's nest of fishing line in the reel. If you have no idea what I am talking about, it looks similar to my attempt at my "Bait Performance Over Time" table. Initially, I was using a plt.plot() to call on my whole DataFrame without separating by category (e.g., bait type or season). That led to lines being drawn between unrelated entries, creating a tangled mess. I fixed this by grouping the data by category (e.g., bait type) and plotted each group separately. A quick and easy fix, but something that looked interesting to say the least.

<p align="center">
  <img src="https://github.com/user-attachments/assets/83291476-2955-4dd7-a9c2-95651fc1e48f" width="45%" />
  <img src="https://github.com/user-attachments/assets/770aaa46-fcfc-41b8-8475-d43f8c2d0c95" width="45%" />
</p>


