#!/bin/bash

echo "🔑 1Password SSH設定テスト"
echo "=========================="

# SSH_AUTH_SOCKの確認
echo "1. SSH Agent接続確認:"
if [ -n "$SSH_AUTH_SOCK" ]; then
    echo "   ✅ SSH_AUTH_SOCK: $SSH_AUTH_SOCK"
    if [ -S "$SSH_AUTH_SOCK" ]; then
        echo "   ✅ SSH agentソケットが存在します"
    else
        echo "   ❌ SSH agentソケットが見つかりません"
        exit 1
    fi
else
    echo "   ❌ SSH_AUTH_SOCKが設定されていません"
    exit 1
fi

# SSH鍵の一覧表示
echo ""
echo "2. 利用可能なSSH鍵:"
ssh-add -l
if [ $? -eq 0 ]; then
    echo "   ✅ SSH鍵が見つかりました"
else
    echo "   ❌ SSH鍵が見つかりません"
    exit 1
fi

# Git設定確認
echo ""
echo "3. Git設定確認:"
echo "   ユーザー名: $(git config user.name)"
echo "   メールアドレス: $(git config user.email)"
echo "   署名鍵: $(git config user.signingkey)"
echo "   コミット署名: $(git config commit.gpgsign)"

# GitHub接続テスト
echo ""
echo "4. GitHub接続テスト:"
ssh -T git@github.com -o ConnectTimeout=10 2>&1 | head -1
if [ ${PIPESTATUS[0]} -eq 1 ]; then
    echo "   ✅ GitHub SSH接続成功"
else
    echo "   ❌ GitHub SSH接続失敗"
fi

echo ""
echo "🎉 SSH設定テスト完了！"
