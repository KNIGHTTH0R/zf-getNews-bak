# 1.Readme 书写流程

## 标题：名字


> data：时间



## 版本V1：（若有则写，无则跳过）

1. bug描述，修改情况等
2. ....

## 描述
对你实现的功能进行概述



## 实现原理：
1. 地址：
2. 条件：
3. 环境：
4. ...



## 目录：
对你所上传的文件及文件夹进行说明



## 注意事项：




# 2.接口文档

## REST API 文档最简模板，以 Passport 3 为例

Passport 3 安全验证。

## API Server

> 填写各个API服务器地址

外部： `passport.api.example.com`

内部: `passport.example-namespace.svc.cluster.local`

## 用户验证

### 取得密钥

> 填写请求方式，网址，请求数据，相应等。代码块必须标注语言并且格式化。

`POST` : `/oauth/token`

**Data**

```json
{
    "username": "user@example.com",
    "password": "secret",
    "grant_type": "password",
    "client_id": 2,
    "client_secret": "client_secret",
    "scope": "*"
}
```

> 各项数据说明

#### `username`

    用户登录邮箱

#### `passpord`

    用户密码

#### `grant_type`

    Passport 授权方式

    - 可选 `password`, `ldap`

#### `client_id`

    验证编号

#### `scope`

    访问域

**Response**

```json
{
  "token_type": "Bearer",
  "expires_in": 31535999,
  "access_token": "access_token",
  "refresh_token": "refresh_token"
}
```

#### `token_type`
    验证方式
#### `expires_in`
    有效期
#### `access_token`
    访问密钥
#### `refresh_token`
    续期密钥
