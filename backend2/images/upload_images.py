import logging
import sys
import time
from datetime import datetime

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKIDcBSzTynfTDrOn5Qm5IS6OhF5cnwGRO7w'
secret_key = 'w6BCAA6tSRD0y7DQhtypWDtgWRnFfZPA' 
region = 'ap-guangzhou'
bucket_name = 'drinkwater-1325041233'

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)

def upload_percentage(consumed_bytes, total_bytes):
    """进度条回调函数，计算当前上传的百分比

    :param consumed_bytes: 已经上传的数据量
    :param total_bytes: 总数据量
    """
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate))
        sys.stdout.flush()


def upload(path, title):
    """上传图片逻辑，返回上传好的图片对应的图床url

    :param path: 本地图片地址
    :param title: 图片名称
    """
    # 获取当前时间
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    print(formatted_time)
    key = "db_imgs/" + formatted_time + "_" + title
    response = client.upload_file(
        Bucket=bucket_name,
        Key=key,
        LocalFilePath=path,
        PartSize=1,
        MAXThread=5,
        progress_callback=upload_percentage,
        EnableMD5=False,
        ACL='public-read',
    )
    url = client.get_object_url(
        Bucket=bucket_name,
        Key=key
    )
    return url


if __name__ == "__main__":
    url = upload("images/4.png", "pic_test.png")
    print(url)