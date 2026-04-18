# Contacts API - Fix Report

## Problem 1

**What was wrong:**
The `venv/` folder was committed to the repository. There was no `.gitignore` file.

**Why it is a problem:**
The virtual environment contains paths and binaries specific to one machine. 
Committing it causes problems for every other developer who clones the repo - 
their machine is not the same, and the paths inside the venv will not match. 
Virtual environments are never shared, they are always created locally from 
the recorded dependencies.

**How I fixed it:**
Created a `.gitignore` file with `venv/` and `.env` listed, then removed 
`venv/` from Git's tracking without deleting it from disk:

```bash
git rm -r --cached venv/
git add .gitignore
git commit -m "chore: add .gitignore and untrack venv"
```



## Problem 2

**What was wrong:**
`.env` was committed to the repository.

**Why it is a problem:**
`.env` contains values that are personal to the environment running the app. 
Later in a project it will contain sensitive values like API keys and passwords. 
Committing it to a repository - especially a public one - exposes those values 
to anyone who can see the repo. It also means every developer's local config 
ends up in source control, which causes unnecessary conflicts.

**How I fixed it:**
Removed `.env` from Git's tracking and ensured it was listed in `.gitignore`:

```bash
git rm --cached .env
git commit -m "chore: untrack .env"
```



## Problem 3

**What was wrong:**
`.env` contained a `SECRET_KEY` value that the app never reads.

**Why it is a problem:**
Config files should only contain values the app actually uses. An unused key 
with a real-looking value is misleading - it suggests the app depends on it 
when it does not. It also creates a false sense that sensitive values are being 
handled correctly when they are just sitting in a file for no reason.

**How I fixed it:**
Removed `SECRET_KEY` from `.env`. The file should only contain `PORT`, 
`DEBUG`, and `ENVIRONMENT`.



## Problem 4

**What was wrong:**
`requirements.txt` was missing `python-dotenv`. The app imports from `dotenv` 
but it was not recorded as a dependency.

**Why it is a problem:**
Anyone installing from `requirements.txt` on a fresh machine will get a 
`ModuleNotFoundError` when they try to run the app. The dependency was 
installed locally but never recorded, so the snapshot is incomplete.

**How I fixed it:**
Installed `python-dotenv` if not already present, then regenerated 
`requirements.txt`:

```bash
pip install python-dotenv
pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: add missing python-dotenv to requirements.txt"
```



## Problem 5

**What was wrong:**
`ENVIRONMENT` was not set in `.env`. The app reads it with 
`os.environ.get("ENVIRONMENT")` but with no fallback value and no entry 
in `.env`, it returns `None`. The health check endpoint reports 
`"environment": null`.

**Why it is a problem:**
The health check is meant to confirm the app knows where it is running. 
Returning `null` means it does not. In later lessons this endpoint is used 
to verify a deployment is reading the correct configuration - a `null` value 
there would be indistinguishable from a misconfigured deployment.

**How I fixed it:**
Added `ENVIRONMENT=dev` to `.env` and added `ENVIRONMENT=` to `.env.example` 
so future developers know the key is required.



## Problem 6

**What was wrong:**
`app.run()` at the bottom of `app.py` had `port` and `debug` hardcoded:

```python
if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

The `debug` variable was read from the environment correctly earlier in the 
file but never used. The `port` variable was never read from the environment 
at all.

**Why it is a problem:**
Debug mode is always on regardless of what `.env` says, which is a security 
risk in production. The port is always 5000 regardless of the environment. 
The whole point of reading config from the environment is that the same code 
behaves correctly in different contexts - hardcoding these values defeats that 
entirely.

**How I fixed it:**
Added the missing `port` variable and updated `app.run()` to use both 
variables:

```python
port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(port=port, debug=debug)
```

## Reflection

After fixing all six problems, answer the following:

- Which problem was hardest to spot and why?
- Which fix was least obvious to you before reading the lesson?
- If you cloned this repo six months from now with no memory of this task, would the README give you everything you need to get it running?