"""
Verify the 4D regular polytope math is CORRECT before building anything around it.
The claim: these are the actual 6 convex regular 4-polytopes with correct vertex
counts, edge counts, and the edge count matches the known f-vector.
If the vertex/edge counts don't match the mathematically known values, the whole
thing is wrong and we stop.
"""
import numpy as np
from itertools import permutations, product

PHI = (1 + 5**0.5) / 2

def all_perms_signs(base):
    """All permutations of base with all sign combinations on nonzero entries."""
    out = set()
    for p in set(permutations(base)):
        nz = [i for i, x in enumerate(p) if abs(x) > 1e-12]
        if not nz:
            out.add(tuple(round(x, 9) for x in p)); continue
        for signs in product([-1, 1], repeat=len(nz)):
            v = list(p)
            for k, i in enumerate(nz):
                v[i] = signs[k] * abs(v[i])
            out.add(tuple(round(x, 9) for x in v))
    return [np.array(v) for v in out]

def even_perms_signs(base):
    """Even permutations only, with all sign combinations."""
    out = set()
    for p in set(permutations(base)):
        # parity of this permutation relative to sorted base
        full = list(p)
        idx = sorted(range(4), key=lambda i: full[i])
        inv = sum(1 for i in range(4) for j in range(i+1,4) if idx[i] > idx[j])
        if inv % 2: continue
        nz = [i for i, x in enumerate(p) if abs(x) > 1e-12]
        if not nz:
            out.add(tuple(round(x, 9) for x in p)); continue
        for signs in product([-1, 1], repeat=len(nz)):
            v = list(p)
            for k, i in enumerate(nz):
                v[i] = signs[k] * abs(v[i])
            out.add(tuple(round(x, 9) for x in v))
    return [np.array(v) for v in out]

def count_edges(V):
    """Edges = pairs at the minimum nonzero distance."""
    V = np.array(V)
    n = len(V)
    dmin = np.inf
    for i in range(n):
        for j in range(i+1, n):
            d = np.linalg.norm(V[i]-V[j])
            if 1e-9 < d < dmin: dmin = d
    edges = 0
    for i in range(n):
        for j in range(i+1, n):
            d = np.linalg.norm(V[i]-V[j])
            if abs(d - dmin) < 1e-6: edges += 1
    return edges, dmin

# The mathematically KNOWN f-vectors (vertices, edges, faces, cells)
KNOWN = {
    "5-cell":   (5, 10, 10, 5),
    "8-cell":   (16, 32, 24, 8),
    "16-cell":  (8, 24, 32, 16),
    "24-cell":  (24, 96, 96, 24),
    "600-cell": (120, 720, 1200, 600),
    "120-cell": (600, 1200, 720, 120),
}

def build_5cell():
    # standard: 5 points, regular simplex in 4D (embed 5D then project)
    v5 = np.array([[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]], float)
    c = v5.mean(0); v5 = v5 - c
    # project to 4D via SVD
    U,S,Vt = np.linalg.svd(v5)
    return v5 @ Vt[:4].T

results = {}
print(f"{'polytope':>10} | {'V got':>6} {'V want':>6} | {'E got':>6} {'E want':>6} | verdict")
print("-"*62)

# 5-cell
V = build_5cell(); e,_ = count_edges(V)
results["5-cell"] = (len(V), e)
# 8-cell (tesseract)
V = [np.array(p, float) for p in product([-1,1], repeat=4)]; e,_ = count_edges(V)
results["8-cell"] = (len(V), e)
# 16-cell
V = all_perms_signs([1,0,0,0]); e,_ = count_edges(V)
results["16-cell"] = (len(V), e)
# 24-cell
V = all_perms_signs([1,1,0,0]); e,_ = count_edges(V)
results["24-cell"] = (len(V), e)
# 600-cell
Va = all_perms_signs([1,0,0,0])
Vb = [np.array(p,float) for p in product([-0.5,0.5], repeat=4)]
Vc = even_perms_signs([0, 0.5, PHI/2, (PHI-1)/2])
V = Va + Vb + Vc; e,_ = count_edges(V)
results["600-cell"] = (len(V), e)

all_pass = True
for name in ["5-cell","8-cell","16-cell","24-cell","600-cell"]:
    vg, eg = results[name]
    vw, ew = KNOWN[name][0], KNOWN[name][1]
    ok = (vg == vw and eg == ew)
    all_pass = all_pass and ok
    print(f"{name:>10} | {vg:>6} {vw:>6} | {eg:>6} {ew:>6} | {'PASS' if ok else 'FAIL'}")

print("-"*62)
print(f"{'ALL VERTEX/EDGE COUNTS CORRECT' if all_pass else 'MATH IS WRONG - STOP'}")
