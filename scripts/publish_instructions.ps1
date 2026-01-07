# PowerShell helper: run locally to push to GitHub
# Usage: run in project root after installing git and gh

# Initialize repo if needed
if (-not (Test-Path .git)) {
  git init
  git branch -M main
  git add -A
  git commit -m "initial commit"
}

Write-Host "Create repository on GitHub (public):"
gh repo create PaintingExhibition --public --source=. --remote=origin --push
Write-Host "Repository created and pushed to origin/main"