SOURCE OF TRUTH
Git repo (your JSON token files)
    ↓ on merge to main

BUILD
Style Dictionary
transforms JSON → CSS, SCSS, JS, TS, Tailwind, Figma
    ↓

PACKAGE
@solidigm/brand-tokens
bundles all the dist files
    ↓

REGISTRY (where npm lives)
GitHub Packages
stores and serves the versioned package
    ↓

CONSUMPTION
Engineer runs: npm install @solidigm/brand-tokens
imports tokens into their project
    ↓

ENFORCEMENT
ESLint plugin flags hardcoded values
GitHub Action fails CI if tokens aren't used