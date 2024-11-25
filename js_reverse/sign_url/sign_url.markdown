# 分析URL动态签名的关键js代码

原始关键代码: `Cj = C8[YM(uP.C)](C2, Cj, CK, this[YM(uP.j)][-0xb * 0x2db + -0x1 * -0x1de7 + -0xc1 * -0x2])`

## C8[YM(uP.C)]分析过程

> C8[YM(uP.C)]
> `ƒ (CK,Cj,CC,CN){var Yc=s3;return K7[Yc(us.s)](CK,Cj,CC,CN);}`
> K7[Yc(us.s)]
> `ƒ (C8,C9,Cs,CK){var d5=ND;return s[d5(EP.s)](C8,C9,Cs,CK);}`
> s[d5(EP.s)]
> `ƒ (I,D,Y,V){return I(D,Y,V);}`

结论：4个输入参数，第一个是函数，后3个是参数，把后3个参数传给第一个函数，返回值就是最终的签名

## C2函数分析过程

> C2
> `ƒ (C8,C9,Cs){return!!C1['sU'](C8)&&C1['sg'](C8,C9,Cs);}`

这段代码是URL签名验证的关键逻辑:

1. C1['sU'](C8) 是一个URL合法性检查函数
   - 首先用!!将返回值转为布尔值
   - 检查URL是否合法,不能包含特定的阿里云域名
   - 返回true表示URL合法,false表示不合法

2. C1['sg'](C8,C9,Cs) 是实际的签名生成函数
   - C8: URL对象, 示例: {
     protocol: 'https:',
     host: 'xxx.xxx.cn',
     hostname: '.xxx.cn',
     port: '',
     pathname: '/assembly/build/index.wasm',
     search: '?sid=xxxx',
     hash: '',
     sl: 'https://xxx.xxx.cn/assembly/build/index.wasm?sid=xxx'
   }
   - C9: 参数(这里是undefined)
   - Cs: 请求方法(这里是"GET")

3. &&操作符表示:
   - 只有当URL合法性检查通过时
   - 才会执行后面的签名生成函数
   - 否则直接返回false

> C1['sU']
> `ƒ (C8){var Yr=ND;return!((-0x2c*0xab+0x64e+0x49e*0x5,Ks['sb'])(C8)||C8[Yr(OZ.s)][Yr(OZ.K)](/(cloudauth-device|captcha-(pro-)?open).*?\.aliyuncs\.com$/)||!C1['su'](C8));}`
> 暂时不再进一步分析这里了，我继续聚焦分析签名生成函数C1['sg']

### C1['sg']分析过程

> C1['sg']

```js
// sg函数 - 用于生成签名
// 输入参数: C8, C9, Cs
// 输入示例：
// C8: {
//     protocol: 'https:',
//     host: 'xxx.xxx.cn',
//     hostname: '.xxx.cn',
//     ...
// }
// C9: undefined
// Cs: 'GET'
'sg': function(C8, C9, Cs) {
    var YS = ND
      , CK = K7[YS(u3.s)][YS(u3.K)]('|') // 获取分隔符'|'['0', '3', '1', '4', '2']
      , Cj = 0; // 初始化计数器
    while (!![]) { // 无限循环,直到break
        switch (CK[Cj++]) { // switch语句,根据计数器选择不同case
        case '0':
            // 处理请求方法(GET/POST等),转换为大写
            Cs = (Cs = K7[YS(u3.j)](Cs, K7[YS(u3.C)]))[YS(u3.N) + 'e']();
            continue;
        case '1':
            // 处理请求参数
            // 如果是GET或POST请求且C9为空,则清空C9
            if (K7[YS(u3.I)](-1, [K7[YS(u3.D)], K7[YS(u3.Y)]][YS(u3.V)](Cs)) && (C9 = ''),
            // URL编码CI参数
            CI = K7[YS(u3.R)](encodeURIComponent, CI),
            C9) {
                // 如果存在C9参数
                if (KC['sD'][YS(u3.L)] && K7[YS(u3.b)](C9, Uint8Array)) {
                    // 如果C9是Uint8Array类型,进行特殊处理
                    for (var CC = '', CN = 0; K7[YS(u3.n)](CN, C9[YS(u3.A)]); CN++)
                        CC += jy[C9[CN]];
                    CI += CC;
                } else
                    // 否则直接URL编码后拼接
                    CI += K7[YS(u3.P)](encodeURIComponent, C9);
            }
            continue;
        case '2':
            // 最终处理和返回
            // 1. 将CI值存储到Cs对象的特定属性中
            // 2. 计算C8的签名值
            // 3. 返回最终的签名结果
            return Cs[C1['sz'](C8[YS(u3.l)])] = CI,
            C8[YS(u3.H)] = (Ks['sn'])(C8[YS(u3.E)], Cs),
            (Ks['sA'])(C8);
        case '3':
            // 获取初始签名值
            var CI = (Ks['sA'])(C8, !0); // 获取初始签名值,传入C8对象和true参数,调用Ks对象的sA方法
            continue;
        case '4':
            // 构造签名字符串
            // 格式: CI值|时间戳|1
            Cs = K7[YS(u3.O)](K7[YS(u3.u)](K7[YS(u3.X)](K7[YS(u3.U)](K7[YS(u3.e)](C1['se'](CI), '|'), K7[YS(u3.g)](KN)), '|'), new Date()[YS(u3.z)]()), '|1'),
            // 对签名字符串进行加密
            CI = Kj['sE'](Cs, !0),
            // 初始化Cs对象
            Cs = {};
            continue;
        }
        break;
    }
}
```

