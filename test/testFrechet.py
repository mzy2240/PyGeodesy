
# -*- coding: utf-8 -*-

# Test the Frechet distances.

__all__ = ('Tests',)
__version__ = '20.02.26'

from base import coverage, isPython3, isWindows, TestsBase

from pygeodesy import fStr, LatLon_, randomrangenerator

_rr = randomrangenerator('R')
_ms = [LatLon_(*_ll) for _ll in zip(_rr( -90,  90, 2),  # 90
                                    _rr(-180, 180, 4))]

_ps = [LatLon_(*_ll) for _ll in zip(_rr( -89,  90, 3),  # 60
                                    _rr(-179, 180, 6))]


class Tests(TestsBase):

    def test2(self, Frechet, x, y, **kwds):

        def _tstr(t):
            s = list(t[:5])
            s[0] = fStr(t.fd, prec=5)
            return '(%s)' % (', '.join(map(str, s)),)

        f = Frechet(_ms, fraction=1, **kwds)

        t = _tstr(f.discrete(_ps))
        self.test(f.named, t, x)  # + (t.units,)

        t = _tstr(f.discrete(_ps, fraction=0.5))
        self.test(f.named, t, y)  # + (t.units,)

        if not f.units:  # coverage
            f.units = 'test'

        self.testCopy(f)


if __name__ == '__main__':

    from pygeodesy import fractional, frechet_, \
                          FrechetDegrees, FrechetRadians, \
                          FrechetEquirectangular, FrechetEuclidean, \
                          FrechetHaversine, FrechetVincentys

    def _distance(p1, p2):
        dy, dx = abs(p1.lat - p2.lat), abs(p1.lon - p2.lon)
        if dx < dy:
            dx, dy = dy, dx
        return dx + dy * 0.5

    class FrechetDegrees_(FrechetDegrees):
        '''Custom Frechet.'''
        def distance(self, p1, p2):
            return _distance(p1, p2)

    class FrechetRadians_(FrechetRadians):
        '''Custom Frechet.'''
        def distance(self, p1, p2):
            dy, dx = abs(p1.phi - p2.phi), abs(p1.lam - p2.lam)
            if dx < dy:
                dx, dy = dy, dx
            return dx + dy * 0.5

    t = Tests(__file__, __version__)

    if isPython3:  # XXX different Random?
        t.test2(FrechetDegrees_, (178.5, 74, 56,   19,  5400),
                                 (175.5, 74, 52.5, 29, 10710))

        t.test2(FrechetRadians_, (3.11541, 74, 56,   19,  5400),
                                 (3.06305, 74, 52.5, 29, 10710))

        t.test2(FrechetEquirectangular, (7.1331,  8, 3, 138,  5400),
                                        (7.01295, 0, 0, 208, 10710))

        t.test2(FrechetEuclidean, (2.84717, 8, 3, 138,  5400),
                                  (2.76523, 0, 0, 208, 10710))

        t.test2(FrechetHaversine, (2.63867, 0, 0, 149,  5400),
                                  (2.63867, 0, 0, 208, 10710))

        t.test2(FrechetVincentys, (2.63867, 0, 0, 149,  5400),
                                  (2.63867, 0, 0, 208, 10710))

    elif isWindows:  # Python 2
        t.test2(FrechetDegrees_, (182.5,  83, 45,   21,  5400),
                                 (175.75, 83, 56.5, 12, 10710))

        t.test2(FrechetRadians_, (3.18523, 83, 45,   21,  5400),
                                 (3.06742, 83, 56.5, 12, 10710))

        t.test2(FrechetEquirectangular, (5.88254, 41, 18,    90,  5400),
                                        (5.90078, 40, 15.5, 137, 10710))

        t.test2(FrechetEuclidean, (2.6207,  49, 26, 74,  5400),
                                  (2.53749, 67, 34, 73, 10710))

        t.test2(FrechetHaversine, (1.75068, 49, 27,  73,  5400),
                                  (1.75068, 49, 27, 105, 10710))

        t.test2(FrechetVincentys, (1.75068, 49, 27,  73,  5400),
                                  (1.75068, 49, 27, 105, 10710))

    else:  # Python 2, elsewhere
        t.test2(FrechetDegrees_, (288.0, 1, 1, 147,  5400),
                                 (288.0, 1, 1, 205, 10710))

        t.test2(FrechetRadians_, (5.02655, 1, 1, 147,  5400),
                                 (5.02655, 1, 1, 205, 10710))

        t.test2(FrechetEquirectangular, ( 7.53702, 1, 3,   145,  5400),
                                        (12.58507, 0, 2.5, 203, 10710))

        t.test2(FrechetEuclidean, (2.81941, 1, 3,   145,  5400),
                                  (3.95734, 0, 2.5, 203, 10710))

        t.test2(FrechetHaversine, (1.81341, 18, 14,   117,  5400),
                                  (1.83289,  3,  4.5, 196, 10710))

        t.test2(FrechetVincentys, (1.81341, 18, 14,   117,  5400),
                                  (1.83289,  3,  4.5, 196, 10710))

    if coverage:  # for test coverage
        f = frechet_(_ms, _ps, distance=_distance, units='degrees')
        t.test('frechet_', f, "(178.5, 74, 56, 19, 5400, 'degrees')" if isPython3 else
                              "(288.0, 1, 1, 147, 5400, 'degrees')", known=True)

        t.test('[fi1]', fractional(_ms, f.fi1), '64.0°S, 096.0°E' if isPython3 else '38.0°S, 116.0°W', known=True)
        t.test('[fi2]', fractional(_ps, f.fi2), '41.0°S, 071.0°W' if isPython3 else '64.0°N, 121.0°E', known=True)

    t.results()
    t.exit()
