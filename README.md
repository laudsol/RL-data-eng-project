# RL-data-eng-project

**Data and performance assumptions**
1) Based on the brief, I have modeled the data such that 1 role in 90 is unique (20M unique roles of 1.8B).
2) The cache contains approxiamtely 1 year's worth of data (20M rows). I assume the cache is occasionally refined to remove roles from companies which not longer exist or have been renamed. 
3) the gPRC endpoint for the seniority model starts to queue when more than 1000 calls are made per second. To simulate the time effects of the service, I added a 1ms sleep method to the code


**Files**
The data directory should be used to hold data for testing the scripts. There are no files in it because pushing 5M rows of data to github is difficult and wasteful.

The populate directory can be used to popualte data files using differnt methods. 
- Populate_data uses the simplest method, creating unique ids and populating files such that each 90th row of data is unique
- Populate_cache fills the cache with 20M rows of data
- Distribute_data creates input data using statistically normal distribution
- Populate_cached_data uses the cache of 20M roles to populate an input file (1 in 90 roles are still unique)

The service directory contains the scripts for the data augmentation service. 
- When running perforamnce analyis on the scripts, I found that measurements were interfering with each other (for example, measuring memory artificially increased time). Sometimes, these discrepencies were large, so I decided to dupplicate the files and test each metric seperately.
- Seniority_time, Seniority_memory, Seniority_cpu test the base case for time, memory, and cpu time 
- Seniority_time_hot implements a hot cache and measures time to run the service

**Redis**
I selected Redis as the cache for the following reasons:
1) Can be stored in-memory, which is very fast
2) Performs persist operations, so a restart of the program wouldn't lose the caching data
3) Very efficient for single-layer read/write operations. When testing the code with an empty cache vs a cache with 20m rows of data, I saw virtually no slowdown in performance
4) Excellent documentation, and broad adoption means the internent will have lots of suplementary information

Setup docs: https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-mac-os/

**Scripts & code to measure performance**
time analysis line by line:
kernprof -l -v seniority.py

memory usage of keys in redis:
 redis-cli EVAL "local keys = redis.call('KEYS', '*'); local total_memory = 0; for _, key in ipairs(keys) do total_memory = total_memory + redis.call('MEMORY', 'USAGE', key); end; return total_memory" 0

memory usage for the script:
python3 -m memory_profiler seniority.py

Time:
start_time = time.perf_counter()
end_time = time.perf_counter()
total_time = end_time - start_time

CPU time:
start_time = time.process_time()
end_time = time.process_time()
total_cpu_time = end_time - start_time

Redis CPU time:
redis-cli INFO CPU | grep used_cpu (observe usage before and after running script)

Redis memory:
redis-cli info memory

**Testing and scaling**

The Base Case:

1) A single file is 5580 rows of data (8M rows per day, files processed one a minute)
2) Brief says file sizes may vary, so I tested files with increasing orders of magnitude to ensure performance is steady.
3) LI users seem to be resonably well distruibuted between Asia, Europe and the US: https://www.linkedin.com/pulse/important-linkedin-statistics-data-trends-oleksii-bondar-pqlie/
4) hile Revelio Labs writes lots of articles about the workforce in the US, there are some internationally-focus articles, indicating that RL does collect international data. For example: https://www.reveliolabs.com/news/business/european-tech-attracts-global-talent/
5) Based on #4, I surmised that RL processes files from job postings all over the world. These postings are in different time zones (see point #3), and I took the assumption that they are evenly distributed based on user distribution. For these reasons I made the file size for the base-case a simple average of the number of daily rows of data processed each minute.
6) Users can toggle between two databases in the redis cache. The first is for the base case, while the second can be populated with 20m rows of data to stress test the script
7) I tested the data with four increases in orders of magnitude (5k -> 50k -> 500k -> 8m). The time to process the data scaled linearly, so performance under current conditions is O(n)
8) About 75% of time to run the script is used by redis reads and writes. This leaves room for potential performance imporovement.

Hot Cache:

9) I wanted to see if I could achieve O(log n) time. 
10) One method for this is to index the cache. This is commonly implemented in conjunction with the recency of the search. However, I thought this would be counter-productive, since a company hiring for a given position would be unlikely to post another, duplicate role shortly thereafter. 
11) I settled on trying a hot cache based on frequency of role. My reasoning was that there are probably large companies hiring many people for the same role, so one would expect to see these postings again and again over time.
12) To test the hot cache, I thought it important to change how the test data was populated. Much of the data would need to already exist in the cache to see real increases in efficiency. 
13) I had worked on a script to populate data based on normal statistical distrubutions, but never had the oportunity to integrate this with the file in #12
14) I expected the hot cache to take a lot more time reading when roles were not in the first layer. The eviction policy would also take up time.
15) The gains from the top layer of the hot cache were nowhere near close enough to offset the extra time from the nested caching layer and the eviction analysis.
16) It seems likely that performance gains from the hot-cache would be noticed with a much larger cache, and a better constructed set of test data


**Learnings**
1) Redis Memory: Checking the memory used in redis seemed high relative to number of key-value pairs in the cache. Cleared the cache, and saw memory usage hadn't changed much. Researched and learned that redis uses fragmentation (ratio was ~2.7). Decided to measure key-value pairs directly, so wrote script. 
2) Profile Decorator: Can't use this to evaluate time of lines run in a loop because 
3) Code was running much slower one day to another. Clearing caches and restart services helps, but running on AWS or similar should provide the most control and consistency