#### case 1 的代码分析

> `CI = K7[YS(u3.R)](encodeURIComponent, CI),`
> 浏览器控制台输出信息：
> CI
> `https://wxsports.ydmap.cn/assembly/build/index.wasm?sid=735f92867b40463a9ed71bcedf6bd4d3`
> encodeURIComponent
> `ƒ encodeURIComponent() { [native code] }`
> `K7[YS(u3.R)]`
> `ƒ (C8,C9){var Dy=ND;return s[Dy(EI.s)](C8,C9);}`
> `s[Dy(EI.s)]`
> `ƒ (I,D){return I(D);}`

分析

- 调用`K7[YS(u3.R)]`函数, 传入`encodeURIComponent`和`CI`参数, 调用`encodeURIComponent`函数对`CI`进行URL编码
- 将编码后的结果赋值给CI

case 1代码作用：
输入参数CI：https://wxsports.ydmap.cn/assembly/build/index.wasm?sid=44813931a6894b21add5c1b400804ff3
输出参数CI：https%3A%2F%2Fwxsports.ydmap.cn%2Fassembly%2Fbuild%2Findex.wasm%3Fsid%3Dfe369c83946142bc91c63318c03d0a30

✅结果：对应python函数：`sign_url_utls.py` 中的`encode_uri_component`函数

#### case 4 的代码分析01

`Cs = K7[YS(u3.O)](K7[YS(u3.u)](K7[YS(u3.X)](K7[YS(u3.U)](K7[YS(u3.e)](C1['se'](CI), '|'), K7[YS(u3.g)](KN)), '|'), new Date()[YS(u3.z)]()), '|1')`

> `K7[YS(u3.O)]`
> `ƒ (C8,C9){var Da=ND;return s[Da(EV.s)](C8,C9);}`
> `s[Da(EV.s)]`
> `ƒ (I,D){return I+D;}`
> `K7[YS(u3.u)]`
> `ƒ (C8,C9){var d0=ND;return s[d0(ER.s)](C8,C9);}`
> `s[d0(ER.s)]`
> `ƒ (I,D){return I+D;}`
> `K7[YS(u3.X)]`
> `ƒ (C8,C9){var d1=ND;return s[d1(EL.s)](C8,C9);}`
> `s[d1(EL.s)]`
> `ƒ (I,D){return I(D);}`
> `K7[YS(u3.U)]`
> `ƒ (C8,C9){var d2=ND;return s[d2(EJ.s)](C8,C9);}`
> `s[d2(EJ.s)]`
> `ƒ (I,D){return I(D);}`
> `K7[YS(u3.e)]`
> `ƒ (C8,C9){var d3=ND;return s[d3(EJ.s)](C8,C9);}`
> `s[d3(EJ.s)]`
> `ƒ (I,D){return I(D);}`

