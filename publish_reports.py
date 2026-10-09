"""Publish the HTML reports in Outputs/ to GitHub Pages (the `gh-pages` branch of this repo's origin).

Usage: .venv/Scripts/python publish_reports.py [--dry-run]

- Published: the deliverables under Outputs/ — `*.html` reports, `*.xlsx` workbooks, `*.pdf`, finished `*.docx`
  documents and the market dashboard PNG. The folder layout is kept, so the pages' relative links keep working.
- Never published (intermediate or cache files): JSON of any kind (fetched data, `_spec.json`, `_summary.json`,
  `.chart.json`), chart PNGs, generator scripts, CSV/TXT, and the per-component `.docx` files that
  `assemble_package.py` merges into the research package (see `is_deliverable`).
- Each HTML copy gets a "not investment advice" banner and a `noindex` meta tag; files in Outputs/ are unchanged.
- The branch is rebuilt from scratch and force-pushed each run, so the site always mirrors Outputs/ (anything
  deleted locally disappears from the site). It never touches `master`.
- Anyone with the link can read the site if the repo is public.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "Outputs")
BRANCH = "gh-pages"

BANNER = ('<div style="background:#fff4d6;color:#4a3b00;border-bottom:1px solid #e0c870;padding:8px 16px;'
          'font:13px/1.4 system-ui,sans-serif;text-align:center">AI-generated research for information only. '
          'Not investment advice, not a recommendation to buy or sell any security. Figures come from SEC EDGAR, '
          'Yahoo Finance and web sources and may be incomplete or out of date.</div>')
NOINDEX = '<meta name="robots" content="noindex,nofollow">'


def sh(args, cwd=None, check=True):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit(f"{' '.join(args)}\n{r.stdout}{r.stderr}")
    return r.stdout.strip()


DELIVERABLE_EXT = (".html", ".xlsx", ".pdf", ".docx")
_COMPONENT_DOCX = re.compile(r"(^|/)[1-8]_[^/]+_analysis_\d{8}\.docx$")
_NOTE_DOCX = re.compile(r"^(.*)_stock_deep_research_notes_(\d{8})\.docx$")


def is_deliverable(rel):
    """True for a finished output worth publishing; False for caches and intermediates."""
    rel = rel.replace(os.sep, "/")
    name = os.path.basename(rel).lower()
    if name.startswith("sentiment_dashboard_") and name.endswith(".png"):
        return True
    if not name.endswith(DELIVERABLE_EXT):
        return False
    if _COMPONENT_DOCX.search(rel):          # merged into the package by assemble_package.py
        return False
    m = _NOTE_DOCX.match(rel)
    if m and os.path.exists(os.path.join(OUT, f"{m.group(1)}_stock_deep_research_{m.group(2)}.docx")):
        return False                         # the merged package supersedes the bare note
    return True


def decorate(text):
    text = re.sub(r"(<head[^>]*>)", r"\1" + NOINDEX, text, count=1, flags=re.I)
    return re.sub(r"(<body[^>]*>)", r"\1" + BANNER, text, count=1, flags=re.I)


def main():
    dry = "--dry-run" in sys.argv
    files = []
    for dirpath, _, names in os.walk(OUT):
        files += [os.path.join(dirpath, n) for n in names if is_deliverable(os.path.relpath(os.path.join(dirpath, n), OUT))]
    if not any(os.path.basename(f) == "index.html" for f in files):
        raise SystemExit("Outputs/index.html is missing; run report_renderer.py --index first")

    site = tempfile.mkdtemp(prefix="reports_site_")
    for f in files:
        dest = os.path.join(site, os.path.relpath(f, OUT))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if f.lower().endswith(".html"):
            with open(f, encoding="utf-8") as src, open(dest, "w", encoding="utf-8") as out:
                out.write(decorate(src.read()))
        else:
            shutil.copyfile(f, dest)
    open(os.path.join(site, ".nojekyll"), "w").close()
    with open(os.path.join(site, "robots.txt"), "w") as f:
        f.write("User-agent: *\nDisallow: /\n")
    print(f"Staged {len(files)} files in {site}: " + ", ".join(f"{n} {e}" for e, n in sorted(
        {e: sum(f.lower().endswith(e) for f in files) for e in (".html", ".xlsx", ".pdf", ".docx", ".png")}.items(), key=lambda x: x[0]) if n))
    if dry:
        return

    remote = sh(["git", "remote", "get-url", "origin"], cwd=ROOT)
    name = sh(["git", "config", "user.name"], cwd=ROOT)
    email = sh(["git", "config", "user.email"], cwd=ROOT, check=False)
    ident = ["-c", f"user.name={name}", "-c", f"user.email={email or 'noreply@users.noreply.github.com'}"]
    sh(["git", "init", "-q", "-b", BRANCH], cwd=site)
    sh(["git", "add", "-A"], cwd=site)
    sh(["git", *ident, "commit", "-q", "-m", f"Publish reports {datetime.now():%Y-%m-%d %H:%M}"], cwd=site)
    sh(["git", "push", "-q", "--force", remote, f"{BRANCH}:{BRANCH}"], cwd=site)
    print(f"Pushed {BRANCH} to {remote}")

    m = re.search(r"github\.com[:/]([^/]+)/([^/.]+)", remote)
    if m:
        owner, repo = m.groups()
        sh(["gh", "api", "-X", "POST", f"repos/{owner}/{repo}/pages", "-f", f"source[branch]={BRANCH}",
            "-f", "source[path]=/"], check=False)   # already enabled -> harmless error
        print(f"Site: https://{owner}.github.io/{repo}/  (the first build can take a minute or two)")
    shutil.rmtree(site, ignore_errors=True)


if __name__ == "__main__":
    main()
