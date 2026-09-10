# Pre-publication check

Run before the first push to any new public remote, and again before any push that follows
a git-history rewrite. Not a substitute for judgment — a floor, so the same class of problem
doesn't need to be rediscovered from scratch each time.

Origin: the checklist actually run before this repository's first push (`reports/06-live.md`),
after `docs/outreach-emails.md` was found to name a real individual alongside internal
negotiating strategy about him, immediately before that first push.

## 1. Full tracked-file inventory

```
git ls-files
```

Skim the complete list, not a sample. A stranger reading every path and every file should not
learn anything this project doesn't intend to publish. Group by directory to make this
tractable (`archive/`, `store/`, `scratch/`, `docs/`, `collect/`, etc.) rather than reading
253 lines in file order.

## 2. Named individuals

Grep for personal-name patterns and correspondence markers across every tracked file outside
`archive/`/`store/`/`scratch/` (those hold third-party page content and raw evidence, where
provider and platform names are expected and in scope):

```
git ls-files | grep '\.md$' | xargs grep -in 'Dear \|Hi [A-Z][a-z]\+,\|regards\|Cheers,'
```

A real person's name is fine when it is a **published citation** — a report author, a footnote,
a named role in a public document already cited elsewhere in the project (e.g. `CLAIMS.md`
citing a review's own footnote for which company ran a programme). It is not fine when it is
this project's own internal correspondence, a contact's personal negotiating position, or
anything written about a specific person that they would not expect a stranger to read.

## 3. Internal strategy content

Grep for negotiation/strategy-flavoured language:

```
git ls-files | grep '\.md$' | xargs grep -iln 'negotiat\|leverage\|strategy\|ask him\|ask her\|privately\|off.the.record\|confidential'
```

Read every hit in context. A claim like "the review found the programme unsustainable" is a
research finding with a citation — fine. Notes on what a specific contact would likely accept,
what to avoid offering them, or what leverage to use in approaching them — not fine, regardless
of how useful it is to the maintainer. That content has a place; it is not this repository.

## 4. Credentials and tokens

```
git ls-files -z | xargs -0 grep -ilE 'authorization|api[_-]?key|secret|bearer|password'
```

Every hit needs its actual context read, not just counted — most will be false positives
(a CORS header listing `authorization` as an allowed header name, a provider's own public
client-side analytics key embedded in a page this project archived, "password" inside a login
form's UI copy). None of those are this project's credentials. What would be a real finding:
this project's own API key, token, or account identifier committed anywhere — which should
never exist in the first place per `CLAUDE.md` §1.4.

## 5. Absolute local paths

```
git ls-files -z | xargs -0 grep -l '/Users/\|/home/'
```

Committed code should not carry one maintainer's machine-specific path. Fix in code (relative
path, or an environment variable with a documented default) — not in `reports/`, which are a
historical record of what was actually run and are never rewritten to look tidier in hindsight.

## 6. Unrelated data

Confirm nothing outside this project's own scope is tracked — most concretely, that no path
under the maintainer's `.gitignore`'d personal research data (`hm-ds/`, or anything added to
that ignore block later) appears in `git ls-files`. If it does, treat it exactly like a named
individual or strategy-content finding: it must be removed and rewritten out of history before
any push, not just deleted going forward — see §7.

## 7. If something has to come out of history

If nothing has been pushed yet, this is cheap to fix correctly. Do not just delete the file in
a new commit and leave it recoverable from an earlier one.

1. Preserve the file's full content somewhere outside the repository tree first, and confirm
   the copy is byte-identical before removing anything.
2. Remove the file from the working tree and commit that removal.
3. Rewrite it out of history with `git-filter-repo` (`git filter-repo --path <path>
   --invert-paths`). Do not reach for `git filter-branch` — it is slower, easier to get wrong,
   and upstream itself now points people at `filter-repo`. If `git-filter-repo` isn't
   available and can't be installed, stop and say so rather than improvising.
4. Verify, checking exit codes rather than just eyeballing the output:
   ```
   git log --all --oneline -- <path>       # must be empty, exit 0
   git rev-list --objects --all | grep -i <keyword>   # must be empty, exit 1
   ```
5. Add the path (or its containing directory) to `.gitignore` so it can't be re-added by
   accident.

If anything has already been pushed, filter-repo still works locally but the history rewrite
also has to be force-pushed and every existing clone is now stale — a materially bigger
problem. That is a reason to run this checklist before the first push, not after.

## 8. Push target

Confirm the remote URL matches what was actually intended — org/user, repository name,
visibility (public vs. private) — before pushing, not after.

```
git remote -v
```

## Then, and only then

Push. Watch the first CI run. Fix what breaks.
