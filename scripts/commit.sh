#!/bin/bash
set -e   # stop the whole script immediately if any command fails

if [ -z "$1" ]; then
    echo "Usage: sh commit.sh \"your commit message\""
    exit 1
fi

echo "Running tests..."
python -m pytest -v

echo "Running lint..."
ruff check . --fix

BRANCH=$(git branch --show-current)
echo "All checks passed. Committing to $BRANCH..."

git add -A
git commit -m "$1"
git push -u origin "$BRANCH"

echo "Done."