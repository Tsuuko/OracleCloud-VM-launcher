import oci
import sys
import requests
from configparser import ConfigParser
from datetime import datetime

config_l=ConfigParser()
config_l.read("config.ini",encoding='utf-8')

# Set up config
config = oci.config.from_file("config.ini","DEFAULT")
# Create a service client
identity = oci.identity.IdentityClient(config)
# ComputeClient
cclient=oci.core.ComputeClient(config)
# めっちゃ要求されるcompartment_id
compartment_id=config["tenancy"]

# 起動しているインスタンスが1つ以上あったら終了
if len([i.lifecycle_state for i in cclient.list_instances(compartment_id).data if i.lifecycle_state!="TERMINATED"])>=1:
    sys.exit()

# 可用性ドメインの設定
if len(identity.list_availability_domains(compartment_id).data)>=1:
    availability_domain=identity.list_availability_domains(compartment_id).data[0].name
    # シェイプの設定
    if len(cclient.list_shapes(compartment_id).data)>=1:
        shape=cclient.list_shapes(compartment_id).data[0].shape

        # VNICの設定（これいる？？）
        vinc_details=oci.core.models.CreateVnicDetails(
            assign_public_ip=True,
            subnet_id=config_l["LAUNCHER"]["subnet_id"]
        )

        # 立ち上げ設定
        launch_details=oci.core.models.LaunchInstanceDetails(
            availability_domain=availability_domain,
            compartment_id=compartment_id,
            shape=shape,
            display_name=config_l["LAUNCHER"]["display_name"],
            image_id=config_l["LAUNCHER"]["image_id"],
            subnet_id=vinc_details.subnet_id,
            extended_metadata={
                "ssh_authorized_keys":config_l["LAUNCHER"]["ssh_authorized_keys"]
            }
        )

        # 立ち上げる
        try:
            launch_result=cclient.launch_instance(launch_details)

        # 立ち上げに失敗した場合
        except oci.exceptions.ServiceError as e:
            print(e.message)

            # discordに日時+エラーメッセージを送信 (だいたいOut of host capacity.)
            webhook_data={
                "content":datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" : "+e.message
            }
            requests.post(config_l["LAUNCHER"]["webhook_url"],data=webhook_data)

            # 終了
            sys.exit()

        # 立ち上げに成功した場合
        else:
            # discordに日時+立ち上げ成功通知を送信
            webhook_data={
                "content":datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" : "+"立ち上げ成功"
            }
            requests.post(config_l["LAUNCHER"]["webhook_url"],data=webhook_data)

            # discordにログを送信 (.get_instance()したときと同じ内容が出力されるっぽい)
            webhook_data={
                "content":str(launch_result.data)
            }
            requests.post(config_l["LAUNCHER"]["webhook_url"],data=webhook_data)

            # ./launch_result.logにログを出力
            with open("launch_result.log","w",encoding="utf8") as f:
                f.write(str(launch_result.data))

