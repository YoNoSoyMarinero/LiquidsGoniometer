from math import sqrt

def line_circle_intersection(p, lsp, lep):
    # p is the circle parameter, lsp and lep is the two end of the line
    x0, y0, r0 = p
    x1, y1 = lsp
    x2, y2 = lep
    if x1 == x2:
        if abs(r0) >= abs(x1 - x0):
            p1 = x1, y0 - sqrt(r0 ** 2 - (x1 - x0) ** 2)
            p2 = x1, y0 + sqrt(r0 ** 2 - (x1 - x0) ** 2)
            inp = [p1, p2]
            inp = [p for p in inp if p[1] >= min(
                y1, y2) and p[1] <= max(y1, y2)]
        else:
            inp = []
    else:
        k = (y1 - y2) / (x1 - x2)
        b0 = y1 - k * x1
        a = k ** 2 + 1
        b = 2 * k * (b0 - y0) - 2 * x0
        c = (b0 - y0) ** 2 + x0 ** 2 - r0 ** 2
        delta = b ** 2 - 4 * a * c
        if delta >= 0:
            p1x = (-b - sqrt(delta)) / (2 * a)
            p2x = (-b + sqrt(delta)) / (2 * a)
            p1y = k * x1 + b0
            p2y = k * x2 + b0
            inp = [[p1x, p1y], [p2x, p2y]]
            inp = [p for p in inp if p[0] >= min(
                x1, x2) and p[0] <= max(x1, x2)]
        else:
            inp = []
    return inp

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def tangents(y0, y0_int, x0, x0_int, x1_int, y1_int, x2):
    m_cd = (y0 - y0_int) / (x0 - x0_int)
    m_ab = -1 / m_cd
    c = - m_ab * x0_int + y0_int
    c1 = m_ab * x1_int + y1_int

    p1 = (x0_int, int(m_ab * x0_int + c))
    p2 = (x2, int(m_ab * x2 + c))
    p3 = (0, int(m_ab * 0 + c))

    p4 = (x1_int, int(-m_ab * x1_int + c1))
    p5 = (0, int(-m_ab * 0 + c1))
    p6 = (x2, int(-m_ab * x2 + c1))

    return p1, p2, p3, p4, p5, p6, m_ab, c, c1
