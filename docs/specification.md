

# 渔夫量化策略规范

## 简介

渔夫量化策略规范旨在建立一套标准的数字货币量化交易策略描述文档规范，使任何符合该规范的策略均可接入渔夫量化交易系统。策略描述文档格式当前仅支持 JSON，后续将支持 YAML。

## 版本

该规范目前处于 draft 状态，仅在渔夫量化交易系统内部使用，并可能根据实际情况引入不兼容改善。

## 内容

### 顶层属性

**策略描述文档**是一个 JSON 对象，该对象有以下**顶层属性**：

## 顶级属性

| 属性名               | 说明                          |
| -------------------- | ----------------------------- |
| version              |                               |
| specificationVersion | 规格版本，当前最新版本为 v1.0 |
| desription           | 描述信息                      |
| parameters           | 策略参数对象                  |

## 策略参数列表

**策略参数列表**是一个 JSON 列表，列表的每一项均为**策略参数对象**。

## 策略参数对象

**策略参数对象**描述了策略的某项参数，它有以下属性：

| 属性名      | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| code        | 参数编码                                                     |
| name        | 用于显示的名称                                               |
| type        | 参数类型，支持 integer、float、decimal、enum、string         |
| description | 参数说明信息。                                               |
| default     | 参数默认值                                                   |
| editable    | 是否允许修改此参数                                           |
| items       | 一个 JSON 列表，列表每一项均为一个**参数枚举对象**。当参数类型为 enum 时必须，其余类型忽略。 |
| group       | 参数所属的组                                                 |

### 参数枚举对象

**参数枚举对象**描述了参数为 enum 类型时每项的枚举信息，它有以下属性：

| 属性名  |      | 说明   |
| ------- | ---- | ------ |
| value   |      | 存储值 |
| display |      | 展示值 |

## 示例

```json
{
   "version":"v0",
   "specicationVersion":"v1.0",
   "description":"",
   "parameters":[
      {
         "code":"entry_price",
         "name":"入场价格",
         "type":"float",
         "description":"",
         "default":null,
         "editable":true
      },
      {
         "code":"exit_price",
         "name":"出场价格",
         "type":"float",
         "description":"",
         "default":null,
         "editable":true
      },
      {
         "code":"direction",
         "name":"方向",
         "type":"enum",
         "description":"入场方向。如果是现货，做空表示先卖出资产再低价买回。",
         "default":null,
         "editable":true,
         "items":[
            {
                "value":1,
                "display":"做多"
            },
            {
                "value":-1,
                "display":"做空"
            }
         ]
      },
      {
         "code":"amount",
         "name":"数量",
         "type":"float",
         "description":"订单数量，必须 >0",
         "default":null,
         "editable":true
      }
   ]
}
```

