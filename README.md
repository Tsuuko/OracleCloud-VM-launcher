# OracleCloud-VM-launcher

## なにこれ

OracleCloudのVMを作成するスクリプト

OracleCloudのリージョンをJapan Eastにしたら全然インスタンスが立てられなかったのでつくりました。

![かなしい](https://i.imgur.com/rxdvZbM.png)

↑かなしい

毎日やっても立てられなかったのに、定期試行したら2時間程度で作れました。（運次第）

意図しない課金を防ぐため、無料アカウントでの実行をおすすめします。

いかなる事があっても責任は負えません。

プログラムは自由に修正して構いません。

## 設定

config.iniに各種設定を書きます。

### DEFAULT

[DEFAULT]セクションについてはOracle Cloud公式ブログを参考にしてください。

[Oracle Cloud 公式ブログ: Oracle Cloud Infrastructure... | Oracle Community](https://community.oracle.com/groups/oracle-cloud-japan-blog/blog/2019/02/21/oci%E3%82%AF%E3%82%A4%E3%83%83%E3%82%AF%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%88-python-sdk%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%8B)

### LAUNCHER

[LAUNCHER]セクションには立ち上げるVMの設定を記述します。

```ini
[LAUNCHER]
# discordのwebhookURL
webhook_url=
# これのサブネットのOCID
subnet_id=
# イメージID
image_id=
# インスタンス名
display_name=
# ssh認証鍵（public key）
ssh_authorized_keys=
```

#### webhook_url

Discordのチャンネル設定から作成したWebhookURLを指定してください。

#### subnet_id

ここ（ https://console.us-phoenix-1.oraclecloud.com/networking/vcns ）で"ネットワーキングQuickstart"から適当に進めてサブネットのOCID取得し、指定してください。

既に存在する場合は使って大丈夫だと思います。

#### image_id

インストールするOSのOCIDを指定してください。

多分ここのやつが使えます。
https://docs.cloud.oracle.com/iaas/images/

#### display_name

インスタンス名。お好きにどうぞ。

#### ssh_authorized_keys

SSHキーを指定してください。

キーの生成は適当に調べてください。

## つかいかた

pipenvを使用しているため、pipenvがインストールされた環境では`pipenv install`で環境が整います。

pipenvを使用しない場合は以下のコマンドを実行してパッケージをインストールしてください。

```
pip install oci requests
```

1回の実行で1回試行されるので、cron等で定期実行してください。

インスタンスが既に1つ以上立ち上がっている場合は試行されません。

2つ立てる場合はこの部分の末尾の`>=1:`を`>=2:`に変えてください。
```python
# 起動しているインスタンスが1つ以上あったら終了
if len([i.lifecycle_state for i in cclient.list_instances(compartment_id).data if i.lifecycle_state!="TERMINATED"])>=1:
```

```cron
*/5 * * * * cd /home/ubuntu/OracleCloud-launcher; /home/ubuntu/.local/bin/pipenv run python oc-vm-launcher.py
```

↑これはうちの環境です。この場合5分に1回試行します。

ユーザー名等は自身の環境に合わせてください。

## キャプチャ

こんな感じに通知が来ます。チャンネルミュート推奨。(メッセージ少しかえました)

下にVMの詳細が続きます。

![通知](https://i.imgur.com/FMPGH3t.png)
