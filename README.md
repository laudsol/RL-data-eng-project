# RL-data-eng-project

Research on caching options
1) Simple in-memory object: data will be wiped if program restarts
2) Redis: can persist the data to disk, so won’t lose everything in a restart
3) Memcached: make more memory available by pooling space from servers, won’t persist


**Redis**
Setup docs: https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-mac-os/

Key-value pairs are hashes, which are probably 256 bits. If we assume 20M pairs, thats 640MB. Way too big for L3 caching, which should be used for 1MB to 8MB. Should we then clear the l3 cache to keep it below 8MB or use a different mechanism?

Do I need to build in an expiration? Alex says 640MB not too big but internet disagrees....

Given 8M lines a day, assume each file has 350k lines (that's ~one file an hour)

Timing for Redis code:
Does it take longer to read/write to a larger cache? Largely not if its not on network, and the data is simple

Date is once a minute - consider that EU and US timezones will have most postings
Would it be faster to shard the caches? Look up company name first instead of saving them as key-value pairs? test both? If by company - values are dictionaries with titles as keys and seniority as values. 


**Scripts & code to measure performance**
time analysis line by line:
kernprof -l -v seniority.py

redis memory:
redis-cli info memory

memory usage of keys in redis:
 redis-cli EVAL "local keys = redis.call('KEYS', '*'); local total_memory = 0; for _, key in ipairs(keys) do total_memory = total_memory + redis.call('MEMORY', 'USAGE', key); end; return total_memory" 0

memory usage for the script:
python3 -m memory_profiler seniority.py

CPU time:
start_time = time.process_time()
end_time = time.process_time()
total_cpu_time = end_time - start_time

Redic CPU time:
redis-cli INFO CPU | grep used_cpu


**Learnings**
Redis Memory: Checking the memory used in redis seemed high relative to number of key-value pairs in the cache. Cleared the cache, and saw memory usage hadn't changed much. Researched and learned that redis uses fragmentation (ratio was ~2.7). Decided to measure key-value pairs directly, so wrote script. 

Profile Decorator: Adds time to run, so may not be reliable???

Code was running much slower one day to another

**Testing for normal use and scaling up**
The Base Case:
- Instructions day ~8M lines per day, with varying files sizes uploaded once a minute
- LI users seem to be resonably ll distruibuted between Asia, Europe and the US: https://www.linkedin.com/pulse/important-linkedin-statistics-data-trends-oleksii-bondar-pqlie/
- While Revelio Labs writes lots of articles about the workforce in the US, there are some internationally-focus articles, indicating that RL does collect international data. For example: https://www.reveliolabs.com/news/business/european-tech-attracts-global-talent/
- I have no data directly correlate the geographical location of LI users with new jobs postings. I explcitly assume that job postings are evenly distributed with geographic location of users.
- Given even geographic districution, there is little reason to think that availability of new data will vary with time of day file sizes would vary by the time of day the data is scraped. 
- I have created a file with 5500 lines of data to use as a baseline (8M lines per day  / 1440 minutes per day)

Stress Testing:
- The seniority model throttles at 1000 requests a second.
- After this, a req are queued. I want to see how the script will perform around this limit to determine if I should use multithreading or multiprocessesing.  
- To get to 1000 requests to the senioroty service, I'll need a file with 90,000 lines of data (we're told RL processed 1.8B lines and got 20M unique positions, a ratio of 1 / 90)
- Is a file with 90,000 lines reasonable? Under what circumstances would this happen? If the scraping service went down for 15 minutes, the backlog would be 90,000 lines. This seems realistic.
- The question is if my service can process 90,000 lines in a second.

Should I test with 20M key-value pairs in the Redis cache? Should I use this to come up with a retention policy???