##### C1['se']函数分析

```js
'se': function(C8) {
    var Yg = ND;
    for (var C9 = -0x717 + -0x1c73 * -0x1 + -0x4 * 0x557, Cs = 0x62f * -0x2 + -0x2391 + 0x2fef; K7[Yg(Oa.s)](Cs, C8[Yg(Oa.K)]); Cs++)
        C9 = K7[Yg(Oa.j)](K7[Yg(Oa.C)](K7[Yg(Oa.N)](K7[Yg(Oa.I)](C9, -0x4e * -0x2f + 0x8ef * -0x4 + -0x1571 * -0x1), C9), -0x7 * -0xe9 + -0x18c9 + 0x13f8), C8[Yg(Oa.D)](Cs)),
        C9 |= -0x5f3 * 0x4 + 0x2087 * -0x1 + -0x3853 * -0x1;
    return C9;
},
```

浏览器控制台输出信息：

> `K7[Yg(Oa.s)]`
> `ƒ (C8,C9){var Nb=ND;return s[Nb(PT.s)](C8,C9);}`
> `s[Nb(PT.s)]`
> `ƒ (I,D){return I<D;}`
> `C8[Yg(Oa.K)]`
> `104`
> `Yg(Oa.K)`
> `'length'`
> `K7[Yg(Oa.j)]`
> `ƒ (C8,C9){var IT=ND;return s[IT(lZ.s)](C8,C9);}`
> `s[IT(lZ.s)]`
> `ƒ (I,D){return I+D;}`
> `K7[Yg(Oa.C)]`
> `ƒ (C8,C9){var Dp=ND;return s[Dp(Ej.s)](C8,C9);}`
> `s[Dp(Ej.s)]`
> `ƒ (I,D){return I+D;}`
> `K7[Yg(Oa.N)]`
> `ƒ (C8,C9){var NW=ND;return s[NW(l3.s)](C8,C9);}`
> `s[NW(l3.s)]`
> `ƒ (I,D){return I-D;}`
> `K7[Yg(Oa.I)]`
> `ƒ (C8,C9){var DJ=ND;return s[DJ(EC.s)](C8,C9);}`
> `s[DJ(EC.s)]`
> `ƒ (I,D){return I<<D;}`
> `-0x4e * -0x2f + 0x8ef * -0x4 + -0x1571 * -0x1`
> `7`
> `-0x7 * -0xe9 + -0x18c9 + 0x13f8`
> `398`
> `C8[Yg(Oa.D)]`
> `ƒ charCodeAt() { [native code] }`

输入示例：C8 = "https%3A%2F%2Fwxsports.ydmap.cn%2Fassembly%2Fbuild%2Findex.wasm%3Fsid%3D1bb75ad9bba74371babbfad292755c7d"
输出示例：C9 = 859196381

✅结果：对应python函数：`sign_url_utls.py` 中的`compute_hash`函数

#### K7[YS(u3.g)]函数分析

> `K7[YS(u3.g)]`
> `ƒ (C8){var Dr=ND;return s[Dr(Hp.s)](C8);}`
> `s[Dr(Hp.s)]`
> `ƒ (I){return I();}`

✅结果：对应python函数：`int(time.time() * 1000)`

总结：

`Cs = K7[YS(u3.O)](K7[YS(u3.u)](K7[YS(u3.X)](K7[YS(u3.U)](K7[YS(u3.e)](C1['se'](CI), '|'), K7[YS(u3.g)](KN)), '|'), new Date()[YS(u3.z)]()), '|1')`
输入示例：CI = "https%3A%2F%2Fwxsports.ydmap.cn%2Fassembly%2Fbuild%2Findex.wasm%3Fsid%3D24622b09121843d181d6695572617cda"
输出示例：Cs = "-713518747|0|1731770954061|1"
解释：
- 第1个数字：url的hash签名值
- 第2个数字：固定0
- 第3个数字：时间戳
- 第4个数字：固定1

✅结果：case 4 的代码分析01:
输入：CI = "https://wxsports.ydmap.cn/assembly/build/index.wasm?sid=fbdda5188ad545d39a8ab610e70723ae"
输出：Cs = "-713518747|0|1731770954061|1"

