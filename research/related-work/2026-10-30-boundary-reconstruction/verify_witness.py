"""Independent closed-form check of the invisible-interior-edge example."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
from probe import ensemble, laplacian, response, transfer_signature, describe


def main():
    out = {'check': 'complete join with two hidden vertices', 'examples': []}
    for n in (5, 6):
        b = n - 2
        cs, es, unions, _ = ensemble(n)
        full = (1 << len(es)) - 1
        missing = full ^ (1 << es.index((b, b + 1)))
        assert full in unions and missing in unions
        A, B = [laplacian(g, n, es) for g in (full, missing)]
        assert transfer_signature(A, b) == transfer_signature(B, b)
        # Different edge counts ensure the graphs are non-isomorphic.
        assert full.bit_count() != missing.bit_count()
        checked = []
        for z in (0, F(1, 7), 1, 2, 3, 17):
            predicted = tuple((n + z if i == j else 0) - (1 + F(2, b + z))
                              for i in range(b) for j in range(b))
            assert response(A, b, z) == response(B, b, z) == predicted
            checked.append(str(z))
        out['examples'].append({'n': n, 'boundary_vertices': list(range(b)),
            'hidden_vertices': [b, b + 1], 'checked_z': checked,
            'equal_complete_transfer_signature': True,
            'graph_a': describe(full, n, es, cs, unions),
            'graph_b': describe(missing, n, es, cs, unions)})
    out['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_name('witness_checks.json').write_text(json.dumps(out, indent=2) + '\n')
    print('PASS: admissible triad witnesses, full response signatures and independent closed formula')


if __name__ == '__main__':
    main()
