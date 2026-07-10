"""
The polytope MATH is verified. But the file annotates each polytope with a
'quantum' claim. Some are real established mathematics, some might be a stretch.
Verify what's actually true so the honest version states ONLY what's correct.
This checks the ONE claim that's cleanly checkable in code: that the 24-cell's
24 vertices form a group under quaternion multiplication (the binary tetrahedral
group 2T), which is the basis for the '1-qubit Clifford' correspondence.
"""
import numpy as np
from itertools import permutations, product

PHI = (1 + 5**0.5) / 2

def all_perms_signs(base):
    out = set()
    for p in set(permutations(base)):
        nz = [i for i,x in enumerate(p) if abs(x)>1e-12]
        if not nz: out.add(tuple(round(x,9) for x in p)); continue
        for s in product([-1,1], repeat=len(nz)):
            v=list(p)
            for k,i in enumerate(nz): v[i]=s[k]*abs(v[i])
            out.add(tuple(round(x,9) for x in v))
    return [np.array(v) for v in out]

# 24-cell vertices, scaled to unit quaternions
# The 24 vertices are the 8 from {±1,0,0,0} perms and 16 from {±1/2,±1/2,±1/2,±1/2}
V8 = all_perms_signs([1,0,0,0])                      # 8 unit quaternions (±1,±i,±j,±k)
V16 = [np.array(p,float) for p in product([-0.5,0.5], repeat=4)]  # 16 half-integer
verts = V8 + V16
verts = [v/np.linalg.norm(v) for v in verts]
print(f"24-cell: {len(verts)} vertices, all unit quaternions: "
      f"{all(abs(np.linalg.norm(v)-1)<1e-9 for v in verts)}")

def qmul(a, b):
    """Quaternion multiplication (a,b as [w,x,y,z])."""
    w1,x1,y1,z1 = a; w2,x2,y2,z2 = b
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
    ])

def find(v, verts, tol=1e-6):
    for u in verts:
        if np.linalg.norm(v-u) < tol: return True
    return False

# CLAIM: these 24 unit quaternions are CLOSED under multiplication (form a group)
closed = True
checked = 0
for a in verts:
    for b in verts:
        p = qmul(a, b)
        checked += 1
        if not find(p, verts):
            closed = False
            break
    if not closed: break

print(f"Closed under quaternion multiplication ({checked} products checked): {closed}")
print(f"=> The 24 vertices {'DO' if closed else 'DO NOT'} form the binary tetrahedral group 2T.")
print()
print("VERIFIED-TRUE annotations (established math, safe to state):")
print("  - 24-cell vertices = binary tetrahedral group 2T (order 24)  [checked above]")
print("  - 600-cell vertices = binary icosahedral group 2I (order 120) [same construction, known]")
print("  - These are the classical McKay correspondence facts (decades-old mathematics)")
print()
print("HONEST FRAMING: these are beautiful classical group-theory facts about 4D")
print("polytopes. Real mathematics. NOT a quantum computing tool, NOT novel, NOT")
print("connected to any synthesis system. A correct visualizer with correct labels.")
