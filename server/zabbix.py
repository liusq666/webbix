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

class HOST_GRAPH(Resource):
    # 主机对应的监控图表
    def get(self, hostid):
        host_graph = zabbix_server.graph.get(output="extend", hostids=hostid, sortfield="name")
        return host_graph, 200


class GRAPH_OF_ITEM(Resource):
    def get(self, graphid):
        graph_item = zabbix_server.item.get(ouput="extend", graphids=graphid, sortfield="name")
        return graph_item, 200


class ITEM_DATA(Resource):
    def get(self, itemid):
        item_data = zabbix_server.history.get(
            output="extend", history=3, itemids=itemid, sortfield="clock", sortorder="DESC", limit=10
        )
        return item_data, 200





api.add_resource(ALL_HOST, '/ah')
api.add_resource(HOST_GRAPH, '/host_graph/<hostid>')
api.add_resource(GRAPH_OF_ITEM, '/graph_item/<graphid>')
api.add_resource(ITEM_DATA, '/item/<itemid>')




if __name__ == '__main__':
    weapp.run(debug=True)
