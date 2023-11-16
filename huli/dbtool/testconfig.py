config = {
    "id_start": "9020021112344157000",
    "id_prefix": "9020021112344157",
    "number": 1000,
    "taskName": "单实例单系统节点测试4",
    "execKey": "singleNodeTest",
    "execName": "单节点压测流程"
}

db_config = {
    "maxTotal": "10",
    "maxIdle": "-1",
    "minIdle": "5",
    "maxWaitMillis": "600000"
}

dubbo_config = {
    "dubbo.provider.connections": "0",
    "dubbo.provider.actives": "0",
    "dubbo.provider.executes": "0",
    "dubbo.provider.accepts": "0",
    "dubbo.provider.threads": "200",
    "dubbo.provider.timeout": "60000"
}
