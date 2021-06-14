import boto3
from datetime import datetime
from dateutil import tz

iam = boto3.client('iam')

# クレデンシャル情報を指定したい場合は以下のようにする
# session = boto3.Session(profile_name='famm')
# iam = session.client('iam')

print("UserName\tNumAccessKeys\tLastUsedAccessKey\tKeyLastUsedDate\tKeyLastUsedService\tURL")

res_users = iam.list_users()
for user in res_users['Users']:
        username = user['UserName']
        url = "https://console.aws.amazon.com/iam/home?region=ap-northeast-1#/users/%s" + username
        res_access_keys = iam.list_access_keys(
                UserName=username
        )
        num_access_keys = len(res_access_keys['AccessKeyMetadata'])

        max_last_used_ak = ''
        max_last_used_date = datetime(2000,1,1).replace(tzinfo=tz.tzutc())
        max_last_used_service = ''

        for ak in res_access_keys['AccessKeyMetadata']:
                access_key = ak['AccessKeyId']
                res_last_used = iam.get_access_key_last_used(
                        AccessKeyId=access_key
                )

                if res_last_used['AccessKeyLastUsed']['Region'] != 'N/A':
                        last_used_date = res_last_used['AccessKeyLastUsed']['LastUsedDate']
                        last_used_service = res_last_used['AccessKeyLastUsed']['ServiceName']
#                       print "%s : %s" % (last_used_date, max_last_used_date)
                        if last_used_date > max_last_used_date:
#                               print "FOUND LARGER LAST_USED"
                                max_last_used_ak = access_key
                                max_last_used_service = last_used_service
                                max_last_used_date = last_used_date

        print("\t".join([username, str(num_access_keys), max_last_used_ak, max_last_used_date.strftime('%Y-%m-%d %H:%M:%S'), max_last_used_service, url]))