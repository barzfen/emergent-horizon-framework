"""Verify preserved scientific source bytes and syntax; never execute legacy code."""
import ast, hashlib, json, warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    manifest=json.loads(Path(__file__).with_name('source-manifest.json').read_text())
    paths=sorted({x['destination'] for x in manifest})
    for item in manifest:
        data=(ROOT/item['destination']).read_bytes()
        assert len(data)==item['size_bytes']
        assert hashlib.sha256(data).hexdigest()==item['sha256']
    syntax_errors=[];print_only=[];encoding_bom=[]
    for rel in paths:
        p=ROOT/rel
        if p.suffix!='.py':continue
        data=p.read_bytes()
        if data.startswith(b'\xef\xbb\xbf'):encoding_bom.append(rel)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore',SyntaxWarning)
                tree=compile(data,str(p),'exec',flags=ast.PyCF_ONLY_AST)
        except SyntaxError as e:
            syntax_errors.append({'path':rel,'line':e.lineno,'error':str(e)})
            continue
        if not any(isinstance(x,(ast.Assert,ast.For,ast.While,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) for x in ast.walk(tree)):
            print_only.append(rel)
    report={'source_entries':len(manifest),'distinct_preserved_files':len(paths),'total_preserved_bytes':sum((ROOT/p).stat().st_size for p in paths),'source_hash_checks':'PASS','python_files':sum(Path(p).suffix=='.py' for p in paths),'syntax_errors':syntax_errors,'utf8_bom_files_accepted_by_python':encoding_bom,'scripts_without_assertions_loops_or_functions':print_only,'legacy_scripts_executed':False,'scope':'Byte integrity and Python syntax only. Does not certify mathematical results, historical outputs, dependencies or runtimes.'}
    Path(__file__).with_name('validation.json').write_text(json.dumps(report,indent=2)+'\n')
    assert not syntax_errors,syntax_errors
    print(json.dumps({k:v for k,v in report.items() if not isinstance(v,list)},indent=2))


if __name__=='__main__':main()
