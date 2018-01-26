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
    """
    获取所有主机名和主机Id
    """
    def get(self):
        host_id_name = {}
        hosts_info = zabbix_server.host.get()
        for i in hosts_info:
            host_id_name[i['hostid']] = i['host']
        return host_id_name, 200

class HOST_GRAPH(Resource):
    def get(self, hostid):
        # 获取主机的监控项id和名称
        gra_id_name = {}
        graph_data = zabbix_server.graph.get(hostids=hostid, output="extend", sortfield="name")
        for gra in graph_data:
            gra_id_name[gra['graphid']] = gra['name']
        return {hostid:gra_id_name}, 200


class GRAPH(Resource):
    def get(self, graphid):
        # 获取监控项数据
        graph_data = zabbix_server.graphitem.get(output="extend", graphid=graphid)
        return graph_data, 200


api.add_resource(ALL_HOST, '/ah')
api.add_resource(HOST_GRAPH, '/<hostid>')
api.add_resource(GRAPH, '/graph/<int:graphid>')


if __name__ == '__main__':
    weapp.run(debug=True)
    