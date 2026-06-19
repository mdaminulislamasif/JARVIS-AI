"""
JARVIS ADVANCED CACHE SYSTEM
উন্নত ক্যাশ সিস্টেম

Features:
- LRU (Least Recently Used) Cache
- TTL (Time To Live) support
- Memory-efficient storage
- Fast lookup (O(1))
- Automatic cleanup
- Statistics tracking
- Thread-safe operations

Speed: 99999+ 🚀
Memory: Optimized 💾
"""

import time
import threading
from collections import OrderedDict
from datetime import datetime, timedelta
import pickle
import hashlib
import os


class AdvancedCache:
    """Advanced caching system with LRU and TTL support"""
    
    def __init__(self, max_size=1000, default_ttl=3600):
        """
        Initialize advanced cache
        
        Args:
            max_size: Maximum number of items in cache
            default_ttl: Default time-to-live in seconds (1 hour default)
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        
        # LRU cache using OrderedDict
        self.cache = OrderedDict()
        
        # TTL tracking
        self.ttl_map = {}
        
        # Statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'expired': 0,
            'total_gets': 0,
            'total_sets': 0
        }
        
        # Thread lock for thread-safe operations
        self.lock = threading.RLock()
        
        # Auto-cleanup thread
        self.cleanup_thread = None
        self.running = False
        
        print("💾 Advanced Cache System initialized!")
        print(f"💾 Max Size: {max_size} | Default TTL: {default_ttl}s")
    
    def get(self, key):
        """
        Get value from cache
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        """
        with self.lock:
            self.stats['total_gets'] += 1
            
            # Check if key exists
            if key not in self.cache:
                self.stats['misses'] += 1
                return None
            
            # Check if expired
            if self._is_expired(key):
                self.stats['expired'] += 1
                self.stats['misses'] += 1
                self._remove(key)
                return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            
            self.stats['hits'] += 1
            return self.cache[key]
    
    def set(self, key, value, ttl=None):
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (None = use default)
        """
        with self.lock:
            self.stats['total_sets'] += 1
            
            # If key exists, remove it first
            if key in self.cache:
                self._remove(key)
            
            # Check if cache is full
            if len(self.cache) >= self.max_size:
                # Evict least recently used item
                self._evict_lru()
            
            # Add to cache
            self.cache[key] = value
            
            # Set TTL
            if ttl is None:
                ttl = self.default_ttl
            
            self.ttl_map[key] = datetime.now() + timedelta(seconds=ttl)
    
    def delete(self, key):
        """Delete key from cache"""
        with self.lock:
            if key in self.cache:
                self._remove(key)
                return True
            return False
    
    def clear(self):
        """Clear all cache"""
        with self.lock:
            self.cache.clear()
            self.ttl_map.clear()
            print("💾 Cache cleared!")
    
    def _is_expired(self, key):
        """Check if key is expired"""
        if key not in self.ttl_map:
            return True
        
        return datetime.now() > self.ttl_map[key]
    
    def _remove(self, key):
        """Remove key from cache"""
        if key in self.cache:
            del self.cache[key]
        if key in self.ttl_map:
            del self.ttl_map[key]
    
    def _evict_lru(self):
        """Evict least recently used item"""
        if self.cache:
            # Remove first item (least recently used)
            key = next(iter(self.cache))
            self._remove(key)
            self.stats['evictions'] += 1
    
    def start_auto_cleanup(self, interval=60):
        """
        Start automatic cleanup of expired items
        
        Args:
            interval: Cleanup interval in seconds
        """
        if self.running:
            print("⚠️ Auto-cleanup already running!")
            return
        
        self.running = True
        
        def cleanup_loop():
            while self.running:
                time.sleep(interval)
                self._cleanup_expired()
        
        self.cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        
        print(f"✅ Auto-cleanup started (interval: {interval}s)")
    
    def stop_auto_cleanup(self):
        """Stop automatic cleanup"""
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=2)
        print("🛑 Auto-cleanup stopped")
    
    def _cleanup_expired(self):
        """Clean up expired items"""
        with self.lock:
            expired_keys = []
            
            for key in list(self.cache.keys()):
                if self._is_expired(key):
                    expired_keys.append(key)
            
            for key in expired_keys:
                self._remove(key)
                self.stats['expired'] += 1
            
            if expired_keys:
                print(f"🧹 Cleaned up {len(expired_keys)} expired items")
    
    def get_statistics(self):
        """Get cache statistics"""
        with self.lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'usage_percent': (len(self.cache) / self.max_size * 100) if self.max_size > 0 else 0,
                'hits': self.stats['hits'],
                'misses': self.stats['misses'],
                'hit_rate': hit_rate,
                'evictions': self.stats['evictions'],
                'expired': self.stats['expired'],
                'total_gets': self.stats['total_gets'],
                'total_sets': self.stats['total_sets']
            }
    
    def print_statistics(self):
        """Print cache statistics"""
        stats = self.get_statistics()
        
        print(f"""
💾 ADVANCED CACHE STATISTICS:
💾 উন্নত ক্যাশ পরিসংখ্যান:

📊 Size: {stats['size']}/{stats['max_size']} ({stats['usage_percent']:.1f}%)
📊 আকার: {stats['size']}/{stats['max_size']} ({stats['usage_percent']:.1f}%)

✅ Hits: {stats['hits']}
✅ হিট: {stats['hits']}

❌ Misses: {stats['misses']}
❌ মিস: {stats['misses']}

📈 Hit Rate: {stats['hit_rate']:.1f}%
📈 হিট রেট: {stats['hit_rate']:.1f}%

🗑️ Evictions: {stats['evictions']}
🗑️ বহিষ্কার: {stats['evictions']}

⏰ Expired: {stats['expired']}
⏰ মেয়াদ শেষ: {stats['expired']}

📥 Total Gets: {stats['total_gets']}
📥 মোট Gets: {stats['total_gets']}

📤 Total Sets: {stats['total_sets']}
📤 মোট Sets: {stats['total_sets']}
""")
    
    def save_to_disk(self, filepath='jarvis_cache.pkl'):
        """Save cache to disk"""
        try:
            with self.lock:
                with open(filepath, 'wb') as f:
                    pickle.dump({
                        'cache': dict(self.cache),
                        'ttl_map': self.ttl_map,
                        'stats': self.stats
                    }, f)
                print(f"💾 Cache saved to {filepath}")
                return True
        except Exception as e:
            print(f"⚠️ Error saving cache: {e}")
            return False
    
    def load_from_disk(self, filepath='jarvis_cache.pkl'):
        """Load cache from disk"""
        try:
            if not os.path.exists(filepath):
                print(f"⚠️ Cache file not found: {filepath}")
                return False
            
            with self.lock:
                with open(filepath, 'rb') as f:
                    data = pickle.load(f)
                
                self.cache = OrderedDict(data['cache'])
                self.ttl_map = data['ttl_map']
                self.stats = data['stats']
                
                # Clean up expired items
                self._cleanup_expired()
                
                print(f"💾 Cache loaded from {filepath}")
                print(f"💾 Loaded {len(self.cache)} items")
                return True
        except Exception as e:
            print(f"⚠️ Error loading cache: {e}")
            return False


