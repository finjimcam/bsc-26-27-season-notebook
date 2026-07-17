# BSC 26/27 Season Notebook

A single-page coaching notebook (sessions, philosophy, players, tactics boards,
matches, physical testing) served on GitHub Pages from `index.html`.

## How data works

Notebook content is **not** stored in the site — it lives in `data.json` on the
[`data` branch](../../tree/data) of this repo. The page reads and writes it
through the GitHub Contents API, so every device sees the same notebook. Data
is kept off `main` so saves don't trigger Pages rebuilds. Each device also
keeps a `localStorage` copy as an offline cache.

- **Viewing** — anyone who opens the site is asked for the passcode (set from
  the sync menu, bottom-right chip). This only hides the UI; the repo itself is
  public, so treat it as a "keep strangers out" latch, not encryption.
- **Editing** — requires a GitHub fine-grained personal access token with
  **Contents: Read and write** on this repo only, pasted once per device via
  the chip → *Enable editing*. The token stays in that device's localStorage.
  Without it the notebook is view-only (inputs locked, action buttons hidden).
- **Conflicts** — last write wins per save; saves are debounced ~2.5s and
  flushed when the tab is hidden. The page refetches when you return to it.

### Creating an edit token

GitHub → Settings → Developer settings → Personal access tokens →
Fine-grained tokens → Generate new token. Repository access: *Only select
repositories* → this repo. Permissions: *Contents → Read and write*. Max
expiry is 1 year — paste the new one into the site when it lapses.

## Editing the site itself

`index.html` is an exported artifact bundle; the app's markup and logic live as
a JSON string inside its `__bundler/template` block. Don't edit `index.html`
directly — edit `src/template.html`, then rebuild:

```
python tools/pack.py          # src/template.html -> index.html
python tools/pack.py unpack   # index.html -> src/template.html (recover)
```

The sync/passcode logic is the `NBSync` script in `src/template.html`; the
notebook app itself is the `text/x-dc` script at the bottom of the same file.
