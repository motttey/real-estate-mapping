# real-estate-mapping
- 住みたい街データの可視化
- 目的: "住みたい街"がどんな街かを定量化

# 使用データ
- [SUUMO 住みたいまちランキング](https://suumo.jp/edit/sumi_machi/2018/kanto/)
- [住まいサーフィン](https://www.sumai-surfin.com/ )
- [国土交通省,平成29年地価公示 全国の地価動向](http://www.mlit.go.jp/common/001189489.pdf)

# 指標
物件名 + 地理情報 + 以下のフィールドを作成
- 物件数
- 地名毎の物件集合の凸包
- 物件の散らばり: 凸包の面積 / 物件数
- 対応する駅名からの平均距離
- 都心 (東京駅) からの平均距離

# デプロイ先
https://popular-town-visualization.firebaseapp.com/