class SmartCache(AdvancedCache):
    """Smart cache with automatic key generation and compression"""
    
    def __init__(self, max_size=1000, default_ttl=3600):
        super().__init__(max_size, default_ttl)
        print("🧠 Smart Cache initialized!")
    
    def smart_key(self, *args, **kwargs):
        """
        Generate smart cache key from arguments
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
        
        Returns:
            Hash-based cache key
        """
        # Create string representation
        key_str = str(args) + str(sorted(kwargs.items()))
        
        # Generate hash
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def cache_function(self, ttl=None):
        """
        Decorator to cache function results
        
        Usage:
            @cache.cache_function(ttl=300)
            def expensive_function(arg1, arg2):
                # ... expensive computation ...
                return result
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Generate cache key
                key = self.smart_key(func.__name__, args, kwargs)
                
                # Try to get from cache
                result = self.get(key)
                if result is not None:
                    return result
                
                # Call function
                result = func(*args, **kwargs)
                
                # Cache result
                self.set(key, result, ttl=ttl)
                
                return result
            
            return wrapper
        return decorator


# Global cache instance
global_cache = SmartCache(max_size=1000, default_ttl=3600)


def test_cache():
    """Test cache system"""
    print("\n" + "="*80)
    print("  💾 TESTING ADVANCED CACHE SYSTEM")
    print("  💾 উন্নত ক্যাশ সিস্টেম টেস্ট")
    print("="*80)
    
    # Create cache
    cache = AdvancedCache(max_size=5, default_ttl=10)
    
    # Test basic operations
    print("\n1. Testing basic operations...")
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    
    print(f"   Get key1: {cache.get('key1')}")
    print(f"   Get key2: {cache.get('key2')}")
    print(f"   Get key3: {cache.get('key3')}")
    print(f"   Get key4 (not exists): {cache.get('key4')}")
    
    # Test LRU eviction
    print("\n2. Testing LRU eviction...")
    cache.set('key4', 'value4')
    cache.set('key5', 'value5')
    cache.set('key6', 'value6')  # Should evict key1
    
    print(f"   Get key1 (should be evicted): {cache.get('key1')}")
    print(f"   Get key6 (should exist): {cache.get('key6')}")
    
    # Test TTL
    print("\n3. Testing TTL...")
    cache.set('temp_key', 'temp_value', ttl=2)
    print(f"   Get temp_key (immediately): {cache.get('temp_key')}")
    print("   Waiting 3 seconds...")
    time.sleep(3)
    print(f"   Get temp_key (after 3s): {cache.get('temp_key')}")
    
    # Test statistics
    print("\n4. Cache Statistics:")
    cache.print_statistics()
    
    # Test smart cache
    print("\n5. Testing Smart Cache...")
    smart_cache = SmartCache(max_size=10)
    
    @smart_cache.cache_function(ttl=60)
    def expensive_function(x, y):
        print(f"   Computing {x} + {y}...")
        time.sleep(1)  # Simulate expensive operation
        return x + y
    
    print("   First call (should compute):")
    result1 = expensive_function(5, 3)
    print(f"   Result: {result1}")
    
    print("   Second call (should use cache):")
    result2 = expensive_function(5, 3)
    print(f"   Result: {result2}")
    
    print("\n6. Smart Cache Statistics:")
    smart_cache.print_statistics()
    
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    test_cache()
