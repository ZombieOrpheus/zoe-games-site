"""Package explicit public assets from separate production and staging checkouts."""
import argparse
import json
import shutil
from pathlib import Path

PUBLIC = ('index.html', 'assets', 'games', 'labs')

def copy_site(source, destination, staging=False):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if source == destination or source in destination.parents:
        raise ValueError('Build output must be outside source checkout')
    destination.mkdir(parents=True, exist_ok=True)
    for name in PUBLIC:
        path = source / name
        if path.is_dir():
            shutil.copytree(path, destination / name, dirs_exist_ok=True)
        else:
            shutil.copy2(path, destination / name)
    if staging:
        for path in destination.rglob('*.html'):
            html = path.read_text()
            html = html.replace('<head>', '<head><meta name="robots" content="noindex,nofollow">', 1)
            path.write_text(html)
    (destination / '.nojekyll').touch()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--production', required=True)
    parser.add_argument('--staging', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = Path(args.output).resolve()
    if out.exists():
        raise SystemExit('Output already exists; choose a fresh directory')
    copy_site(args.production, out)
    copy_site(args.staging, out / 'staging', staging=True)
    cname = Path(args.production) / 'CNAME'
    if cname.exists():
        shutil.copy2(cname, out / 'CNAME')
    (out / 'robots.txt').write_text('User-agent: *\nDisallow: /staging/\n')
    print('Production and staging packaged successfully')
