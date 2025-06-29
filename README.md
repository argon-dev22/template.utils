# プロジェクト名

汎用テンプレートとして使用できるリポジトリ。

## 環境変数

|名前|説明|必須|
|---|---|---|
|`EXAMPLE_VARIABLE`|Environmental Varialbe Example|〇|

## クイックスタート

### 前提

- [Dev Container](https://containers.dev/)の CLI まはた VSCode 拡張機能のいづれかをインストールしていること。

### 1. リポジトリをクローンする

```bash
git clone <repo-url> <project-name>
```

### 2. 開発用コンテナ（Dev Container）の起動

```bash
devcontainer up --workspace-folder ./<project-name> # または VSCodeのGUIから起動
```

### 3. アプリケーション用コンテナの起動

```bash
docker compose up
```