#### case 4 的代码分析02

`CI = Kj['sE'](Cs, !0)`

```js
'sE': function(C8, C9) {
                var dl = ND
                  , Cs = K7[dl(EB.s)][dl(EB.K)]('|')
                  , CK = -0xdfa + 0x222d + 0x1 * -0x1433;
                while (!![]) {
                    switch (Cs[CK++]) {
                    case '0':
                        if (C9)
                            return CN;
                        continue;
                    case '1':
                        switch (K7[dl(EB.j)](CN[dl(EB.C)], 0x1 * -0x18c2 + -0x1b52 + 0x3418)) {
                        default:
                        case -0x10c9 * 0x2 + -0x1108 + 0x194d * 0x2:
                            return CN;
                        case -0x1 * 0x25fa + -0x6fb + 0x2cf6:
                            return K7[dl(EB.N)](CN, K7[dl(EB.I)]);
                        case -0x3 * -0x797 + -0x1 * -0x1d + -0x16e0:
                            return K7[dl(EB.D)](CN, '==');
                        case -0x8 * -0x382 + 0x1 * 0x1055 + 0x1a * -0x1b5:
                            return K7[dl(EB.Y)](CN, '=');
                        }
                        continue;
                    case '2':
                        var Cj = {};
                        Cj[dl(EB.V)] = K7[dl(EB.R)];
                        var CC = Cj;
                        continue;
                    case '3':
                        var CN = K8['sO'](C8, -0x206f + 0xa * 0x32b + 0xc7, function(CI) {
                            var dH = dl;
                            return CC[dH(EW.s)][dH(EW.K)](CI);
                        });
                        continue;
                    case '4':
                        if (K7[dl(EB.L)](null, C8))
                            return '';
                        continue;
                    }
                    break;
                }
            },
},
```

case顺序：
Cs = ['2', '4', '3', '0', '1']
主要分析2、4、3，在0的时候直接返回CN, 因为C9是True

##### case 2 的代码分析

```js
var Cj = {};
Cj[dl(EB.V)] = K7[dl(EB.R)];
var CC = Cj;
```

这里的逻辑是获取秘钥: CC = "DGi0YA7BemWnQjCl4+bR3f8SKIF9tUz/xhr2oEOgPpac=61ZqwTudLkM5vHyNXsVJ"

##### case 3 的代码分析(啥也没干，忽略)

##### case 4 的代码分析

```js
// 这里是对输入字符串C8进行处理
// K8['sO']是一个处理函数,接收3个参数:
// 1. C8: 输入字符串
// 2. -0x206f + 0xa * 0x32b + 0xc7: 计算得到一个数值,作为步长
// 3. 回调函数,对每个字符进行处理:
//    - 使用CC中存储的秘钥字符串
//    - 通过dH(EW.s)和dH(EW.K)获取处理方法
//    - 对每个字符CI进行转换
CI = K8['sO'](C8, -0x206f + 0xa * 0x32b + 0xc7, function(CI) {
    var dH = dl;
    return CC[dH(EW.s)][dH(EW.K)](CI);
});
```

K8['sO']函数分析和还原的prompt：

