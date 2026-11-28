"use strict";

// Compare single-descendant records with tracked E. coli family sizes.
function analyze(tables) {
  function requireCheck(condition, reason) {
    if (!condition) throw new Error(reason);
  }
  function readRows(csv) {
    const [header, ...lines] = csv.trimEnd().split(/\r?\n/);
    const fields = header.split(",");
    const keys = ["ID", "uID", "motherID", "daughter1ID", "daughter2ID", "Z", "Age"];
    const indices = keys.map(key => fields.indexOf(key));
    requireCheck(indices.every(index => index >= 0), "Unexpected columns");
    const rows = lines.map(line => {
      const parts = line.split(",");
      requireCheck(parts.length === fields.length, "Malformed CSV row");
      const [id, uid, parent, first, second, frame, age] =
        indices.map(index => parts[index] === "" ? NaN : Number(parts[index]));
      requireCheck([id, uid, parent, first, second, frame].every(Number.isInteger), "Malformed lineage IDs");
      return { id, uid, parent, first, second, frame, age };
    });
    const map = new Map(rows.map(row => [row.uid, row]));
    requireCheck(map.size === rows.length, "Duplicate uID");
    return { rows, map };
  }

  function known(age) {
    return Number.isInteger(age) && age >= 1 && age < 10;
  }

  function chronologicalTree(root, byId, stop) {
    const leaves = [];
    const splits = new Map();
    function trace(row, depth) {
      if (row.frame === stop) {
        leaves.push({ uid: row.uid, depth });
        return true;
      }
      const first = byId.get(row.first);
      if (!first || first.parent !== row.uid || first.frame !== row.frame + 1) return false;
      if (row.second === -2) {
        return first.id === row.id && trace(first, depth);
      }
      const second = byId.get(row.second);
      if (!second || second.uid === first.uid || second.parent !== row.uid || second.frame !== first.frame) {
        return false;
      }
      if (first.id === second.id || first.id === row.id || second.id === row.id) return false;
      splits.set(row.uid, row);
      return trace(first, depth + 1) && trace(second, depth + 1);
    }
    return trace(root, 0) ? { leaves, splits } : null;
  }

  function daughterOrder(row, byId) {
    const first = byId.get(row.first);
    const second = byId.get(row.second);
    if (!known(row.age) || !known(first.age) || !known(second.age)) return null;
    if (first.age === row.age + 1 && second.age === 1) return [first, second];
    if (second.age === row.age + 1 && first.age === 1) return [second, first];
    return null;
  }

  function runTable({ rows, map }, start, stop) {
    const roots = rows.filter(row => row.frame === start);
    const reverseLeaves = new Map();
    for (const leaf of rows.filter(row => row.frame === stop)) {
      let row = leaf;
      while (row && row.frame > start) {
        const parent = map.get(row.parent);
        row = parent && parent.frame === row.frame - 1 ? parent : null;
      }
      if (row?.frame === start) {
        if (!reverseLeaves.has(row.uid)) reverseLeaves.set(row.uid, []);
        reverseLeaves.get(row.uid).push(leaf.uid);
      }
    }
    const result = { starting: roots.length, incomplete: 0, ageRejected: 0, trees: [] };
    for (const root of roots) {
      const tree = chronologicalTree(root, map, stop);
      if (!tree) {
        result.incomplete++;
        continue;
      }
      const { leaves, splits } = tree;
      const reverse = reverseLeaves.get(root.uid) ?? [];
      if (reverse.length !== leaves.length || leaves.some(leaf => !reverse.includes(leaf.uid))) {
        result.incomplete++;
        continue;
      }
      requireCheck(leaves.length === splits.size + 1, "Unexpected leaf and division totals");
      if (!known(root.age) || Array.from(splits.values()).some(row => !daughterOrder(row, map))) {
        result.ageRejected++;
        continue;
      }

      function follow(pole) {
        let row = root;
        let depth = 0;
        while (row.frame < stop) {
          if (row.second === -2) {
            row = map.get(row.first);
          } else {
            row = daughterOrder(row, map)[pole];
            depth++;
          }
        }
        requireCheck(leaves.some(leaf => leaf.uid === row.uid && leaf.depth === depth), "Path does not end in its counted tree");
        return { leaf: row.uid, divisions: depth, estimate: 2 ** depth };
      }

      let probability = 0;
      let fairMean = 0;
      let fairSecondMoment = 0;
      const depths = {};
      for (const { depth } of leaves) {
        const weight = 2 ** depth;
        probability += 1 / weight;
        fairMean += weight / weight;
        fairSecondMoment += weight * weight / weight;
        depths[depth] = (depths[depth] ?? 0) + 1;
      }
      requireCheck(probability === 1 && fairMean === reverse.length, "Random-daughter control failed");
      result.trees.push({
        root: root.uid, initialAge: root.age, observed: reverse.length,
        old: follow(0), new: follow(1), fairMean,
        fairVariance: fairSecondMoment - fairMean ** 2, depths,
      });
    }
    requireCheck(result.starting === result.incomplete + result.ageRejected + result.trees.length, "Accounting failed");
    return result;
  }

  function summarize(audit) {
    const count = audit.trees.length;
    const sum = fn => audit.trees.reduce((total, row) => total + fn(row), 0);
    return {
      starting: audit.starting, incomplete: audit.incomplete, ageRejected: audit.ageRejected, included: count,
      dividing: sum(row => Number(row.observed > 1)), observed: sum(row => row.observed),
      old: sum(row => row.old.estimate), new: sum(row => row.new.estimate), randomMean: sum(row => row.fairMean),
      randomSD: Math.sqrt(sum(row => row.fairVariance)),
    };
  }

  const inputs = tables.map(({ name, csv }) => ({ name, table: readRows(csv) }));
  return [[8, 12], [7, 11], [9, 13]].map(([start, stop]) => {
    const results = inputs.map(({ name, table }) => {
      const audit = runTable(table, start, stop);
      return { name, ...summarize(audit), trees: audit.trees };
    });
    return { start, stop, results };
  });
}

