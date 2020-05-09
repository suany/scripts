# Note: this was authored to track down transitive include files for boost.
# It should be easily adaptable to general include tracing.

import re

root = [
    'boost/any.hpp',
    'boost/cregex.hpp',
    'boost/dynamic_bitset.hpp',
    'boost/functional/hash.hpp',
    'boost/lexical_cast.hpp',
    'boost/mpl/end.hpp',
    'boost/mpl/find.hpp',
    'boost/mpl/vector.hpp',
    'boost/preprocessor/cat.hpp',
    'boost/preprocessor/stringize.hpp',
    'boost/random.hpp',
    'boost/scoped_array.hpp',
    'boost/scoped_ptr.hpp',
    'boost/shared_ptr.hpp',
    'boost/smart_ptr.hpp',
    'boost/static_assert.hpp',
    'boost/tuple/tuple.hpp',
    'boost/type_traits/is_base_of.hpp',
    'boost/type_traits/is_convertible.hpp',
    'boost/type_traits/is_pointer.hpp',
    'boost/type_traits/is_same.hpp',
    'boost/unordered_map.hpp',
    'boost/unordered_set.hpp',
    'boost/variant/get.hpp',
    'boost/variant/variant.hpp',
    ]

todo = set(root)
done = set()
nonboost = set()

r1 = re.compile('# *include *<([^>]*)>')
r2 = re.compile('# *include *"([^"]*)"')

while todo:
    fn = todo.pop()
    done.add(fn)
    try:
        for l in open(fn):
            m = r1.search(l) or r2.search(l)
            if not m:
                continue
            ifile = m.group(1)
            if not ifile.startswith('boost/'):
                nonboost.add(ifile)
            elif not ifile in done:
                todo.add(ifile)
    except IOError, e:
        print e

print '{-- done'
for fn in done:
    print fn
print '}-- done'
print '{-- non-boost'
for fn in nonboost:
    print fn
print '}-- non-boost'
