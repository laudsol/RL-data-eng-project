# RL-data-eng-project

To Do:
1) Research how to measure time and space for python script
2) Make a large list of caching services, research pros/cons
3) Might want to implement multiple caching services to test time/space
4) Is there an angle to the augmentation service?
5) Populate a test file to run the script at scale? Will that make a difference to performance?
6) Should my cache be cloud-based or can it be local?

Research on caching options
1) Simple in-memory object: data will be wiped if program restarts
2) Redis: can persist the data to disk, so won’t lose everything in a restart
3) Memcached: make more memory available by pooling space from servers, won’t persist


Redis
Setup docs: https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-mac-os/
