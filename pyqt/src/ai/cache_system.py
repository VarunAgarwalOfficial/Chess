'''
Caching System for Chess Engine
Advanced caching mechanisms for improved performance
'''

from collections import OrderedDict
import time


class LRUCache:
    '''
    Least Recently Used cache with size limit
    Used for transposition table and evaluation cache
    '''

    def __init__(self, max_size=100000):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def get(self, key):
        '''Get value from cache, update access order'''
        if key in self.cache:
            self.hits += 1
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        else:
            self.misses += 1
            return None

    def put(self, key, value):
        '''Add value to cache, evict oldest if full'''
        if key in self.cache:
            # Update existing entry
            self.cache.move_to_end(key)
        else:
            # Add new entry
            if len(self.cache) >= self.max_size:
                # Remove oldest entry
                self.cache.popitem(last=False)

        self.cache[key] = value

    def clear(self):
        '''Clear all cache entries'''
        self.cache.clear()
        self.hits = 0
        self.misses = 0

    def get_hit_rate(self):
        '''Calculate cache hit rate'''
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total

    def __len__(self):
        return len(self.cache)


class TranspositionTable:
    '''
    Enhanced transposition table with replacement strategy
    Stores position evaluations to avoid redundant searches
    '''

    EXACT = 0
    LOWER_BOUND = 1
    UPPER_BOUND = 2

    def __init__(self, size_mb=256):
        # Calculate number of entries from memory size
        entry_size = 32  # bytes per entry (approximate)
        self.max_entries = (size_mb * 1024 * 1024) // entry_size

        self.table = {}
        self.generation = 0

        # Statistics
        self.lookups = 0
        self.hits = 0
        self.collisions = 0

    def probe(self, key, depth, alpha, beta):
        '''
        Look up position in table
        Returns (score, move, hit) tuple
        '''
        self.lookups += 1

        if key not in self.table:
            return (None, None, False)

        entry = self.table[key]

        # Check if stored depth is sufficient
        if entry['depth'] < depth:
            return (None, entry.get('move'), False)

        score = entry['score']
        flag = entry['flag']

        # Check if score is useful
        if flag == self.EXACT:
            self.hits += 1
            return (score, entry.get('move'), True)
        elif flag == self.LOWER_BOUND and score >= beta:
            self.hits += 1
            return (score, entry.get('move'), True)
        elif flag == self.UPPER_BOUND and score <= alpha:
            self.hits += 1
            return (score, entry.get('move'), True)

        # Score not useful, but return best move if available
        return (None, entry.get('move'), False)

    def store(self, key, depth, score, flag, move=None):
        '''
        Store position evaluation
        Enhanced replacement strategy for better hit rates:
        - Always replace if new entry is deeper (depth-preferred)
        - Replace old generation entries
        - Use aging to prioritize recent searches
        '''
        # Check if we should replace existing entry
        if key in self.table:
            existing = self.table[key]

            # Calculate replacement priority
            # Higher priority means more important to keep
            existing_priority = existing['depth'] * 4 + (1 if existing['generation'] == self.generation else 0)
            new_priority = depth * 4 + 2  # New entries get slight bonus

            # Keep existing if it has higher priority
            if existing_priority >= new_priority:
                # But always update if new search is significantly deeper
                if depth > existing['depth'] + 2:
                    pass  # Will replace
                else:
                    return  # Keep existing

            self.collisions += 1

        # Store new entry
        self.table[key] = {
            'depth': depth,
            'score': score,
            'flag': flag,
            'move': move,
            'generation': self.generation
        }

        # Limit table size (optimized cleanup)
        if len(self.table) > self.max_entries:
            self._cleanup()

    def _cleanup(self):
        '''Remove entries from old generations'''
        old_gen = self.generation - 2

        to_remove = []
        for key, entry in self.table.items():
            if entry['generation'] <= old_gen:
                to_remove.append(key)

            # Stop if we've freed enough space
            if len(to_remove) > self.max_entries // 4:
                break

        for key in to_remove:
            del self.table[key]

    def new_search(self):
        '''Increment generation counter for new search'''
        self.generation += 1

    def clear(self):
        '''Clear entire table'''
        self.table.clear()
        self.generation = 0
        self.lookups = 0
        self.hits = 0
        self.collisions = 0

    def get_stats(self):
        '''Get table statistics'''
        return {
            'size': len(self.table),
            'max_size': self.max_entries,
            'utilization': len(self.table) / self.max_entries,
            'lookups': self.lookups,
            'hits': self.hits,
            'hit_rate': self.hits / max(1, self.lookups),
            'collisions': self.collisions
        }


