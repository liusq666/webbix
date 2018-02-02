from flask import Flask
from flask_restful import Api, Resource
from pyzabbix import ZabbixAPI
import configparser
import os

conf = configparser.ConfigParser()
conf.read('config.conf')


# 配置添加到这个字典
confd = {}
for za in conf.options("zabbix_server"):
    confd[za] = conf.get("zabbix_server", za)

weapp = Flask(__name__)
api = Api(weapp)

# 连接zabbix服务器
zabbix_server = ZabbixAPI(server=confd['zabbix_host'])
zabbix_server.login(user=confd['zabbix_user'], password=confd['zabbix_passwd'])


class ALL_HOST(Resource):
    def get(self):
        # 获取所有主机名和主机Id
        host_id_name = {}
        hosts_info = zabbix_server.host.get()
        for i in hosts_info:
            host_id_name[i['hostid']] = i['host']
        return host_id_name, 200


class HOST_ITEMS(Resource):
    def get(self, hostid):
        # 获取主机的监控项id和名称
        item_id_name = {}
        items_data = zabbix_server.item.get(
            hostids=hostid, output=["itemids","name", "key_"], sortfield="name")
        for item in items_data:
            item_id_name[item['itemid']] = [item['name'], item['key_']]
        return {"items": item_id_name}, 200


class ITEM_DATA(Resource):
    def get(self, itemid):
        item_data = zabbix_server.history.get(
            output="extend", history=3, itemids=itemid, sortfield="clock", sortorder="DESC", limit=10
        )
        return item_data, 200


api.add_resource(ALL_HOST, '/ah')
api.add_resource(HOST_ITEMS, '/host/<hostid>')
api.add_resource(ITEM_DATA, '/item/<int:itemid>')




if __name__ == '__main__':
    weapp.run(debug=True)