```js
// 第一次prompt：
// 【已知条件】通过浏览器的控制器断点的方式，已知下列的多个dE和K7相关的函数定义：
dE(Ex.s) =  SjfXJ
dE(Ex.K) =  lLdZH
dE(Ex.j) =  length
dE(Ex.C) =  charAt
dE(Ex.N) =  prototype
dE(Ex.I) =  hasOwnProp
dE(Ex.D) =  erty
dE(Ex.Y) =  call
dE(Ex.V) =  BUEle
dE(Ex.R) =  hasOwnProp
dE(Ex.L) =  erty
dE(Ex.b) =  call
dE(Ex.n) =  prototype
dE(Ex.A) =  erty
dE(Ex.P) =  charCodeAt
dE(Ex.l) =  IDfPN
dE(Ex.H) =  pjjrR
dE(Ex.E) =  push
dE(Ex.O) =  IIwPd
dE(Ex.u) =  charCodeAt
dE(Ex.X) =  riKRs
dE(Ex.U) =  PFwIT
dE(Ex.e) =  fEwFm
dE(Ex.g) =  ElrQl
dE(Ex.z) =  lzmBf
dE(Ex.f) =  zGiFk
dE(Ex.S) =  push
dE(Ex.h) =  IIwPd
dE(Ex.F) =  DOyMq
dE(Ex.T) =  PFwIT
dE(Ex.t) =  fEwFm
dE(Ex.m) =  lzmBf
dE(Ex.c) =  KTmNC
dE(Ex.w) =  wYIVx
dE(Ex.W) =  DOyMq
dE(Ex.B) =  fEwFm
dE(Ex.x) =  qOGSu
dE(Ex.k) =  QdsOy
dE(Ex.q) =  ZSdGE
dE(Ex.i) =  qOGSu
dE(Ex.Q) =  pow
dE(Ex.v) =  riKRs
dE(Ex.p) =  fEwFm
dE(Ex.J) =  uuRxm
dE(Ex.G) =  push
dE(Ex.y) =  wYIVx
dE(Ex.M) =  TxwGH
dE(Ex.Z) =  erty
dE(Ex.a) =  nqMwU
dE(Ex.s0) =  CVIxk
dE(Ex.s1) =  bFoqp
dE(Ex.K2) =  RLBUU
dE(Ex.K3) =  wYIVx
dE(Ex.K4) =  OYbki
dE(Ex.K5) =  PFwIT
dE(Ex.K6) =  fEwFm
dE(Ex.K7) =  BwkQJ
dE(Ex.K8) =  qNMxS
dE(Ex.K9) =  YzDFx
dE(Ex.Ks) =  NjUYW
dE(Ex.KK) =  fEwFm
dE(Ex.Kj) =  rEAqP
dE(Ex.KC) =  VhaVZ
dE(Ex.KN) =  IIwPd
dE(Ex.KI) =  dHfGD
dE(Ex.KD) =  pEMmR
dE(Ex.Kd) =  fEwFm
dE(Ex.KY) =  DyNCO
dE(Ex.KV) =  RLBUU
dE(Ex.KR) =  IIwPd
dE(Ex.KL) =  bFoqp
dE(Ex.Kb) =  pow
dE(Ex.Kn) =  NjUYW
dE(Ex.KA) =  ercgf
dE(Ex.KP) =  ElrQl
dE(Ex.Kl) =  Aqrxt
dE(Ex.KH) =  sdhJj
dE(Ex.KE) =  push
dE(Ex.KO) =  qERUm
dE(Ex.Ku) =  qOGSu
dE(Ex.KX) =  pow
dE(Ex.KU) =  IMjWu
dE(Ex.Ke) =  mhaVB
dE(Ex.Kr) =  abmNA
dE(Ex.Kg) =  NzFED
dE(Ex.Kz) =  FAfic
dE(Ex.Kf) =  push
dE(Ex.KS) =  KTmNC
dE(Ex.Kh) =  IOYyt
dE(Ex.KF) =  join

K7['SjfXJ']
ƒ (C8,C9){var NL=ND;return s[NL(PF.s)](C8,C9);}
s[NL(PF.s)]
ƒ (I,D){return I==D;}


K7['lLdZH']
ƒ (C8,C9){var Nb=ND;return s[Nb(PT.s)](C8,C9);}
s[Nb(PT.s)]
ƒ (I,D){return I<D;}


K7['BUEle']
ƒ (C8,C9){var Nn=ND;return s[Nn(Pt.s)](C8,C9);}
s[Nb(PT.s)]
ƒ (I,D){return I<D;}


K7['IDfPN']
ƒ (C8,C9){var NA=ND;return s[NA(Pm.s)](C8,C9);}
s[NA(Pm.s)]
ƒ (I,D){return I<D;}


K7['SjfXJ']
ƒ (C8,C9){var NL=ND;return s[NL(PF.s)](C8,C9);}
s[NL(PF.s)]
ƒ (I,D){return I==D;}


K7['pjjrR']
ƒ (C8,C9){var NP=ND;return s[NP(Pc.s)](C8,C9);}
s[NP(Pc.s)]
ƒ (I,D){return I-D;}


K7['IIwPd']
ƒ (C8,C9){var Nl=ND;return s[Nl(Pw.s)](C8,C9);}
s[Nl(Pw.s)]
ƒ (I,D){return I(D);}


K7['riKRs']
ƒ (C8,C9){var NH=ND;return s[NH(PW.s)](C8,C9);}
s[NH(PW.s)]
ƒ (I,D){return I<D;}


K7['PFwIT']
ƒ (C8,C9){var NE=ND;return s[NE(PB.s)](C8,C9);}
s[NE(PB.s)]
ƒ (I,D){return I|D;}


K7['fEwFm']
ƒ (C8,C9){var NO=ND;return s[NO(Px.s)](C8,C9);}
s[NO(Px.s)]
ƒ (I,D){return I<<D;}


K7['ElrQl']
ƒ (C8,C9){var Nu=ND;return s[Nu(Pk.s)](C8,C9);}
s[Nu(Pk.s)]
ƒ (I,D){return I&D;}


K7['lzmBf']
ƒ (C8,C9){var NX=ND;return s[NX(Pq.s)](C8,C9);}
s[NX(Pq.s)]
ƒ (I,D){return I==D;}


K7['zGiFk']
ƒ (C8,C9){var NU=ND;return s[NU(Pi.s)](C8,C9);}
s[NU(Pi.s)]
ƒ (I,D){return I-D;}


K7['IIwPd']
ƒ (C8,C9){var Nl=ND;return s[Nl(Pw.s)](C8,C9);}
s[Nl(Pw.s)]
ƒ (I,D){return I(D);}


K7['qOGSu']
ƒ (C8,C9){var Nz=ND;return s[Nz(PJ.s)](C8,C9);}
s[Nz(PJ.s)]
ƒ (I,D){return I==D;}


K7['riKRs']
ƒ (C8,C9){var NH=ND;return s[NH(PW.s)](C8,C9);}
s[NH(PW.s)]
ƒ (I,D){return I<D;}


K7['PFwIT']
ƒ (C8,C9){var NE=ND;return s[NE(PB.s)](C8,C9);}
s[NE(PB.s)]
ƒ (I,D){return I|D;}


K7['uuRxm']
ƒ (C8,C9){var Nh=ND;return s[Nh(Po.s)](C8,C9);}
s[Nh(Po.s)]
ƒ (I,D){return I==D;}


K7['KTmNC']
ƒ (C8,C9){var Nr=ND;return s[Nr(Pv.s)](C8,C9);}
s[Nr(Pv.s)]
ƒ (I,D){return I-D;}


K7['wYIVx']
ƒ (C8,C9){var Ng=ND;return s[Ng(Pp.s)](C8,C9);}
s[Ng(Pp.s)]
ƒ (I,D){return I(D);}


K7['TxwGH']
ƒ (C8,C9){var NF=ND;return s[NF(PM.s)](C8,C9);}
s[NF(PM.s)]
ƒ (I,D){return I!==D;}


K7['riKRs']
ƒ (C8,C9){var NH=ND;return s[NH(PW.s)](C8,C9);}
s[NH(PW.s)]
ƒ (I,D){return I<D;}


K7['NjUYW']
ƒ (C8,C9){var Nk=ND;return s[Nk(l6.s)](C8,C9);}
s[Nk(l6.s)]
ƒ (I,D){return I|D;}


K7['ElrQl']
ƒ (C8,C9){var Nu=ND;return s[Nu(Pk.s)](C8,C9);}
s[Nu(Pk.s)]
ƒ (I,D){return I&D;}


K7['Aqrxt']
ƒ (C8,C9){var NG=ND;return s[NG(lC.s)](C8,C9);}
s[NG(lC.s)]
ƒ (I,D){return I==D;}


K7['sdhJj']
ƒ (C8,C9){var Ny=ND;return s[Ny(lN.s)](C8,C9);}
s[Ny(lN.s)]
ƒ (I,D){return I-D;}


K7['qERUm']
ƒ (C8,C9){var No=ND;return s[No(lI.s)](C8,C9);}
s[No(lI.s)]
ƒ (I,D){return I(D);}


K7['qOGSu']
ƒ (C8,C9){var Nz=ND;return s[Nz(PJ.s)](C8,C9);}
s[Nz(PJ.s)]
ƒ (I,D){return I==D;}


K7['IMjWu']
ƒ (C8,C9){var NM=ND;return s[NM(lD.s)](C8,C9);}
s[NM(lD.s)]
ƒ (I,D){return I<D;}



K7['pEMmR']
ƒ (C8,C9){var Nv=ND;return s[Nv(ls.s)](C8,C9);}
s[Nv(ls.s)]
ƒ (I,D){return I|D;}


K7['mhaVB']
ƒ (C8,C9){var NZ=ND;return s[NZ(ld.s)](C8,C9);}
s[NZ(ld.s)]
ƒ (I,D){return I<<D;}


K7['abmNA']
ƒ (C8,C9){var Na=ND;return s[Na(lY.s)](C8,C9);}
s[Na(lY.s)]
ƒ (I,D){return I&D;}


K7['NzFED']
ƒ (C8,C9){var I0=ND;return s[I0(lV.s)](C8,C9);}
s[I0(lV.s)]
ƒ (I,D){return I==D;}


K7['FAfic']
ƒ (C8,C9){var I1=ND;return s[I1(lR.s)](C8,C9);}
s[I1(lR.s)]
ƒ (I,D){return I-D;}


K7['IIwPd']
ƒ (C8,C9){var Nl=ND;return s[Nl(Pw.s)](C8,C9);}
s[Nl(Pw.s)]
ƒ (I,D){return I(D);}


K7['KTmNC']
ƒ (C8,C9){var Nr=ND;return s[Nr(Pv.s)](C8,C9);}
s[Nr(Pv.s)]
ƒ (I,D){return I-D;}


K7['IOYyt']
ƒ (C8,C9){var I2=ND;return s[I2(lL.s)](C8,C9);}
s[I2(lL.s)]
ƒ (I,D){return I(D);}

【源js代码】下面是一个js代码的s0函数：
// 输入示例：
// 参数1：C8: -281929993|0|1732434046324|1
// 参数2：C9 -0x206f + 0xa * 0x32b + 0xc7, 固定数字6
// 参数3：固定函数Cs
// 浏览器控制台的输出信息
// Cs
// ƒ (CI){var dH=dl;return CC[dH(EW.s)][dH(EW.K)](CI);}
// dH(EW.s)
// 'DCAiy'
// dH(EW.K)
// 'charAt'
// CC
// 固定：{DCAiy: 'DGi0YA7BemWnQjCl4+bR3f8SKIF9tUz/xhr2oEOgPpac=61ZqwTudLkM5vHyNXsVJ'}

输出示例：
CN = "n4mxBD2DgifquDBqDTexUgrDnl9u=Dkn9jeD"
'sO': function(C8, C9, Cs) {
    var dE = ND;
    if (K7['SjfXJ'](null, C8)) {
        return '';
    }

    // 初始化变量
    var CK, Cj, CC, CN;
    var CI = {};
    var CD = {};
    var Cd = '';
    var CY = 2;
    var CV = 3;
    var CR = 2;
    var CL = [];
    var Cb = 0;
    var Cn = 0;

    for (CA = 0; K7['lLdZH'](CA, C8['length']); CA++) {
        CC = C8['charAt'](CA);
        if (!Object['prototype']['hasOwnProp' + 'erty']['call'](CI, CC)) {
            CI[CC] = CV++;
            CD[CC] = true;
        }
        CN = K7['BUEle'](Cd, CC);
        if (Object['prototype']['hasOwnProp' + 'erty']['call'](CI, CN)) {
            Cd = CN;
        } else {
            if (Object['prototype']['hasOwnProp' + 'erty']['call'](CD, Cd)) {
                if (K7['lLdZH'](Cd['charCodeAt'](-1), 0)) {
                    for (CK = 0; K7['IDfPN'](CK, CR); CK++) {
                        Cb <<= 1;
                        if (K7['SjfXJ'](Cn, K7['pjjrR'](C9, 1))) {
                            Cn = 0;
                            CL['push'](K7['IIwPd'](Cs, Cb));
                            Cb = 0;
                        } else {
                            Cn++;
                        }
                    }
                    Cj = Cd['charCodeAt'](-1);
                    for (CK = 0; K7['riKRs'](CK, 8); CK++) {
                        Cb = K7['PFwIT'](K7['fEwFm'](Cb, 1), K7['ElrQl'](1, Cj));
                        if (K7['lzmBf'](Cn, K7['zGiFk'](C9, 1))) {
                            Cn = 0;
                            CL['push'](K7['IIwPd'](Cs, Cb));
                            Cb = 0;
                        } else {
                            Cn++;
                        }
                        Cj >>= 1;
                    }
                } else {
                    // 这个分支不关注，没有正常情况下没有走到这里
                    // 如果走到这里，抛异常
                }
                if (K7['qOGSu'](0, --CY)) {
                    CY = Math['pow'](Math.max(CY, CR));
                    CR++;
                }
                delete CD[Cd];
            } else {
                Cj = CI[Cd];
                for (CK = 0; K7['riKRs'](CK, CR); CK++) {
                    Cb = K7['PFwIT'](K7['fEwFm'](Cb, 1), K7['ElrQl'](1, Cj));
                    if (K7['uuRxm'](Cn, K7['KTmNC'](C9, 1))) {
                        Cn = 0;
                        CL['push'](K7['wYIVx'](Cs, Cb));
                        Cb = 0;
                    } else {
                        Cn++;
                    }
                    Cj >>= 1;
                }
            }
            if (K7['uuRxm'](0, --CY)) {
                CY = Math['pow'](Math.max(CY, CR));
                CR++;
            }
            CI[CN] = CV++;
            Cd = String(CC);
        }
    }

    if (K7['TxwGH']('', Cd)) {
        if (Object['prototype']['hasOwnProp' + 'erty']['call'](CD, Cd)) {
            // 这个分支不关注，没有正常情况下没有走到这里
            // 如果走到这里，抛异常
        } else {
            Cj = CI[Cd];
            for (CK = 0; K7['riKRs'](CK, CR); CK++) {
                Cb = K7['NjUYW'](K7['ercgf'](Cb, 1), K7['ElrQl'](1, Cj));
                if (K7['Aqrxt'](Cn, K7['sdhJj'](C9, 1))) {
                    Cn = 0;
                    CL['push'](K7['qERUm'](Cs, Cb));
                    Cb = 0;
                } else {
                    Cn++;
                }
                Cj >>= 1;
            }
        }
        if (K7['qOGSu'](0, --CY)) {
            CY = Math['pow'](Math.max(CY, CR));
            CR++;
        }
    }

    Cj = 0;
    for (CK = 0; K7['IMjWu'](CK, CR); CK++) {
        Cb = K7['pEMmR'](K7['mhaVB'](Cb, 1), K7['abmNA'](1, Cj));
        if (K7['NzFED'](Cn, K7['FAfic'](C9, 1))) {
            Cn = 0;
            CL['push'](K7['IIwPd'](Cs, Cb));
            Cb = 0;
        } else {
            Cn++;
        }
        Cj >>= 1;
    }

    while (true) {
        Cb <<= 1;
        if (K7['qOGSu'](Cn, K7['KTmNC'](C9, 1))) {
            CL['push'](K7['IOYyt'](Cs, Cb));
            break;
        }
        Cn++;
    }
    return CL['join']('');
}

=============================================================================
测试用例01：
输入：C8: "-1938548878|0|1732437458668|1"
输出：CN: "n4+xgDuDBDcDnAWGkWD/D0WobeiK5+mqw4G=pFe4D"

测试用例02：
输入：C8: "-565752108|0|1732437342710|1"，
输出：CN: "n4fx9i0=eYqeqDKDtD/GWH4QqqiwzLwoo4TD"
=============================================================================

任务：根据已知条件、源js代码、输入示例、输出示例，将上述的s0函数转换为本地可运行的JS函数，并增加测试用例的运行

// 第二次prompt：
任务：将测试通过的本地JS代码转换为Python代码

```

✅结果：对应python函数：`sign_url_utls.py` 中的`s0`函数