function pool(window) {
  const outcomes = new Map([[0, 1]]);
  const totals = { starting: 0, incomplete: 0, ageRejected: 0, included: 0, dividing: 0,
    observed: 0, old: 0, new: 0, randomMean: 0, informative: 0, oldOver: 0, oldUnder: 0 };
  let probabilities = outcomes;
  for (const recording of window.results) {
    for (const key of ["starting", "incomplete", "ageRejected", "included", "dividing", "observed", "old", "new", "randomMean"]) {
      totals[key] += recording[key];
    }
    for (const tree of recording.trees) {
      if (tree.fairVariance > 0) totals.informative++;
      if (tree.old.estimate > tree.observed) totals.oldOver++;
      if (tree.old.estimate < tree.observed) totals.oldUnder++;
      const next = new Map();
      for (const [partial, prior] of probabilities) {
        for (const [depth, count] of Object.entries(tree.depths)) {
          const value = 2 ** Number(depth);
          const endpoint = partial + value;
          next.set(endpoint, (next.get(endpoint) ?? 0) + prior * count / value);
        }
      }
      probabilities = next;
    }
  }
  const distribution = [...probabilities.entries()].sort(([a], [b]) => a - b);
  const mass = distribution.reduce((sum, [, p]) => sum + p, 0);
  const mean = distribution.reduce((sum, [estimate, p]) => sum + estimate * p, 0);
  if (Math.abs(mass - 1) > 1e-12 || Math.abs(mean - totals.observed) > 1e-10) {
    throw new Error("Pooled fair-daughter control failed");
  }
  return { ...totals, distribution,
    atOrAboveOlder: distribution.reduce((sum, [estimate,p]) => sum + (estimate >= totals.old ? p : 0), 0) };
}

async function main() {
  const base = "https://raw.githubusercontent.com/funalab/pyCellLineage/60008ee698e23f6400bd62fb1a60579188e09377/Data/";
  const names = [
    "glc_poor/sample1", "glc_poor/sample2", "glc_poor/sample3",
    "glc_rich/sample1", "glc_rich/sample2", "glc_rich/sample3",
  ];
  const tables = await Promise.all(names.map(async name => {
    const response = await fetch(base + name + "/CellDf_wAge.csv");
    if (!response.ok) throw new Error("Data retrieval failed for " + name + ": " + response.status);
    return { name, csv: await response.text() };
  }));
  const results = analyze(tables).map(window => ({ ...window, pooled: pool(window) }));
  console.log(JSON.stringify(results, null, 2));
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
