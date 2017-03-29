#!/usr/bin/env bash

mongodump
#导出 mongo 数据

#删除 dump 目录下的 admin 目录

mongorestore
#导入 mongo 数据


#.tar 
#解包：tar xvf dump.tar
#打包：tar cvf dump.tar dump
#（注：tar是打包，不是压缩！）


#将本地文件远程传入到远程主机
scp mongodb.tar root@{host}:/root

将远程主机传入到本地文件远程
scp {user}@{host}:{tar_path} {local_path}

# 备份数据库实例
    mongodump -h 127.0.0.1:27017 -d dbname -o {path}

    # 备份指定数据库实例的集合
    mongodump --collection mycol --db dbname -o {path}

######### 导入重置指定的数据 ####

mongodump -d {db} -o {db_path}
scp {user}@{host}:{db_path} ~
mongorestore -d {db} --dir={db_path}