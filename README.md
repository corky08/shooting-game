# shooting-game
## 操作方法
- `a`：左に移動
- `d`：右に移動
- `左クリック`：射撃

## ルール
- 弾は全部で10発あり、弾がなくなるとゲームオーバー
- 的の中心に近いほど得点が高く、中心から順に50, 30, 10点
- ゲームオーバー時、Spaceキーを押すとリトライ

## ゲーム設定
### Player
- **Speed**：プレイヤーの移動速度を変更
    - slow, normal（デフォルト）, fast

### Bullet
- **Speed**：弾の速度を変更
    - slow, normal（デフォルト）, fast

### Target
- **Speed**：的の移動速度を変更
    - slow, normal（デフォルト）, fast
- **Size**：的の大きさを変更
    - small, medium（デフォルト）, big
- **Random**：一定間隔でランダムに的の移動方向が変化する。変化する直前に的の色が変化する。
    - none（デフォルト）, normal, frequent