class EvaluationCache:
    '''
    Cache for board position evaluations
    Separate from transposition table for faster lookups
    '''

    def __init__(self, max_size=50000):
        self.cache = LRUCache(max_size)

    def get_eval(self, position_hash):
        '''Get cached evaluation for position'''
        return self.cache.get(position_hash)

    def store_eval(self, position_hash, evaluation):
        '''Store evaluation for position'''
        self.cache.put(position_hash, evaluation)

    def clear(self):
        '''Clear evaluation cache'''
        self.cache.clear()

    def get_stats(self):
        '''Get cache statistics'''
        return {
            'size': len(self.cache),
            'hit_rate': self.cache.get_hit_rate(),
            'hits': self.cache.hits,
            'misses': self.cache.misses
        }


class MoveCache:
    '''
    Cache for legal move generation
    Avoids regenerating moves for same position
    '''

    def __init__(self, max_size=10000):
        self.cache = LRUCache(max_size)
        self.generation = 0

    def get_moves(self, position_hash):
        '''Get cached moves for position'''
        entry = self.cache.get(position_hash)
        if entry and entry['generation'] == self.generation:
            return entry['moves']
        return None

    def store_moves(self, position_hash, moves):
        '''Store generated moves'''
        self.cache.put(position_hash, {
            'moves': moves,
            'generation': self.generation
        })

    def new_game(self):
        '''Increment generation for new game'''
        self.generation += 1

    def clear(self):
        '''Clear move cache'''
        self.cache.clear()


class PerftCache:
    '''
    Cache for perft (performance test) results
    Speeds up move counting and testing
    '''

    def __init__(self):
        self.cache = {}

    def get(self, position_hash, depth):
        '''Get cached perft result'''
        key = (position_hash, depth)
        return self.cache.get(key)

    def store(self, position_hash, depth, count):
        '''Store perft result'''
        key = (position_hash, depth)
        self.cache[key] = count

    def clear(self):
        '''Clear perft cache'''
        self.cache.clear()


class CacheManager:
    '''
    Manages all caching systems
    Provides unified interface and statistics
    '''

    def __init__(self):
        self.transposition_table = TranspositionTable(size_mb=256)
        self.evaluation_cache = EvaluationCache(max_size=50000)
        self.move_cache = MoveCache(max_size=10000)
        self.perft_cache = PerftCache()

        self.start_time = time.time()

    def clear_all(self):
        '''Clear all caches'''
        self.transposition_table.clear()
        self.evaluation_cache.clear()
        self.move_cache.clear()
        self.perft_cache.clear()

    def new_game(self):
        '''Prepare caches for new game'''
        self.move_cache.new_game()
        self.transposition_table.new_search()

    def get_memory_usage(self):
        '''Estimate memory usage in MB'''
        tt_size = len(self.transposition_table.table) * 32 / (1024 * 1024)
        eval_size = len(self.evaluation_cache.cache) * 16 / (1024 * 1024)
        move_size = len(self.move_cache.cache) * 128 / (1024 * 1024)

        return {
            'transposition_table': tt_size,
            'evaluation_cache': eval_size,
            'move_cache': move_size,
            'total': tt_size + eval_size + move_size
        }

    def get_all_stats(self):
        '''Get statistics from all caches'''
        return {
            'transposition_table': self.transposition_table.get_stats(),
            'evaluation_cache': self.evaluation_cache.get_stats(),
            'memory_usage': self.get_memory_usage(),
            'uptime': time.time() - self.start_time
        }

    def print_stats(self):
        '''Print comprehensive cache statistics'''
        stats = self.get_all_stats()

        print("\n=== Cache Statistics ===")
        print("\nTransposition Table:")
        tt = stats['transposition_table']
        print(f"  Size: {tt['size']:,} / {tt['max_size']:,} ({tt['utilization']:.1%})")
        print(f"  Hit rate: {tt['hit_rate']:.1%}")
        print(f"  Collisions: {tt['collisions']:,}")

        print("\nEvaluation Cache:")
        ec = stats['evaluation_cache']
        print(f"  Size: {ec['size']:,}")
        print(f"  Hit rate: {ec['hit_rate']:.1%}")

        print("\nMemory Usage:")
        mem = stats['memory_usage']
        print(f"  Transposition table: {mem['transposition_table']:.1f} MB")
        print(f"  Evaluation cache: {mem['evaluation_cache']:.1f} MB")
        print(f"  Move cache: {mem['move_cache']:.1f} MB")
        print(f"  Total: {mem['total']:.1f} MB")

        print(f"\nUptime: {stats['uptime']:.1f}s")
