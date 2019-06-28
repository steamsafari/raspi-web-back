# raspi-web-back
树莓派支持计算机视觉

通过计算机视觉控制LEGO（WeDo2.0）

# 文件

目录storage用户保存用户执行操作后形成文件。

# 运行

## 启动redis服务
```
redis-server
```

## 启动应用
```
npm run pm2
```

## 查看应用日志
```
pm2 logs
```

## 关闭应用
```
pm2 delete raspi-web
```

# python

需要安装gattlib
```
pip3 install gattlib
```

# 参考
[PM2 Runtime | Quick Start](https://pm2.io/doc/en/runtime/quick-start/)