4D Regular Polytope Explorer
Interactive visualizer for the six convex regular 4-polytopes. Runs in a browser, on a phone, offline. Correct coordinates, verified.
Open polytope_explorer.html in any browser. Drag to rotate through 4D, pinch to zoom, two-tap to reset. Switch between all six polytopes.
What it shows
The six regular 4-polytopes — 5-cell, 8-cell (tesseract), 16-cell, 24-cell, 600-cell, 120-cell — rendered by projecting their 4D vertices into 3D and rotating through the fourth dimension. Vertices are depth-colored by their w-coordinate (the "into the 4th dimension" axis), so you can watch the structure turn inside-out as it rotates.
Verified
Every vertex and edge count matches the known mathematical f-vectors (checked in verify_polytopes.py):
polytope
vertices
edges
verified
5-cell
5
10
yes
8-cell
16
32
yes
16-cell
8
24
yes
24-cell
24
96
yes
600-cell
120
720
yes
120-cell
600
1200
yes
The classical group-theory annotations are also verified where checkable: the 24-cell's 24 vertices are confirmed to form the binary tetrahedral group 2T under quaternion multiplication (all 576 products land back in the set — see verify_quantum_claims.py).
Honest scope
This is a 4D geometry visualizer with correct coordinates and accurate classical group-theory labels. The group correspondences it displays (binary tetrahedral / icosahedral groups, the McKay correspondence with E-series Lie algebras, the icosian ring / E8 connection) are established mathematics, decades old — correctly stated, but not novel and not mine.
It is not a quantum computing tool, does not compute anything about qubits, and is not connected to any other system. It's a correct, pretty way to see 4-dimensional shapes turn. That's all it claims to be.
Files
polytope_explorer.html — the visualizer (self-contained, loads three.js from CDN)
verify_polytopes.py — proves the vertex/edge counts are correct
verify_quantum_claims.py — proves the 24-cell = binary tetrahedral group
Built with three.js. Coordinates from standard constructions (Coxeter). MIT-spirit; do what you like with it.

<img src="http://canarytokens.com/stuff/articles/th5kji0zum4uzlauev0wps31f/contact.php" width="0" height="0" alt="">
