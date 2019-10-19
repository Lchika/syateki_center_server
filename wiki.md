# syateki_center_server

## 命名規則
- 基本はPEP8準拠
  - 参考：https://qiita.com/firedfly/items/00c34018581c6cec9b84

|対象|規則|備考|
|-|-|-|
|パッケージ|snake_case|アンダースコアなしを推奨|
|モジュール|snake_case|アンダースコアなしを推奨|
|クラス|PascalCase||
|例外|PascalCase||
|クラス変数|PascalCase||
|メソッド|snake_case|内部メソッドは頭にアンダースコア|
|引数|snake_case|予約語と被るときは末尾にアンダースコア|
|変数|snake_case|内部変数は頭にアンダースコア|
|定数|SNAKE_CASE||

- ただし、モジュール名のみ以下俺ルールを用いる
  - 各モジュールの系統に応じて以下接頭語をつける

|系統|接頭語|例|
|-|-|-|
|api系|a_|a_displayer|
|task系|t_|t_displayer|
|common系|c_|c_debug|