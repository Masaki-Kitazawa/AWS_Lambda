## KickTranscribeWav2Txt

S3バケットに生成された音声ファイル(wav)をテキスト化するためのTranscribeジョブを生成する。

トリガーにS3トリガーを設定。

Transcribeが有効なリージョンでのみ使用可。


### 環境変数

|変数名|値|例|
|---|---|---|
|URL_BASE|S3バケットのURL|https://s3-ap-southeast-2.amazonaws.com/hogehoge/|
|REGION_NAME|リージョン名|ap-southeast-2|
|ACCESS_KEY_ID|アクセスキー|hogehoge|
|SECRET_ACCESS_KEY|シークレットキー|hogehoge|

