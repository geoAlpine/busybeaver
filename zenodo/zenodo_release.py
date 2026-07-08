#!/usr/bin/env python3
# Zenodo release automation (2026-07-08).
#
#   ZENODO_TOKEN=xxx python3 zenodo/zenodo_release.py [--version 1.1] [--publish] [--sandbox]
#
# What it does:
#   1. rebuilds the curated package (build_package.py; aborts if self-containment fails)
#   2. first run: creates a NEW deposition; later runs: creates a NEW VERSION of the same
#      concept record (state kept in zenodo/.zenodo_record_id)
#   3. uploads the zip + sets metadata from metadata.json (version field overridden by --version)
#   4. leaves the deposit as a DRAFT for web review — publishing is IRREVERSIBLE, so it only
#      happens with an explicit --publish flag.
#
# Token: create at zenodo.org -> (avatar) -> Applications -> Personal access tokens,
#        scopes: deposit:write + deposit:actions.  NEVER commit the token.
import json, os, subprocess, sys, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SANDBOX = "--sandbox" in sys.argv
BASE = "https://sandbox.zenodo.org/api" if SANDBOX else "https://zenodo.org/api"
STATE = os.path.join(HERE, ".zenodo_record_id" + (".sandbox" if SANDBOX else ""))


def arg(flag, default=None):
    if flag in sys.argv:
        i = sys.argv.index(flag)
        return sys.argv[i + 1]
    return default

def api(method, path, data=None, raw=False, ctype="application/json"):
    tok = os.environ.get("ZENODO_TOKEN")
    if not tok:
        sys.exit("ZENODO_TOKEN not set (create one at zenodo.org -> Applications -> Personal access tokens)")
    url = path if path.startswith("http") else BASE + path
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}access_token={tok}"
    body = data if raw else (json.dumps(data).encode() if data is not None else None)
    req = urllib.request.Request(url, data=body, method=method)
    if body is not None:
        req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"Zenodo API error {e.code} on {method} {path}:\n{e.read().decode()[:800]}")

def main():
    version = arg("--version", "1.0")
    # 1. rebuild + self-test
    print("== rebuilding package ==")
    r = subprocess.run([sys.executable, os.path.join(HERE, "build_package.py"), "--version", version])
    zip_path = os.path.join(HERE, f"bb6-cryptid-frontier-v{version}.zip")
    if r.returncode != 0:
        sys.exit("build_package.py failed (self-containment) -- aborting release")

    # 2. create deposition or new version
    if os.path.exists(STATE):
        rec = open(STATE).read().strip()
        print(f"== creating new version of record {rec} ==")
        d = api("POST", f"/deposit/depositions/{rec}/actions/newversion")
        draft_url = d["links"]["latest_draft"]
        dep = api("GET", draft_url)
        # remove files inherited from the previous version
        for f in dep.get("files", []):
            api("DELETE", f["links"]["self"])
    else:
        print("== creating first deposition ==")
        dep = api("POST", "/deposit/depositions", {})
    dep_id = dep["id"]

    # 3. upload zip via the bucket API
    print(f"== uploading {os.path.basename(zip_path)} to deposition {dep_id} ==")
    bucket = dep["links"]["bucket"]
    with open(zip_path, "rb") as fh:
        api("PUT", f"{bucket}/{os.path.basename(zip_path)}", fh.read(), raw=True,
            ctype="application/octet-stream")

    # 4. metadata
    meta = json.load(open(os.path.join(HERE, "metadata.json")))
    meta["version"] = version
    api("PUT", f"/deposit/depositions/{dep_id}", {"metadata": meta})
    print(f"== metadata set (version {version}) ==")

    # persist the record id for future versions (conceptrecid groups versions)
    concept = str(dep.get("conceptrecid") or dep_id)
    open(STATE, "w").write(concept)

    if "--publish" in sys.argv:
        pub = api("POST", f"/deposit/depositions/{dep_id}/actions/publish")
        print("PUBLISHED. DOI:", pub.get("doi"))
        print("Concept DOI (all versions):", pub.get("conceptdoi"))
    else:
        print("DRAFT saved (not published). Review at:")
        print(f"  https://{'sandbox.' if SANDBOX else ''}zenodo.org/uploads/{dep_id}")
        print("Publish from the web UI, or re-run with --publish.")

if __name__ == "__main__":
    main()
