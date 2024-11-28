// 定义a8原型上的send方法
a8['\x70\x72\x6f\x74\x6f\x74\x79\x70\x65']['\x73\x65\x6e\x64'] = function() {
    // 定义一些辅助函数
    var as = {
        'xnMbI': function(ay, az) {
            return q['sTXTG'](ay, az);
        },
        'eWCJP': q['fQWuo'],
        'ceCTU': 'gezAu',
        'JEWyF': function(ay, az) {
            return q['jsBHW'](ay, az);
        },
        'yYsNa': function(ay, az) {
            return q['KQuPn'](ay, az);
        },
        'LNCNJ': function(ay, az) {
            return q['gXiHw'](ay, az);
        }
    };
    // 保存传入的参数
    const at = arguments;
    // 获取请求头信息
    var au = q['QGdCO'](a5, this['__send_headers'] || this['_headers'] || {}),
        // 获取签名信息
        av = au['signature'],
        // 获取序列ID
        aw = this['_serialId'],
        // 从ah中获取序列ID对应的值
        ax = ah['get'](aw);

    // 删除序列ID
    ah['delete'](aw);

    // 如果没有ax但有签名信息,直接调用aa方法
    if (q['zque'](!ax, av)) {
        aa['apply'](this, at);
    } else {
        // 判断是否为'Zarkl'
        if (q['Qqmbw'](q['Zarkl'], q['Zarkl'])) {
            const ay = this;
            // 解构获取url、duration和method
            var { url: aw, duration: av, method: ax } = ax;
            let az;

            // 根据请求方法类型处理
            if (q['rVjOm'](q['oTNsN'], ax)) {
                // GET请求处理
                az = q['TIdHl'](a4, aw, av, null, Z['Get']);
            } else if (q['SIFIY']('POST', ax)) {
                // POST请求处理
                ax = au[q['lhRwS']] || '';
                az = q['hJexX'](a4, aw, av, at[0], ax['includes'](q['oeLMJ']) ? Z['PostJSON'] : Z['Post']);
            }

            // 如果az为空直接调用aa,否则处理Promise
            if (q['jcdjg'](null, az)) {
                aa['apply'](this, at);
            } else {
                az['then'](function(aA) {
                    // 如果aA存在,遍历其所有key并设置请求头
                    if (aA) {
                        Object['keys'](aA)['forEach'](aB => {
                            var aC = {
                                'aMwVr': function(aD, aE) {
                                    return aD !== aE;
                                },
                                'Btarl': function(aD, aE) {
                                    return aD(aE);
                                }
                            };
                            // 设置请求头
                            as['xnMbI'](as['eWCJP'], as['ceCTU']) ?
                                ay['setRequestHeader'](aB, aA[aB]) :
                                aC['aMwVr'](a5, T) && N['push']('' ['concat'](ag, '=')['concat'](aC['Btarl'](al, a1)));
                        });
                    }
                    // 最后调用aa方法
                    aa['apply'](ay, at);
                });
            }
        } else {
            // 处理参数
            for (var aB = arguments['length'],
                    aC = new X(as['JEWyF'](0x265 + 0x171d + -0x1981, aB) ? aB - 1 : 0),
                    aD = 0; as['yYsNa'](aD, aB); aD++) {
                aC[as['LNCNJ'](aD, 1)] = arguments[aD];
            }
            a3['call'](null, ...aC);
        }
    }
}