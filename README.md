# プロジェクト名

汎用テンプレートとして使用できるリポジトリ。

## 環境変数

|名前|説明|必須|
|---|---|---|
|`EXAMPLE_VARIABLE`|Environmental Variable Example|〇|

## クイックスタート

## 前提条件

- [Dev Containers](https://containers.dev/)の拡張昨日をインストールしていること

## セットアップ例（macOS/Linux環境）

### 1. リポジトリをクローンする

```bash
git clone <repo-url> <project-name>
cd <project-name>
```

### 2. プロジェクトを初期化する

```bash
bash ./bin/setup-container.sh
# または
zsh ./bin/setup-container.sh
```

### 3. Dev Containersを起動する

1. VSCodeで「^P」を押してコマンドパレットを開く

2. 検索窓に「> `Dev Containers: Open Folder in Container`」と入力する

3. 表示された候補を選択して実行（Dev Containers起動）

以降の手順はDev Containers内で行う。

### 3. 開発環境でアプリケーションを起動する

```bash
docker compose up
```

### 4. アプリケーションにアクセスする

ブラウザで以下のURLにアクセス:
- **アプリケーション**: http://localhost:3000
