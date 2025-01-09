// API签名的入口函数
// 输入示例：{
// "aJ": true,
// "aK": "/srv200/api/pub/basic/getConfig?t=1732953722436",
// "aL": 0,
// "aM": "",
// "aN": "",
// "aO": ""
ar = Object['\x73\x65' + '\x74\x50' + '\x72\x6f' + '\x74\x6f' + '\x74\x79' + '\x70\x65' + '\x4f\x66']({
    '\x73\x69\x67\x6e\x61\x74\x75\x72\x65' (aF, aG, aH, aI, aJ, aK) {
        aF = aF ? 0x15c6 + 0x8cc + 0x5 * -0x61d : -0x11e2 + 0xd8a * -0x1 + 0x1f6c,
            aG = at['\x41\x42' + '\x71\x59' + '\x59'](aB, az(aG) || at['\x63\x49' + '\x46\x53' + '\x63'](Q)),
            aI = at['\x74\x79' + '\x52\x61' + '\x49'](aB, at['\x52\x41' + '\x43\x6b' + '\x6f'](az, aI) || Q()),
            aJ = aB(at['\x67\x51' + '\x79\x5a' + '\x57'](az, aJ) || at['\x49\x6d' + '\x77\x74' + '\x73'](Q)),
            aK = at['\x41\x42' + '\x71\x59' + '\x59'](az, aK) || Q();
        try {
            return (aL = at['\x47\x74' + '\x63\x77' + '\x73'](aw['\x73\x69' + '\x67\x6e' + '\x61\x74' + '\x75\x72' + '\x65'](aF, aG, aH, aI, aJ, aK), -0x3 * -0x5ab + 0x2bb * 0x4 + -0x1 * 0x1bed)) ? {
                '\x6e\x6f\x6e\x63\x65': at['\x74\x79' + '\x52\x61' + '\x49'](ay, at['\x63\x46' + '\x52\x43' + '\x7a'](aE, aL + (0x1d31 + 0x550 + 0x2281 * -0x1))),
                '\x74\x69\x6d\x65\x73\x74\x61\x6d\x70': at['\x69\x61' + '\x4d\x52' + '\x55'](ay, at['\x67\x51' + '\x79\x5a' + '\x57'](aE, at['\x61\x43' + '\x6e\x6f' + '\x62'](aL, 0xf1d * 0x1 + -0xdc5 + -0xa * 0x22))),
                '\x73\x69\x67\x6e\x61\x74\x75\x72\x65': ay(aE(at['\x51\x6e' + '\x77\x75' + '\x6f'](aL, -0xfa1 + 0x13d * -0x1 + 0x10e6)))
            } : null;
        } finally {
            at['\x4b\x61' + '\x72\x4f' + '\x6c'](aC, aG),
                at['\x75\x64' + '\x52\x65' + '\x6a'](aC, aI),
                at['\x74\x79' + '\x52\x61' + '\x49'](aC, aJ);
        }
        var aL;
    }
}, aw);

// 反混淆后：
ar = Object['setPrototypeOf']({
    'signature' (aF, aG, aH, aI, aJ, aK) {
            aF = aF ? 1 : 0,
            aG = at['ABqYY'](aB, az(aG) || at['cIFSc'](Q)),
            aI = at['tyRaI'](aB, at['RACkoc'](az, aI) || Q()),
            aJ = aB(at['gQyZW'](az, aJ) || at['Imwts'](Q)),
            aK = at['ABqYY'](az, aK) || Q();
        try {
            return (aL = at['Gtcws'](aw['signature'](aF, aG, aH, aI, aJ, aK), 1443 + 6996 + -8029)) ? {
                'nonce': at['tyRaI'](ay, at['cFRVz'](aE, aL + (4641 + 1360 + -4329))),
                'timestamp': at['iaMRU'](ay, at['gQyZW'](aE, at['aCnob'](aL, 3873 + -3453 + -162))),
                'signature': ay(aE(at['Qnwwo'](aL, -1217 + 313 * -1 + 2806)))
            } : null;
        } finally {
            at['KarOl'](aC, aG),
                at['udRej'](aC, aI),
                at['tyRaI'](aC, aJ);
        }
        var aL;
    }
}, aw);

// 解释：
// 1. 这个代码创建了一个对象并使用 Object.setPrototypeOf 方法将其原型设置为 aw。
// 2. 对象中定义了一个名为 'signature' 的方法，这个方法有六个参数。
// 3. 函数内部有一系列赋值和函数调用，大多数函数调用来自对象 at。
// 4. 在 try 块中调用了 aw.signature 方法，并根据返回值 aL 来决定返回一个对象还是 null。
// 5. finally 块用于清理操作，无论 try 中是否抛出异常，都会执行。

// 总的来说，这段代码通过大量混淆来隐藏其逻辑，但反混淆后看起来是一些函数调用和逻辑处理。
// 可能用于某种签名验证或安全相关的操作。




