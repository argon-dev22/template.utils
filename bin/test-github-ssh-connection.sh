#!/bin/bash

echo "🔑 1Password SSH Configuration Test"
echo "===================================="

# Check SSH_AUTH_SOCK
echo "1. SSH Agent Connection Check:"
if [ -n "$SSH_AUTH_SOCK" ]; then
    echo "   ✅ SSH_AUTH_SOCK: $SSH_AUTH_SOCK"
    if [ -S "$SSH_AUTH_SOCK" ]; then
        echo "   ✅ SSH agent socket exists"
    else
        echo "   ❌ SSH agent socket not found"
        exit 1
    fi
else
    echo "   ❌ SSH_AUTH_SOCK is not set"
    exit 1
fi

# List available SSH keys
echo ""
echo "2. Available SSH Keys:"
ssh-add -l
if [ $? -eq 0 ]; then
    echo "   ✅ SSH keys found"
else
    echo "   ❌ No SSH keys found"
    exit 1
fi

# Check Git configuration
echo ""
echo "3. Git Configuration Check:"
echo "   Username: $(git config user.name)"
echo "   Email: $(git config user.email)"
echo "   Signing key: $(git config user.signingkey)"
echo "   Commit signing: $(git config commit.gpgsign)"

# GitHub connection test
echo ""
echo "4. GitHub Connection Test:"
ssh -T git@github.com -o ConnectTimeout=10 2>&1 | head -1
if [ ${PIPESTATUS[0]} -eq 1 ]; then
    echo "   ✅ GitHub SSH connection successful"
else
    echo "   ❌ GitHub SSH connection failed"
fi

echo ""
echo "🎉 SSH configuration test completed!"
