#!/usr/bin/env python2

if __name__ == '__main__':
    for i in xrange(1, 5):
        with open('q{}-qrels.txt.old'.format(i)) as q, open('q{}-qrels.txt'.format(i), 'w') as w:
            pos = []
            for i in q:
                i = i.split()
                for a, b in zip(i[::2], i[1::2]):
                    pos.append('{}  {}'.format(a, b))

            w.write('\n'.join(pos))