// 输入示例：aF = /srv100140/api/pub/sport/venue/getVenueOrderList?salesItemId=100000&curDate=1732464000000&venueGroupId=&t=1732539277899
// 输出示例：aH = 49520
// 备注： 
function az(aF) {
    if (q['\x6a\x63' + '\x64\x6a' + '\x67'](null, aF))
        return -0x19d * 0x16 + 0x42c + 0x1f52;
    var aG = aF['\x6c\x65' + '\x6e\x67' + '\x74\x68'],
        aH = aw['\x5f\x5f' + '\x6e\x65' + '\x77'](q['\x44\x6a' + '\x4b\x56' + '\x52'](aG, -0x1a51 + 0x1863 * -0x1 + 0x10e7 * 0x3), -0x15f3 + -0x5a * 0x1e + 0x2081) >>> -0x1b3e + -0x2ab * -0xb + 0x7 * -0x4d,
        aI = new Uint16Array(ax['\x62\x75' + '\x66\x66' + '\x65\x72']);
    for (let aJ = 0x240b * 0x1 + -0x1368 + -0x1 * 0x10a3; q['\x6c\x6a' + '\x4f\x50' + '\x6a'](aJ, aG); ++aJ)
        aI[q['\x41\x64' + '\x73\x43' + '\x67'](q['\x67\x79' + '\x74\x51' + '\x67'](aH, -0x1 * 0x1cfa + -0x1 * 0x134f + 0x304a * 0x1), aJ)] = aF['\x63\x6f' + '\x64\x65' + '\x50\x6f' + '\x69\x6e' + '\x74\x41' + '\x74'](aJ);
    return aH;
}




// 输入示例：aF = 44576
// 输出示例：aH = 49520
// 备注： 
function aB(aF) {
    var aG = {
        '\x6b\x49\x57\x4e\x63': function(aI, aJ) {
            return q['\x68\x45' + '\x7a\x74' + '\x69'](aI, aJ);
        },
        '\x43\x45\x49\x65\x4f': function(aI, aJ) {
            return q['\x51\x79' + '\x64\x74' + '\x42'](aI, aJ);
        }
    };
    if (q['\x63\x43' + '\x59\x5a' + '\x72'] === q['\x63\x43' + '\x59\x5a' + '\x72']) {
        var aH;
        return aF && ((aH = aA['\x67\x65' + '\x74'](aF)) ? aA['\x73\x65' + '\x74'](aF, q['\x50\x6b' + '\x52\x69' + '\x76'](aH, 0x21f8 + -0x319 * -0x5 + -0x3174)) : aA['\x73\x65' + '\x74'](aw['\x5f\x5f' + '\x70\x69' + '\x6e'](aF), -0x5d2 + -0x3 * -0x569 + -0xa68)),
            aF;
    } else {
        var aJ = {
                '\x74\x6d\x42\x48\x4f': function(aM, aN) {
                    return aG['\x6b\x49' + '\x57\x4e' + '\x63'](aM, aN);
                },
                '\x76\x54\x79\x4e\x58': function(aM, aN) {
                    return aM < aN;
                },
                '\x74\x76\x74\x51\x64': function(aM, aN) {
                    return aM % aN;
                },
                '\x69\x6e\x6d\x42\x56': function(aM, aN) {
                    return aM + aN;
                }
            },
            aK = aC(function(aM, aN) {
                var aO = 0x45 * -0x22 + 0x1 * 0x599 + -0x1c9 * -0x2 < arguments['\x6c\x65' + '\x6e\x67' + '\x74\x68'] && aJ['\x74\x6d' + '\x42\x48' + '\x4f'](void(-0xa49 * 0x1 + 0x10e2 + -0x699), aN) ? aN : -0x1eea + 0x90f + -0x1 * -0x3ceb;
                if (null == aM)
                    return [];
                var aP = [];
                for (let aQ = -0x14df + -0x16a + 0x5 * 0x475, aR = 0x147e + 0x16 * -0xe4 + -0xe6, aS = 0x2687 + 0x163e + -0x1 * 0x3cc5, aT = aM['\x6c\x65' + '\x6e\x67' + '\x74\x68']; aJ['\x76\x54' + '\x79\x4e' + '\x58'](aQ, aO); aQ += 0x316 + -0x1 * -0x1e0b + 0x2 * -0x1090,
                    aR += 0x139e + -0x2248 + 0x1 * 0xeab,
                    aS = aJ['\x74\x76' + '\x74\x51' + '\x64'](aJ['\x69\x6e' + '\x6d\x42' + '\x56'](aS, aR), aT))
                    aP['\x70\x75' + '\x73\x68'](aM[aS]);
                return aP;
            }([...new a5(T['\x72\x65' + '\x73\x75' + '\x6c\x74'])])['\x6a\x6f' + '\x69\x6e']('\x2d')),
            aL = {};
        aL['\x6b\x65' + '\x79'] = ag,
            aL['\x76\x61' + '\x6c\x75' + '\x65'] = aK,
            aG['\x43\x45' + '\x49\x65' + '\x4f'](aw, aL);
    }
}