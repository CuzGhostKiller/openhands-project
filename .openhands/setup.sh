#!/usr/bin/env bash
set -e

# Use OpenHands' existing GitHub token.
# The token itself is never written into Git configuration.
git config --global credential.helper \
  '!f() {
      if [ "$1" = get ]; then
          echo username=x-access-token
          echo "password=${GITHUB_TOKEN:-${github_token:-}}"
      fi
  }; f'

echo "OpenHands GitHub credential helper configured."
