"use strict";
(self["webpackChunkydmap_web_portal"] = self["webpackChunkydmap_web_portal"] || []).push([
            [6264], {
                60841: (e, t, s) => {
                    s.d(t, {
                        A: () => c
                    });
                    var i = function() {
                            var e = this,
                                t = e.$createElement,
                                s = e._self._c || t;
                            return e.name ? s("div", {
                                ref: "nav",
                                staticClass: "abs-nav"
                            }, [s("div", {
                                staticClass: "box-weather"
                            }, [s("img", {
                                staticClass: "img-max",
                                attrs: {
                                    src: e.CDN_STATIC_HOST + "/images/svg/" + encodeURIComponent(e.name) + ".svg"
                                }
                            }), s("span", {
                                staticClass: "block ml-[2px]"
                            }, [e._v(e._s(e.name))])])]) : e._e()
                        },
                        a = [];
                    s(27495),
                        s(25440);
                    const r = {
                            props: {
                                bottom: String,
                                id: Number,
                                curDate: {
                                    type: Number,
                                    default: 0
                                },
                                loadingFlg: {
                                    type: Boolean,
                                    default: !1
                                }
                            },
                            data() {
                                return {
                                    name: "",
                                    timeVal: null,
                                    day: new Date((new Date).setHours(0, 0, 0, 0)).getTime(),
                                    timeIt: null
                                }
                            },
                            watch: {
                                curDate() {
                                    this.getWeatherFun()
                                },
                                id(e) {
                                    this.setTimeoutFun(e)
                                }
                            },
                            destroyed() {
                                this.closeFun()
                            },
                            methods: {
                                flushCss() {
                                    if (this.$refs.nav)
                                        if (this.bottom) {
                                            const e = this.bottom;
                                            this.$refs.nav.setAttribute("style", `\n          bottom: ${e};\n          bottom: calc(var(--body-padding-offset-bottom) + ${e});\n          bottom: calc(var(--body-padding-offset-bottom) + ${e} + env(safe-area-inset-bottom, 0px));\n          `)
                                        } else
                                            this.$refs.nav.setAttribute("style", "")
                                },
                                closeFun() {
                                    this.name = "",
                                        clearTimeout(this.timeVal),
                                        clearTimeout(this.timeIt)
                                },
                                getWeatherFun() {
                                    if (!this.curDate)
                                        return void(this.name = "");
                                    const e = {
                                        weatherDate: this.curDate,
                                        salesId: this.id
                                    };
                                    this.$http.get("/pub/sport/venue/getWeather", e, {
                                        silent: this.loadingFlg
                                    }).then((e => {
                                        if (!e)
                                            return void(this.name = "");
                                        const t = (new Date).getHours() > 18 ? e.nightWeather : e.dayWeather;
                                        this.name = t.replace("/", "-"),
                                            this.$nextTick((() => {
                                                this.flushCss()
                                            })),
                                            clearTimeout(this.timeVal),
                                            this.curDate === this.day && (this.timeVal = setTimeout((() => {
                                                this.getWeatherFun()
                                            }), 18e5))
                                    })).catch((() => {
                                        this.name = ""
                                    }))
                                },
                                setTimeoutFun(e) {
                                    e ? (this.loadingFlg || this.getWeatherFun(),
                                        clearTimeout(this.timeIt),
                                        this.timeIt = setTimeout((() => {
                                            e === this.id && this.getWeatherFun()
                                        }), 1e3)) : this.closeFun()
                                }
                            }
                        },
                        l = r;
                    var n = s(81656),
                        o = (0,
                            n.A)(l, i, a, !1, null, "4cea0768", null);
                    const c = o.exports
                },
                24098: (e, t, s) => {
                    s.d(t, {
                        A: () => c
                    });
                    var i = function() {
                            var e = this,
                                t = e.$createElement,
                                s = e._self._c || t;
                            return e.marquee || e.useTipText ? s("div", {
                                ref: "marqueeBox",
                                staticClass: "marquee-box calc-box"
                            }, [s("div", {
                                ref: "marqueeTip",
                                staticClass: "marquee-tip",
                                class: {
                                    "marquee-tip-txt": e.useTipText,
                                        "!pl-3 !pr-2": e.focus
                                }
                            }, [s("div", {
                                staticClass: "text-overflow marquee-tip-txt-inner"
                            }, [s("i", {
                                class: e.focus ? "i-focus text-[#ED6A0C] !text-[24px] align-middle" : "icon-pt-notice"
                            }), e._v(" " + e._s(e.useTipText) + " ")])]), s("div", {
                                staticClass: "marquee-scroll"
                            }, [s("div", {
                                ref: "marquee",
                                staticClass: "marquee",
                                style: {
                                    left: e.marqueeLeft + "px"
                                }
                            }, [e._v(" " + e._s(e.text) + " ")])])]) : e._e()
                        },
                        a = [];
                    const r = {
                            props: {
                                text: String,
                                tipText: String,
                                focus: Boolean
                            },
                            data() {
                                return {
                                    animationFrame: null,
                                    marqueeLeft: 0,
                                    marqueeWidth: 0
                                }
                            },
                            computed: {
                                marquee() {
                                    var e;
                                    return (null === (e = this.text) || void 0 === e ? void 0 : e.trim().length) > 0
                                },
                                useTipText() {
                                    var e;
                                    return null === (e = this.tipText) || void 0 === e ? void 0 : e.trim()
                                }
                            },
                            watch: {
                                text: {
                                    handler() {
                                        this.marqueeLeft = 0,
                                            this.$nextTick((() => {
                                                const e = this.$refs.marquee;
                                                this.marqueeWidth = e ? Math.max(e.offsetWidth, e.clientWidth) : 0,
                                                    this.animationFrame && window.clearTimeout(this.animationFrame),
                                                    this.mq()
                                            }))
                                    },
                                    immediate: !0
                                }
                            },
                            methods: {
                                mq() {
                                    if (this.marquee) {
                                        const { marqueeBox: e, marqueeTip: t } = this.$refs, s = e ? Math.max(e.offsetWidth, e.clientWidth) : 0, i = t ? Math.max(t.offsetWidth, t.clientWidth) : 0, a = s - i;
                                        this.marqueeWidth > a && (this.marqueeLeft < -this.marqueeWidth && (this.marqueeLeft = a + 10),
                                                this.marqueeLeft = this.marqueeLeft - 1),
                                            this.animationFrame = window.setTimeout(this.mq, 20)
                                    } else
                                        this.marqueeLeft = 0
                                }
                            }
                        },
                        l = r;
                    var n = s(81656),
                        o = (0,
                            n.A)(l, i, a, !1, null, "243f0150", null);
                    const c = o.exports
                },
                56898: (e, t, s) => {
                    s.d(t, {
                        A: () => g
                    });
                    var i = function() {
                            var e = this,
                                t = e.$createElement,
                                s = e._self._c || t;
                            return s("section", {
                                directives: [{
                                    name: "show",
                                    rawName: "v-show",
                                    value: e.showShare,
                                    expression: "showShare"
                                }],
                                staticClass: "open-share fixed-width",
                                style: {
                                    "z-index": e.zindex
                                }
                            }, [s("div", {
                                ref: "headWrapper",
                                staticClass: "h-60"
                            }, [s("canvas", {
                                ref: "headCanvas"
                            }, [e._v(" 您的浏览器不支持Canvas ")]), s("div", {
                                staticClass: "text-wrapper"
                            }, [e.config ? s("div", {
                                staticClass: "text-edit text-[14px]",
                                attrs: {
                                    contenteditable: "true"
                                },
                                on: {
                                    input: e.handleTitleChange
                                }
                            }, [e._v(" " + e._s(e.config.title) + " ")]) : e._e()]), s("img", {
                                ref: "headImg",
                                staticClass: "img-wrapper",
                                attrs: {
                                    alt: "分享图"
                                }
                            })]), s("div", {
                                staticClass: "flex justify-around btns"
                            }, [e.config ? s("div", {
                                staticClass: "btn copy",
                                on: {
                                    click: e.handleCopy
                                }
                            }, [e._v(" 复制链接 ")]) : e._e(), s("div", {
                                staticClass: "btn download"
                            }, [e._v("长按保存")])]), s("div", {
                                class: {
                                    "pic-select": !0,
                                    holding: 0 === e.configPicList.length || 1 === e.configPicList.length
                                }
                            }, [s("div", [e._v("请选择一张素材图作为封面")]), s("div", {
                                staticClass: "flex pic-list"
                            }, e._l(e.configPicList, (function(t, i) {
                                return s("div", {
                                    key: t,
                                    staticClass: "pt-5 pr-5",
                                    class: [e.curentIndex === i ? "has-icon" : ""],
                                    on: {
                                        click: function(t) {
                                            return e.handleCurentChange(i)
                                        }
                                    }
                                }, [s("img", {
                                    attrs: {
                                        src: e.formatImageUrl(t, "avatar_prew", e.DEFAULT_GIFT_PIC_PATH + "/200X200.jpg"),
                                        alt: "配置图片"
                                    }
                                })])
                            })), 0)]), s("div", {
                                directives: [{
                                    name: "show",
                                    rawName: "v-show",
                                    value: e.isShowFooter,
                                    expression: "isShowFooter"
                                }],
                                staticClass: "fixed",
                                on: {
                                    click: e.hide
                                }
                            }, [s("div", [e._v("返回")])])])
                        },
                        a = [],
                        r = s(82887),
                        l = s(79735),
                        n = s(42098),
                        o = s(94171),
                        c = s(64880),
                        d = s(25800),
                        h = s(8832);
                    const u = {
                            mixins: [c.A],
                            inject: ["serviceInfo"],
                            props: {
                                title: String,
                                link: String,
                                img: [String, Array],
                                desc: String,
                                proactive: {
                                    default: !0,
                                    type: Boolean
                                }
                            },
                            data() {
                                return {
                                    wrappePASCSMTShareLink: d.y8,
                                    bgImg: `https:${d.qv}/images/portal/share-bg.png`,
                                    bgLogo: `https:${d.qv}/images/portal/wechat.png`,
                                    drp: 3,
                                    showShare: !1,
                                    curentIndex: 0,
                                    config: null,
                                    canvasTile: "",
                                    windowHeight: window.innerHeight || 0,
                                    showHeight: window.innerHeight || 0,
                                    isShowFooter: !0,
                                    zindex: l.A.syncZIndex()
                                }
                            },
                            computed: {
                                configPicList() {
                                    var e, t;
                                    return Array.isArray(null === (e = this.config) || void 0 === e ? void 0 : e.img) ? this.config.img : [null === (t = this.config) || void 0 === t ? void 0 : t.img]
                                },
                                configPicImage() {
                                    return (this.configPicList || []).map((e => {
                                        const t = new Image;
                                        return t.crossOrigin = "",
                                            t.src = `${e}?${Date.now()}`, {
                                                url: e,
                                                el: t
                                            }
                                    }))
                                },
                                curentPic() {
                                    return this.configPicList[this.curentIndex]
                                }
                            },
                            watch: {
                                showHeight(e) {
                                    this.isShowFooter = !(this.windowHeight > e)
                                },
                                showShare(e) {
                                    e && (this.zindex = l.A.syncZIndex(),
                                        this.$nextTick((() => {
                                            this.handleDrawHead(this.curentPic)
                                        })))
                                },
                                curentPic(e) {
                                    e && this.showShare && this.$nextTick((() => {
                                        this.handleDrawHead(e)
                                    }))
                                }
                            },
                            mounted() {
                                this.proactive && this.$nextTick((() => {
                                        this.reg()
                                    })),
                                    window.addEventListener("resize", (() => {
                                        this.showHeight = window.innerHeight
                                    }))
                            },
                            methods: {
                                getWechatLogo(e) {
                                    return new Promise((t => {
                                        const s = o.j.get("wechatLogoInfo");
                                        s && e - s.saveTime < 2592e6 ? t(s.logoBase64) : this.$http.get("/pub/wechat/getFollowInfo").then((s => {
                                            if (null !== s && void 0 !== s && s.appQrUrl) {
                                                const i = new Image;
                                                i.setAttribute("crossOrigin", "Anonymous"),
                                                    i.addEventListener("load", (function() {
                                                        const s = document.createElement("canvas");
                                                        s.setAttribute("id", "logoC"),
                                                            s.setAttribute("width", "82"),
                                                            s.setAttribute("height", "82"),
                                                            document.body.append(s);
                                                        const a = document.querySelector("#logoC"),
                                                            r = a.getContext("2d");
                                                        r.drawImage(i, -174, -174),
                                                            o.j.put("wechatLogoInfo", {
                                                                date: e,
                                                                logoBase64: a.toDataURL("image/jpeg")
                                                            }),
                                                            t(a.toDataURL("image/jpeg")),
                                                            s.remove()
                                                    })),
                                                    i.addEventListener("error", (function() {
                                                        t("")
                                                    })),
                                                    i.src = s.appQrUrl
                                            } else
                                                l.A.alert("获取图片失败, 请联系管理员"),
                                                t("")
                                        }))
                                    }))
                                },
                                handleDrawHead(e) {
                                    var t;
                                    const s = null === (t = this.$refs.headCanvas) || void 0 === t ? void 0 : t.getContext("2d"),
                                        i = this.$refs.headWrapper.offsetWidth,
                                        a = this.$refs.headWrapper.offsetHeight;
                                    this.$refs.headCanvas.width = i * this.drp,
                                        this.$refs.headCanvas.height = a * this.drp,
                                        this.$refs.headCanvas.style.width = i,
                                        this.$refs.headCanvas.style.height = a,
                                        s.fillStyle = "#fff",
                                        s.fillRect(0, 0, i * this.drp, a * this.drp),
                                        this.drawBgImg(s, i * this.drp, a * this.drp * .6, this.bgImg, e)
                                },
                                drawBgImg(e, t, s, i, a) {
                                    this.createImgPromise(i).then((async i => {
                                        e.drawImage(i, 0, 0, t, .8 * s);
                                        const r = await this.getWechatLogo(this.currentServerTime) || this.bgLogo;
                                        this.createImgPromise(r).then((s => {
                                            var i;
                                            const r = 60,
                                                l = 60;
                                            e.drawImage(s, t / 2 - r * this.drp / 2, l, r * this.drp, l * this.drp),
                                                e.font = 18 * this.drp + "px normal",
                                                e.fillStyle = "#fff",
                                                e.fillText(this.serviceInfo.srvName, t / 2 - 9 * this.serviceInfo.srvName.length * this.drp, 1.75 * l * this.drp),
                                                e.fillRect((t - 250 * this.drp) / 2, 2 * l * this.drp, 250 * this.drp, 250 * this.drp),
                                                (0,
                                                    n.H)(e, (0,
                                                    d.y8)(null === (i = this.config) || void 0 === i ? void 0 : i.link), 240 * this.drp, {
                                                    originLeft: (t - 240 * this.drp) / 2,
                                                    originTop: 2 * l * this.drp + 5 * this.drp
                                                }),
                                                e.fillStyle = "#000",
                                                e.font = 14 * this.drp + "px normal";
                                            const o = 2.65 * l * this.drp + 30 * this.drp + 200 * this.drp;
                                            e.fillText("长按图片识别二维码进入", t / 2 - 80 * this.drp, o),
                                                e.fillStyle = "#f0f0f0",
                                                e.fillRect(t / 2 - .4 * t, o + 10 * this.drp, .8 * t, 2),
                                                e.fillStyle = "#666",
                                                e.font = 16 * this.drp + "px normal",
                                                (0,
                                                    d.OU)(e, this.canvasTile.length > 25 ? this.canvasTile.slice(0, 25) : this.canvasTile, r * this.drp, o + 40 * this.drp, .44 * this.$refs.headCanvas.width, 14 * this.drp);
                                            const c = this.configPicImage.find((e => e.url === a)).el;
                                            c.complete ? e.drawImage(c, .7 * t, o + 20 * this.drp, l * this.drp * 1.5, r * this.drp * 1.5) : c.addEventListener("load", (() => {
                                                e.drawImage(c, .7 * t, o + 20 * this.drp, l * this.drp * 1.5, r * this.drp * 1.5);
                                                const s = this.$refs.headCanvas.toDataURL();
                                                this.$refs.headImg.src = s
                                            }));
                                            const h = this.$refs.headCanvas.toDataURL();
                                            this.$refs.headImg.src = h
                                        }))
                                    }))
                                },
                                handleCopy() {
                                    (0,
                                        d.Dk)((0,
                                        d.y8)(this.config.link)).then((() => {
                                        l.A.alert("复制成功")
                                    })).catch((e => {
                                        l.A.alert(`复制失败: ${e.message}`)
                                    }))
                                },
                                handleCurentChange(e) {
                                    this.curentIndex = e;
                                    const t = {
                                        ...this.config,
                                        img: this.curentPic
                                    };
                                    this.$wxShare(t, (() => {
                                        this.$emit("onRegSuccess")
                                    }))
                                },
                                handleTitleChange: (0,
                                    r.throttle)(500, (function(e) {
                                    var t;
                                    if (e.target.textContent.trim().length > 25)
                                        return;
                                    const s = {
                                        ...this.config,
                                        img: this.curentPic,
                                        title: e.target.textContent.trim()
                                    };
                                    this.canvasTile = e.target.textContent.trim();
                                    const i = null === (t = this.$refs.headCanvas) || void 0 === t ? void 0 : t.getContext("2d");
                                    i.fillStyle = "#fff",
                                        i.fillRect(40 * this.drp, .8 * this.$refs.headCanvas.height, .55 * this.$refs.headCanvas.width, 80 * this.drp),
                                        i.fillStyle = "#666",
                                        i.font = 16 * this.drp + "px normal",
                                        (0,
                                            d.OU)(i, this.canvasTile, 40 * this.drp, .8 * this.$refs.headCanvas.height + 60, .5 * this.$refs.headCanvas.width, 16 * this.drp);
                                    const a = this.$refs.headCanvas.toDataURL();
                                    this.$refs.headImg.src = a,
                                        this.canvasTile = e.target.textContent.trim(),
                                        this.$wxShare(s, (() => {
                                            this.$emit("onRegSuccess")
                                        }))
                                })),
                                reg(e) {
                                    var t;
                                    let s = e;
                                    if (null == s) {
                                        const e = {};
                                        null != this.title && (e.title = this.title),
                                            null != this.link && (e.link = this.link),
                                            null != this.img && (e.img = this.img),
                                            null != this.desc && (e.desc = this.desc),
                                            Object.keys(e).length > 0 && (s = e)
                                    }
                                    this.config = s,
                                        this.canvasTile = (null === (t = this.config) || void 0 === t ? void 0 : t.title) || "",
                                        this.$nextTick((() => {
                                            this.$wxShare({
                                                ...this.config,
                                                img: this.curentPic
                                            }, (() => {
                                                this.$emit("onRegSuccess")
                                            }))
                                        }))
                                },
                                createImgPromise(e) {
                                    return new Promise((t => {
                                        const s = new Image;
                                        s.crossOrigin = "anonymous",
                                            s.addEventListener("load", (function() {
                                                t(this)
                                            })),
                                            s.src = e
                                    }))
                                },
                                show() {
                                    this.addFee(),
                                        (0,
                                            h.o)({
                                            ...this.config,
                                            img: this.curentPic || this.serviceInfo.srvLogoImgUrl
                                        }) || (this.showShare = !0,
                                            (0,
                                                d.mh)(),
                                            this.$emit("show"))
                                },
                                hide() {
                                    this.showShare = !1,
                                        (0,
                                            d.fY)(),
                                        this.$emit("onHide")
                                },
                                addFee() {
                                    const { dataId: e, relType: t, feeType: s } = this.config || {};
                                    e && t && s && this.$addFee(e, t, s)
                                }
                            }
                        },
                        f = u;
                    var m = s(81656),
                        p = (0,
                            m.A)(f, i, a, !1, null, "295689d3", null);
                    const g = p.exports
                },
                6271: (e, t, s) => {
                    s.d(t, {
                        A: () => h
                    });
                    var i = function() {
                            var e = this,
                                t = e.$createElement,
                                s = e._self._c || t;
                            return s("div", [e.src ? s("iframe", {
                                ref: "iframe",
                                attrs: {
                                    frameborder: "0",
                                    border: "0",
                                    width: "100%",
                                    src: e.src
                                }
                            }) : e._e()])
                        },
                        a = [],
                        r = s(85433),
                        l = s(25800);
                    const n = {
                            props: {
                                newsId: [Number, String],
                                url: String
                            },
                            computed: {
                                src() {
                                    return this.newsId || this.url ? (0,
                                        l.YV)("/_/s/news-viewer.html", {
                                        url: this.url,
                                        id: this.newsId
                                    }) : null
                                }
                            },
                            mounted() {
                                window.addEventListener("message", this.onMessage)
                            },
                            destroyed() {
                                window.removeEventListener("message", this.onMessage)
                            },
                            methods: {
                                onMessage(e) {
                                    const t = this.$refs.iframe;
                                    if (e.source !== (null === t || void 0 === t ? void 0 : t.contentWindow))
                                        return;
                                    let s;
                                    try {
                                        s = JSON.parse(e.data)
                                    } catch (n) {
                                        return
                                    }
                                    const { type: i, payload: a } = s || {};
                                    switch (i) {
                                        case "central.viewHeightChangeNew":
                                            {
                                                const { body: e } = a || {},
                                                { height: s } = e,
                                                i = (0,
                                                    l.Et)(e) ? e : s;
                                                t.style.height = `${i + 10}px`,
                                                this.$emit("landed");
                                                break
                                            }
                                        case "central.imgPreview":
                                            {
                                                const { images: e, startPosition: t } = a || {};
                                                (0,
                                                    r["default"])({
                                                    images: e,
                                                    startPosition: t
                                                });
                                                break
                                            }
                                        default:
                                            console.warn(`central 收到未识别的消息通知：${i}, 可能并不是发给 central 处理的.`)
                                    }
                                }
                            }
                        },
                        o = n;
                    var c = s(81656),
                        d = (0,
                            c.A)(o, i, a, !1, null, null, null);
                    const h = d.exports
                },
                18294: (e, t, s) => {
                        s.r(t),
                            s.d(t, {
                                default: () => De
                            });
                        var i = {};
                        s.r(i),
                            s.d(i, {
                                F2: () => R
                            });
                        var a = function() {
                                var e = this,
                                    t = e.$createElement,
                                    s = e._self._c || t;
                                return s("section", {
                                    directives: [{
                                        name: "bodycls",
                                        rawName: "v-bodycls",
                                        value: ["bd-bg"],
                                        expression: "['bd-bg']"
                                    }]
                                }, [e.collectShow ? s("router-view") : e._e(), s("div", {
                                    directives: [{
                                        name: "show",
                                        rawName: "v-show",
                                        value: e.ready && !e.collectShow,
                                        expression: "ready && !collectShow"
                                    }],
                                    staticClass: "container agreement-container"
                                }, [s("MarqueeBox", {
                                    ref: "marqueeBox",
                                    attrs: {
                                        text: e.flushData.marqueeText,
                                        "tip-text": e.entranceRequire
                                    }
                                }), e.ready ? s("div", {
                                    ref: "others",
                                    staticClass: "bg-white sticky top-0 z-2"
                                }, [s("div", {
                                    staticClass: "flex w-full"
                                }, [s("Slider", {
                                    staticClass: "slider-item-box",
                                    attrs: {
                                        "data-list": e.serverData.itemDataList,
                                        "item-cls": 1 === e.serverData.itemDataList.length ? "!ml-[48px]" : "",
                                        idkey: "salesItemId",
                                        label: "salesItemName",
                                        type: "item",
                                        "new-item-style": ""
                                    },
                                    on: {
                                        groupChange: e.onGroupChange
                                    },
                                    model: {
                                        value: e.salesItemId,
                                        callback: function(t) {
                                            e.salesItemId = t
                                        },
                                        expression: "salesItemId"
                                    }
                                }), s("div", {
                                    staticClass: "w-[48px] h-[48px] text-[24px] item-menu leading-[42px] text-center",
                                    on: {
                                        click: e.menuFun
                                    }
                                }, [s("img", {
                                    staticClass: "w-[24px] h-[24px]",
                                    attrs: {
                                        src: e.CDN_STATIC_HOST + "/images/portal/booking_menu.png"
                                    }
                                })])], 1), e.serverData.dateDataList ? s("Slider", {
                                    attrs: {
                                        "data-list": e.serverData.dateDataList,
                                        idkey: "day",
                                        label: "dayName",
                                        label2: "weekName",
                                        type: "datetime",
                                        "item-bg-color": "#f9f9f9",
                                        "item-cls": "rounded-[4px] !p-0 new-datetime"
                                    },
                                    on: {
                                        reload: e.onDateTimeReload
                                    },
                                    scopedSlots: e._u([{
                                        key: "weather",
                                        fn: function(t) {
                                            return [e.weatherName && t.data.day === e.curDate ? s("div", {
                                                staticClass: "inline-flex flex-col align-top text-[12px] text-[#333] w-[45px] bg-[#fff] h-full items-center box-weather",
                                                on: {
                                                    click: function(t) {
                                                        t.stopPropagation(),
                                                            e.weatherShow = !0
                                                    }
                                                }
                                            }, [s("img", {
                                                staticClass: "img-max w-[20px] h-[18px]",
                                                attrs: {
                                                    src: e.CDN_STATIC_HOST + "/images/svg/" + encodeURIComponent(e.weatherName) + ".svg"
                                                }
                                            }), s("van-notice-bar", {
                                                staticClass: "leading-[18px] !h-[18px] text-[12px] w-[38px]",
                                                attrs: {
                                                    speed: "20",
                                                    background: "#fff",
                                                    color: "#333",
                                                    scrollable: e.weatherName.length > 3,
                                                    text: e.weatherName
                                                }
                                            })], 1) : e._e()]
                                        }
                                    }], null, !1, 2187525585),
                                    model: {
                                        value: e.curDate,
                                        callback: function(t) {
                                            e.curDate = t
                                        },
                                        expression: "curDate"
                                    }
                                }) : e._e(), e.isTicket && e.useCounterTemplate && e.flushData.timeSlotList && e.flushData.timeSlotList.length > 0 ? s("Slider", {
                                    attrs: {
                                        "data-list": e.flushData.timeSlotList,
                                        "check-disable": e.checkSlotTimeDisable,
                                        idkey: "startTime",
                                        label: "startTime"
                                    },
                                    scopedSlots: e._u([{
                                        key: "default",
                                        fn: function(t) {
                                            return [s("span", {
                                                staticClass: "inline-block leading-[34px] px-[8px] rounded-[17px] border border-solid border-[#f0f0f0] cust-item"
                                            }, [e._v(" " + e._s(e.formatHM(t.data.startTime)) + "-" + e._s(e.formatHMCsvt(t.data.endTime)) + " ")])]
                                        }
                                    }], null, !1, 3210607622),
                                    model: {
                                        value: e.selectedSlotStartTime,
                                        callback: function(t) {
                                            e.selectedSlotStartTime = t
                                        },
                                        expression: "selectedSlotStartTime"
                                    }
                                }) : s("div", {
                                    staticClass: "h-[4px]"
                                })], 1) : e._e(), s("ScheduleTable", {
                                    ref: "scheduleTable",
                                    attrs: {
                                        params: e.scheduleTableParams,
                                        "max-height": e.tableMaxHeight
                                    },
                                    on: {
                                        dataReload: e.onDataReload,
                                        selectedReload: e.onSelectedReload,
                                        gotoNext: e.sure,
                                        hourFun: e.onHourFun
                                    }
                                }), e.flushData.someOneOnline ? s("div", {
                                    ref: "operation",
                                    staticClass: "fixed-bt basic-fixed-bt fixed-width !py-[6px] flex items-center"
                                }, [e.isTicket && e.agreementUrl || !e.isTicket || e.useCounterTemplate ? s("div", {
                                    staticClass: "wrapper-left"
                                }, [s("div", {
                                    staticClass: "money text-left"
                                }, [!e.isTicket || e.useCounterTemplate ? s("span", [e._v(" 共计 "), s("span", {
                                    staticClass: "total"
                                }, [e._v(e._s(e.formatMoney(e.totalPrice)) + " ")]), e._v(" 元 ")]) : e._e(), e.agreementUrl ? s("span", {
                                    staticClass: "text-[14px] text-[#f63] ml-[12px]",
                                    on: {
                                        click: function(t) {
                                            return t.stopPropagation(),
                                                e.agreementShowFun.apply(null, arguments)
                                        }
                                    }
                                }, [e._v(" 订场须知 "), s("span", {
                                    staticClass: "inline-block w-[12px] h-[12px] bg-[#f63] rounded-full align-middle agreement-box"
                                })]) : e._e()]), !e.isTicket || e.useCounterTemplate ? s("div", {
                                    staticClass: "time-left line-clamp-2 leading-[14px]"
                                }, [e._v(" " + e._s([e.hourObj.openTime > 0 && e.formatHM(e.hourObj.openTime) + "开放预定", null != e.hourObj.hourCancel && null != e.hourObj.hourCancelType && !e.noRefund.flg && "" + e.formatModel(e.HourCancelTypes, e.hourObj.hourCancelType) + e.formatTimeDuration(e.hourObj.hourCancel, 0, !0) + "可退", e.noRefund.flg && e.noRefund.msg].filter(Boolean).join(", ")) + " ")]) : e._e()]) : e._e(), s("div", {
                                    staticClass: "wrapper-right"
                                }, [e.serverData.bookingType === e.SalesBookingTypes.CallAppointment.key && e.serverData.salesTelList && e.serverData.salesTelList.length > 0 ? s("a", {
                                    attrs: {
                                        href: "tel:" + e.serverData.salesTelList[0].salesTel
                                    }
                                }, [s("el-button", {
                                    staticClass: "full-width primary-button",
                                    attrs: {
                                        type: "text"
                                    }
                                }, [e._v(" " + e._s(e.nextBtnDisText) + " ")])], 1) : s("el-button", {
                                    staticClass: "full-width primary-button",
                                    attrs: {
                                        type: "text",
                                        disabled: !e.canNext
                                    },
                                    on: {
                                        click: e.sure
                                    }
                                }, [e._v(" " + e._s(e.nextBtnDisText || "下一步") + " ")])], 1)]) : e._e(), s("HomeWeather", {
                                    ref: "weatherBox",
                                    staticClass: "hidden",
                                    attrs: {
                                        id: e.salesId,
                                        bottom: "17.8rem",
                                        "cur-date": e.curDate
                                    }
                                }), s("van-popup", {
                                    attrs: {
                                        closeable: "",
                                        round: ""
                                    },
                                    model: {
                                        value: e.weatherShow,
                                        callback: function(t) {
                                            e.weatherShow = t
                                        },
                                        expression: "weatherShow"
                                    }
                                }, [s("div", {
                                    staticClass: "text-center w-full text-[16px] text-[#333] leading-[50px]"
                                }, [e._v(" " + e._s(e.weatherObj.dayName) + " " + e._s(e.weatherObj.weekName) + " ")]), e.curDate ? s("div", {
                                    staticClass: "flex flex-col text-[16px] text-[#333] w-[240px] items-center justify-center pb-[24px]"
                                }, [s("img", {
                                    staticClass: "img-max w-[54px] h-[54px]",
                                    attrs: {
                                        src: e.CDN_STATIC_HOST + "/images/svg/" + encodeURIComponent(e.weatherName) + ".svg"
                                    }
                                }), s("div", {
                                    staticClass: "font-medium"
                                }, [e._v(e._s(e.weatherName))])]) : e._e()]), s("van-popup", {
                                    staticClass: "bg-[#f5f5f5] px-[12px] menu-box",
                                    attrs: {
                                        round: "",
                                        position: "bottom"
                                    },
                                    model: {
                                        value: e.menuShow,
                                        callback: function(t) {
                                            e.menuShow = t
                                        },
                                        expression: "menuShow"
                                    }
                                }, [e._l(e.menuList, (function(t) {
                                    return ["navigate" !== t.path || e.lng && e.lat ? s("div", {
                                        key: t.path,
                                        staticClass: "inline-block w-[25%] px-[4px] align-middle",
                                        on: {
                                            click: function(s) {
                                                return e.gobackFun(t)
                                            }
                                        }
                                    }, [s("div", {
                                        staticClass: "w-full flex flex-col mt-[24px] items-center"
                                    }, [s("div", {
                                        staticClass: "w-[60px] h-[60px] rounded-full bg-[#fff] text-center leading-[60px]",
                                        class: [t.flg ? "text-[22px]" : "text-[30px]"]
                                    }, ["collection" === t.path && e.collectFlg ? s("span", {
                                        staticClass: "text-[#f63]"
                                    }, [s("i", {
                                        class: t.selectIcon,
                                        attrs: {
                                            "aria-hidden": "true"
                                        }
                                    })]) : s("span", {
                                        staticClass: "text-[#333]"
                                    }, [s("i", {
                                        class: t.icon,
                                        attrs: {
                                            "aria-hidden": "true"
                                        }
                                    })])]), s("div", {
                                        staticClass: "mt-[8px] text-center text-[#333] text-[14px]"
                                    }, [e._v(" " + e._s("collection" === t.path && e.collectFlg ? t.selectName : t.name) + " ")])])]) : e._e()]
                                })), s("section", {
                                    staticClass: "fixed-bt mt-[24px] px-[16px]"
                                }, [s("div", {
                                    staticClass: "full-width rounded-[24px] bg-[#fff] text-[#333] text-center leading-[48px] mb-[12px]",
                                    on: {
                                        click: function(t) {
                                            e.menuShow = !1
                                        }
                                    }
                                }, [e._v(" 取消 ")])])], 2)], 1), s("OpenShareTip", {
                                    ref: "OpenShareTip"
                                }), s("van-popup", {
                                    attrs: {
                                        closeable: "",
                                        position: "bottom"
                                    },
                                    model: {
                                        value: e.mapVisible,
                                        callback: function(t) {
                                            e.mapVisible = t
                                        },
                                        expression: "mapVisible"
                                    }
                                }, [s("div", {
                                    staticClass: "h-[50px]"
                                }), s("div", {
                                    staticClass: "map-wrapper"
                                }, [e.lng && e.lat ? s("CustMap", {
                                    ref: "amap",
                                    attrs: {
                                        lng: e.lng,
                                        lat: e.lat,
                                        name: e.flushData.salesName,
                                        address: e.serverData.address
                                    }
                                }) : e._e()], 1)]), s("Agreement", {
                                    ref: "Agreement",
                                    attrs: {
                                        "agreement-url": e.agreementUrl,
                                        "agreement-time": e.agreementTime,
                                        "agreement-read": e.agreementRead,
                                        "but-display": e.butDisplay
                                    },
                                    on: {
                                        sureFun: e.agreementSure
                                    }
                                }), s("NeVerify", {
                                    ref: "verifyComp",
                                    attrs: {
                                        "only-picture": ""
                                    },
                                    on: {
                                        confirm: e.onTicketVerifyConfirm
                                    }
                                })], 1)
                            },
                            r = [],
                            l = (s(44114),
                                s(72712),
                                s(27495),
                                s(25440),
                                s(82887)),
                            n = s(85471),
                            o = s(60841),
                            c = s(43639),
                            d = s(24098),
                            h = function() {
                                var e = this,
                                    t = e.$createElement,
                                    s = e._self._c || t;
                                return s("div", [e.isTicket && e.params.useCounterTemplate ? s("div", {
                                    ref: "body-wrapper",
                                    class: e.style["schedule__body-wrapper"],
                                    style: e.bodyStyle
                                }, [s("div", {
                                    staticClass: "px-[8px] mt-[8px]"
                                }, [e._l(e.viewRows, (function(t) {
                                    return [e._l(t, (function(t) {
                                        return [e.ifCounterShowCol(t) ? s("SpTicketCell", {
                                            key: t.key,
                                            staticClass: "ticket-cell",
                                            attrs: {
                                                value: t.orderInfo ? e.form[t.platformInfo.venueId][t.orderInfo.venueTicketId].value : 0,
                                                data: t,
                                                max: e.maxNum,
                                                highlight: !!t.orderInfo && e.form[t.platformInfo.venueId][t.orderInfo.venueTicketId].value > 0,
                                                disabled: e.ifCounterDisableCol(t),
                                                text: e.params.salesItem ? e.params.salesItem.salesItemName : null,
                                                "is-calc-mode": e.isCalcMode
                                            },
                                            on: {
                                                change: function(s) {
                                                    return e.onTicketChange(t, s)
                                                },
                                                timeChange: function(s) {
                                                    return e.onTimeChange(t, s)
                                                },
                                                popup: e.popupFun
                                            }
                                        }, [s("template", {
                                            slot: "msg"
                                        }, [s("ScheduleColMsg", {
                                            attrs: {
                                                col: t,
                                                "truthy-cls": e.truthyCls,
                                                "falsey-cls-list": e.falseyClsList,
                                                nbdtt: e.params.nextBtnDisText,
                                                nyott: e.notYetOpenTimeText,
                                                "is-ticket": e.isTicket,
                                                "is-reservation": e.isReservation,
                                                "is-calc-mode": e.isCalcMode,
                                                "is-no-book": e.isNoBook,
                                                "is-ticket-disabled": e.isTicketDisabled,
                                                "is-schedule-data-first": e.isScheduleDataFirst,
                                                "view-show": e.serverData.viewShow
                                            }
                                        })], 1)], 2) : e._e()]
                                    }))]
                                })), null == e.params.selectedSlotStartTime || null == e.serverData.timeSlotList || 0 === e.serverData.timeSlotList.length ? s("Card", {
                                    attrs: {
                                        invisible: ""
                                    }
                                }, [s("div", {
                                    staticClass: "list-empty text-center"
                                }, [e._v("暂无可选场次")])]) : e._e()], 2)]) : s("div", {
                                    staticClass: "schedule-table text-center",
                                    class: {
                                        "schedule-table-compact": 1 === e.columns.level1.length && e.columns.level2.length < 2
                                    }
                                }, [s("div", {
                                    ref: "hiddenColumns",
                                    staticClass: "schedule-table__hidden-columns"
                                }), s("div", {
                                    ref: "header-wrapper",
                                    class: e.style["schedule-table__header-wrapper"]
                                }, [e.columns.level1 && e.columns.level1.length > 0 ? s("table", {
                                    style: {
                                        width: e.tableWidth ? e.tableWidth + "px" : "100%"
                                    },
                                    attrs: {
                                        cellspacing: "0",
                                        cellpadding: "0",
                                        border: "0"
                                    }
                                }, [s("colgroup", [e._l(e.columns.level1, (function(t, i) {
                                    return s("col", {
                                        key: t.venueId,
                                        attrs: {
                                            span: t.subCount || 1,
                                            width: e.colWidth,
                                            name: "schedule-table_column_" + (i + 1)
                                        }
                                    })
                                })), s("col", {
                                    attrs: {
                                        span: 1,
                                        width: 0
                                    }
                                })], 2), s("thead", [e._l(e.columns, (function(t, i, a) {
                                    return [t.length > 0 ? s("tr", {
                                        key: i
                                    }, [e._l(t, (function(t) {
                                        return s("th", {
                                            key: t.venueId,
                                            attrs: {
                                                colspan: t.subCount || 1,
                                                rowspan: 0 == a && 0 == t.subCount && e.columns.level2 && e.columns.level2.length > 0 ? 2 : 1,
                                                "data-platform-id": t.venueId
                                            }
                                        }, [s("div", {
                                            class: e.style.tablecell
                                        }, [e._v(e._s(t.venueName))])])
                                    })), 0 == a ? s("th", {
                                        attrs: {
                                            colspan: 1,
                                            rowspan: e.columns.level2 && e.columns.level2.length > 0 ? 2 : 1,
                                            "data-platform-id": -1
                                        }
                                    }) : e._e()], 2) : e._e()]
                                }))], 2)]) : s("Card", {
                                    attrs: {
                                        invisible: ""
                                    }
                                }, [s("div", {
                                    staticClass: "list-empty text-center"
                                }, [e._v("暂无数据")])])], 1), s("div", {
                                    ref: "body-wrapper",
                                    class: e.style["schedule__body-wrapper"],
                                    style: e.bodyStyle
                                }, [s("table", {
                                    style: {
                                        width: e.tableWidth ? e.tableWidth + "px" : "100%"
                                    },
                                    attrs: {
                                        cellspacing: "0",
                                        cellpadding: "0",
                                        border: "0"
                                    }
                                }, [s("colgroup", [e._l(e.columns.level1, (function(t, i) {
                                    return s("col", {
                                        key: t.venueId,
                                        attrs: {
                                            span: t.subCount || 1,
                                            width: e.colWidth,
                                            name: "schedule-table_column_" + (i + 1)
                                        }
                                    })
                                })), s("col", {
                                    attrs: {
                                        span: 1,
                                        width: 0
                                    }
                                })], 2), s("tbody", [e._l(e.viewRows, (function(t, i) {
                                    return s("tr", {
                                        key: i
                                    }, [e._l(t, (function(t, i) {
                                        return [t ? s("td", {
                                            key: t.key,
                                            class: e.getColClassNames(t, i),
                                            style: e.getHotStyle(t),
                                            attrs: {
                                                colspan: t.colspan || 1,
                                                rowspan: t.rowspan || 1,
                                                "data-platform-id": t.platformInfo.venueId,
                                                "data-hot-id": t.hotTimeBean ? t.hotTimeBean.hotId : null
                                            },
                                            on: {
                                                click: function(s) {
                                                    return e.onSelect(t)
                                                }
                                            }
                                        }, [s("div", {
                                            class: e.style.tablecell
                                        }, [t.startTimeText || t.endTimeText ? [e._v(" " + e._s(t.startTimeText) + "-" + e._s(t.endTimeText) + " ")] : e._e(), s("ScheduleColMsg", {
                                            attrs: {
                                                col: t,
                                                "truthy-cls": e.truthyCls,
                                                "falsey-cls-list": e.falseyClsList,
                                                nbdtt: e.params.nextBtnDisText,
                                                nyott: e.notYetOpenTimeText,
                                                "is-ticket": e.isTicket,
                                                "is-calc-mode": e.isCalcMode,
                                                "is-reservation": e.isReservation,
                                                "is-no-book": e.isNoBook,
                                                "is-ticket-disabled": e.isTicketDisabled,
                                                "is-schedule-data-first": e.isScheduleDataFirst,
                                                "view-show": e.serverData.viewShow
                                            }
                                        }, [t.orderInfo && 1 === t.orderInfo.isFightDeal ? s("template", {
                                            slot: "fight"
                                        }, [s("div", {
                                            class: e.style["fight-request-ing"]
                                        }, [s("i", {
                                            staticClass: "icon-pt-team-fight"
                                        }), e._v(" 约战中 ")]), s("div", {
                                            class: e.style["fight-request"]
                                        }, [e._v("已约战")]), s("div", {
                                            class: e.style["fight-respond"]
                                        }, [e._v("已应战")])]) : e._e()], 2)], 2)]) : e._e()]
                                    })), s("td", {
                                        attrs: {
                                            "data-platform-id": -1
                                        }
                                    })], 2)
                                })), e.viewRows && e.viewRows.length > 0 ? s("tr", {
                                    class: e.style.alignmentRow
                                }, [e._l(e.viewRows[e.viewRows.length - 1], (function(e, t) {
                                    return s("td", {
                                        key: e ? e.key : t,
                                        attrs: {
                                            "data-platform-id": e ? e.platformInfo.venueId : -1
                                        }
                                    })
                                })), s("td", {
                                    attrs: {
                                        "data-platform-id": -1
                                    }
                                })], 2) : e.columns.level1.length > 0 ? s("tr", [s("td", {
                                    staticClass: "text-center",
                                    class: e.style["schedule-table__empty-text"],
                                    attrs: {
                                        colspan: e.colLength
                                    }
                                }, [e._v(" " + e._s(e.loading ? "加载中..." : e.serverData.platformCloseAlert || "此时段暂不开放") + " ")]), s("td", {
                                    attrs: {
                                        "data-platform-id": -1
                                    }
                                })]) : e._e()], 2)])]), s("van-dialog", {
                                    attrs: {
                                        "show-cancel-button": "",
                                        "close-on-click-overlay": "",
                                        "cancel-button-text": "关闭",
                                        "show-confirm-button": e.fightDialogState === e.fightStates.requestIng,
                                        "confirm-button-text": "我要应战"
                                    },
                                    on: {
                                        confirm: e.respondFight
                                    },
                                    model: {
                                        value: e.fightDialogShow,
                                        callback: function(t) {
                                            e.fightDialogShow = t
                                        },
                                        expression: "fightDialogShow"
                                    }
                                }, [e.fightDialogCol ? s("div", {
                                    staticClass: "text-left"
                                }, [s("img", {
                                    staticClass: "img-max",
                                    attrs: {
                                        src: e.CDN_STATIC_HOST + "/images/portal/fight/fight-bg.jpg"
                                    }
                                }), s("Card", [s("div", {
                                    staticClass: "inner-card",
                                    class: {
                                        vs: e.fightDialogState === e.fightStates.request || e.fightDialogState === e.fightStates.respond
                                    }
                                }, [s("van-row", [s("van-col", {
                                    staticClass: "text-right",
                                    attrs: {
                                        span: 8
                                    }
                                }, [e._v(" " + e._s(e.fightDialogState === e.fightStates.respond ? "应战" : "约战") + "队伍： ")]), s("van-col", {
                                    attrs: {
                                        span: 16
                                    }
                                }, [e._v(e._s(e.fightInfo.sportTeamName))])], 1), s("van-row", [s("van-col", {
                                    staticClass: "text-right",
                                    attrs: {
                                        span: 8
                                    }
                                }, [e._v(" 队服颜色： ")]), s("van-col", {
                                    attrs: {
                                        span: 16
                                    }
                                }, [e.fightInfo.sportTeamColorRgb ? s("span", {
                                    staticClass: "fight-color-wrapper"
                                }, [e._v(" " + e._s(e.fightInfo.fightColor) + " "), s("span", {
                                    style: {
                                        background: e.fightInfo.sportTeamColorRgb,
                                        borderColor: e.getFightBorderColor(e.fightInfo.sportTeamColorRgb)
                                    }
                                }, [e._v("   ")])]) : e._e()])], 1), s("van-row", [s("van-col", {
                                    staticClass: "text-right",
                                    attrs: {
                                        span: 8
                                    }
                                }, [e._v(" 球队水平： ")]), s("van-col", {
                                    attrs: {
                                        span: 16
                                    }
                                }, [e._v(" " + e._s(e.fightInfo.teamLevelName) + " ")])], 1), s("van-row", [s("van-col", {
                                    staticClass: "text-right",
                                    attrs: {
                                        span: 8
                                    }
                                }, [e._v(" 对手类型： ")]), s("van-col", {
                                    attrs: {
                                        span: 16
                                    }
                                }, [e._v(" " + e._s(e.fightInfo.opponentTypeName) + " ")])], 1), s("van-row", [s("van-col", {
                                    staticClass: "text-right",
                                    attrs: {
                                        span: 8
                                    }
                                }, [e._v(" " + e._s(e.fightDialogState === e.fightStates.respond ? "应战" : "约战") + "留言： ")]), s("van-col", {
                                    attrs: {
                                        span: 16
                                    }
                                }, [e._v(" " + e._s(e.fightInfo.fightDeclaration) + " ")])], 1), e.fightInfo.fightShowMobile ? [s("van-row", [s("van-col", {
                                    staticClass: "text-right",
                                    attrs: {
                                        span: 8
                                    }
                                }, [e._v(" 联系方式： ")]), s("van-col", {
                                    attrs: {
                                        span: 16
                                    }
                                }, [e._v(" " + e._s(e.fightInfo.fightShowMobile) + " ")])], 1)] : e._e(), s("div", {
                                    staticClass: "gap-row"
                                }, e._l(e.fightDialogUserCareerMapping, (function(t, i) {
                                    return s("van-row", {
                                        key: i
                                    }, [s("van-col", {
                                        staticClass: "text-right",
                                        attrs: {
                                            span: 8
                                        }
                                    }, [e._v(" " + e._s(e.formatCareer(+i)) + "： ")]), s("van-col", {
                                        attrs: {
                                            span: 16
                                        }
                                    }, [e._v(" " + e._s(t.map((function(e) {
                                        return e.realName
                                    })).join(", ")) + " ")])], 1)
                                })), 1), e.fightDialogBroCol ? [s("van-row", [s("van-col", {
                                    staticClass: "text-right",
                                    attrs: {
                                        span: 8
                                    }
                                }, [e._v(" " + e._s(e.getFightState(e.fightDialogBroCol) === e.fightStates.respond ? "应战" : "约战") + "队伍： ")]), s("van-col", {
                                    attrs: {
                                        span: 16
                                    }
                                }, [e._v(e._s(e.broFightInfo.sportTeamName))])], 1), s("van-row", [s("van-col", {
                                    staticClass: "text-right",
                                    attrs: {
                                        span: 8
                                    }
                                }, [e._v(" 队服颜色： ")]), s("van-col", {
                                    attrs: {
                                        span: 16
                                    }
                                }, [e.broFightInfo.sportTeamColorRgb ? s("span", {
                                    staticClass: "fight-color-wrapper"
                                }, [e._v(" " + e._s(e.broFightInfo.fightColor) + " "), s("span", {
                                    style: {
                                        background: e.broFightInfo.sportTeamColorRgb,
                                        borderColor: e.getFightBorderColor(e.broFightInfo.sportTeamColorRgb)
                                    }
                                }, [e._v("   ")])]) : e._e()])], 1), s("van-row", [s("van-col", {
                                    staticClass: "text-right",
                                    attrs: {
                                        span: 8
                                    }
                                }, [e._v(" " + e._s(e.getFightState(e.fightDialogBroCol) === e.fightStates.respond ? "应战" : "约战") + "留言： ")]), s("van-col", {
                                    attrs: {
                                        span: 16
                                    }
                                }, [e._v(" " + e._s(e.broFightInfo.fightDeclaration) + " ")])], 1), e.broFightInfo.fightShowMobile ? [s("van-row", [s("van-col", {
                                    staticClass: "text-right",
                                    attrs: {
                                        span: 8
                                    }
                                }, [e._v(" 联系方式： ")]), s("van-col", {
                                    attrs: {
                                        span: 16
                                    }
                                }, [e._v(" " + e._s(e.broFightInfo.fightShowMobile) + " ")])], 1)] : e._e()] : e._e()], 2)])], 1) : e._e()])], 1)])
                            },
                            u = [],
                            f = (s(46449),
                                s(74423),
                                s(26910),
                                s(93514),
                                s(13609),
                                s(62953),
                                s(60530)),
                            m = function() {
                                var e = this,
                                    t = e.$createElement,
                                    s = e._self._c || t;
                                return e.col ? s("span", [e.nbdtt ? [s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedAllFakeList
                                    }
                                }, [e._v(" " + e._s([e.showPrice && e.col.priceBean && (e.col.priceBean.price > 0 ? e.formatMoney(e.col.priceBean.price) + "元" : "免费")].join("/")) + " ")])] : e.col.platformInfo.onlineBooking !== e.OnlineBookingTypes.Open.key ? [s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedAllFakeList
                                    }
                                }, [e._v(" " + e._s(e.sellerMessage || e.closeMsg) + " ")])] : e.isScheduleDataFirst && e.col.className || !e.nyott ? e.col.orderInfo && !e.isTicket ? [1 === e.col.orderInfo.dealState ? [s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedAllFakeList
                                    }
                                }, [e._v(" 预订中 ")])] : 2 === e.col.orderInfo.dealState || 88 == e.col.orderInfo.dealState ? [s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedAllFakeList
                                    }
                                }, [e._v(" " + e._s(e.sellerMessage || "已预订") + " ")])] : e.col.orderInfo.lockId ? [s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedAllFakeList
                                    }
                                }, [e._v(" " + e._s(e.sellerMessage) + " ")])] : e._e(), e.col.orderInfo.dealServiceUserList ? [e.col.orderInfo.dealServiceUserList.some((function(t) {
                                    return t.careerId == e.Careers.SPORTS_TEACH.key
                                })) ? s("div", [e._v(" 教练：" + e._s(e.col.orderInfo.dealServiceUserList.filter((function(t) {
                                    return t.careerId == e.Careers.SPORTS_TEACH.key
                                })).map((function(e) {
                                    return e.realName
                                })).join(",")) + " ")]) : e._e(), e.col.orderInfo.dealServiceUserList.some((function(t) {
                                    return t.careerId == e.Careers.SPORTS_TRAINER.key
                                })) ? s("div", [e._v(" 裁判：" + e._s(e.col.orderInfo.dealServiceUserList.filter((function(t) {
                                    return t.careerId == e.Careers.SPORTS_TRAINER.key
                                })).map((function(e) {
                                    return e.realName
                                })).join(",")) + " ")]) : e._e()] : e._e(), e._t("fight")] : e.col.expired && !e.isTicket ? [s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedAllFakeList
                                    }
                                }, [e._v(" 已过期 ")])] : e.isNoBook(e.col) ? [s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedAllFakeList
                                    }
                                }, [e._v(" 已占用 ")])] : e.isTicketDisabled(e.col.orderInfo) ? [s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedAllFakeList
                                    }
                                }, [e._v(" " + e._s(e.sellerMessage || e.closeMsg) + " ")])] : [e.isReservation ? [s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedAllFakeList
                                    }
                                }, [e.isTicket ? [e._v(" " + e._s(e.col.orderInfo && e.col.orderInfo.surplusNum > 0 ? [e.showCanSell && "可约" + e.col.orderInfo.surplusNum, e.showSelled && "已约" + (e.col.orderInfo.salesNum || 0)].filter(Boolean).join("/") : "已约满") + " ")] : [e._v(" 可约 ")]], 2)] : [s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedList
                                    }
                                })], e.sellerMessage ? s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedAllFakeList
                                    }
                                }, [e._v(" " + e._s(e.sellerMessage) + " ")]) : e._e()] : [s("ScheduleColMsgObfuscated", {
                                    attrs: {
                                        "truthy-cls": e.truthyCls,
                                        list: e.randomObfuscatedAllFakeList
                                    }
                                }, [e._v(" " + e._s(e.nyott) + "开放预订 ")])]], 2) : e._e()
                            },
                            p = [],
                            g = s(6602),
                            b = s(89439),
                            v = s(25800),
                            T = function() {
                                var e = this,
                                    t = e.$createElement,
                                    s = e._self._c || t;
                                return s("div", [e._l(e.leftList, (function(t) {
                                    return s("span", {
                                        key: t.id,
                                        class: t.cls
                                    }, [e._v(" " + e._s(t.text) + " ")])
                                })), s("span", {
                                    class: e.truthyCls
                                }, [e._t("default", (function() {
                                    return [e._v(e._s(" "))]
                                }))], 2), e._l(e.rightList, (function(t) {
                                    return s("span", {
                                        key: t.id,
                                        class: t.cls
                                    }, [e._v(" " + e._s(t.text) + " ")])
                                }))], 2)
                            },
                            I = [];
                        const _ = {
                                props: {
                                    truthyCls: String,
                                    list: Array
                                },
                                computed: {
                                    shuffledList() {
                                        return [...this.list].sort((() => Math.random() - .5))
                                    },
                                    splitIndex() {
                                        return (0,
                                            v.KQ)(0, this.shuffledList.length)
                                    },
                                    leftList() {
                                        return this.shuffledList.slice(0, this.splitIndex)
                                    },
                                    rightList() {
                                        return this.shuffledList.slice(this.splitIndex)
                                    }
                                }
                            },
                            C = _;
                        var w = s(81656),
                            x = (0,
                                w.A)(C, T, I, !1, null, null, null);
                        const y = x.exports,
                            { Careers: S, OnlineBookingTypes: k } = g,
                            D = {
                                components: {
                                    ScheduleColMsgObfuscated: y
                                },
                                props: {
                                    col: Object,
                                    truthyCls: String,
                                    falseyClsList: Array,
                                    viewShow: Array,
                                    nyott: String,
                                    nbdtt: String,
                                    isTicket: Boolean,
                                    isReservation: Boolean,
                                    isScheduleDataFirst: Boolean,
                                    isCalcMode: Boolean,
                                    isNoBook: Function,
                                    isTicketDisabled: Function
                                },
                                data() {
                                    return {
                                        Careers: S,
                                        OnlineBookingTypes: k
                                    }
                                },
                                computed: {
                                    showPrice() {
                                        var e;
                                        return null === (e = this.viewShow) || void 0 === e ? void 0 : e.includes(1)
                                    },
                                    showCanSell() {
                                        var e;
                                        return null === (e = this.viewShow) || void 0 === e ? void 0 : e.includes(2)
                                    },
                                    showSelled() {
                                        var e;
                                        return null === (e = this.viewShow) || void 0 === e ? void 0 : e.includes(3)
                                    },
                                    showMinutes() {
                                        var e;
                                        const t = null === (e = this.col) || void 0 === e || null === (e = e.priceBean) || void 0 === e ? void 0 : e.calcTimeValue;
                                        return this.isCalcMode && t && this.isTicket ? `${(0,
                    b.y4)(t, 6e4)}分钟` : ""
                                    },
                                    fakePriceText() {
                                        const e = (0,
                                                v.W2)(1, 100, 3),
                                            t = ["已预订", `${e[0]}元`, ""],
                                            s = (0,
                                                v.KQ)(0, t.length),
                                            i = [t[s]];
                                        return this.isTicket && i.push(`可售${e[1]}`, `已售${e[2]}`),
                                            i.filter(Boolean).join("/")
                                    },
                                    truthyPriceText() {
                                        var e;
                                        const t = [this.showPrice && (null === (e = this.col) || void 0 === e ? void 0 : e.priceBean) && `${this.showMinutes}${this.col.priceBean.price > 0 ? `${this.formatMoney(this.col.priceBean.price)}元` : "免费"}`];
                    var s, i, a;
                    this.isTicket && t.push((null === (s = this.col) || void 0 === s ? void 0 : s.orderInfo) && this.showCanSell && `可售${this.col.orderInfo.surplusNum || 0}`, (null === (i = this.col) || void 0 === i ? void 0 : i.orderInfo) && this.showSelled && `已售${this.col.orderInfo.salesNum || 0}`, !(null !== (a = this.col) && void 0 !== a && a.orderInfo) && "无票");
                    return t.filter(Boolean).join("/")
                },
                randomFakePriceList() {
                    return this.falseyClsList.map(( (e, t) => ({
                        id: t,
                        cls: e,
                        text: this.fakePriceText
                    })))
                },
                randomObfuscatedList() {
                    const e = [...this.randomFakePriceList]
                      , t = (0,
                    v.KQ)(0, e.length + 1);
                    return e.splice(t, 0, {
                        id: e.length + 1,
                        cls: this.truthyCls,
                        text: this.truthyPriceText
                    }),
                    e
                },
                randomObfuscatedAllFakeList() {
                    const e = [...this.randomFakePriceList]
                      , t = (0,
                    v.KQ)(0, e.length + 1)
                      , s = e[(0,
                    v.KQ)(0, e.length)];
                    return e.splice(t, 0, {
                        id: e.length + 1,
                        cls: s.cls,
                        text: this.truthyPriceText
                    }),
                    e
                },
                sellerMessage() {
                    var e;
                    return null === (e = this.col) || void 0 === e || null === (e = e.orderInfo) || void 0 === e ? void 0 : e.sellerMessage
                },
                closeMsg() {
                    return null == this.col ? null : this.col.platformInfo.platformCloseAlert || "仅支持线下预订"
                }
            }
        }
          , L = D;
        var F = (0,
        w.A)(L, m, p, !1, null, null, null);
        const $ = F.exports;
        var B = s(79735)
          , A = s(94171)
          , N = s(9805)
          , O = (s(16280),
        s(33110),
        s(17642),
        s(58004),
        s(33853),
        s(45876),
        s(32475),
        s(15024),
        s(31698),
        s(74353))
          , M = s.n(O)
          , P = s(64880);
        const R = {
            Platform: {
                key: 0,
                value: "场地"
            },
            ForeverRange: {
                key: 1,
                value: "固定场"
            },
            Course: {
                key: 2,
                value: "课程占场"
            },
            Locked: {
                key: 3,
                value: "锁场"
            },
            Change: {
                key: 4,
                value: "换场"
            }
        };
        var H = s(24062)
          , q = s(78870);
        const {ProfessionalTypes: E, SalesStates: U, OnlineBookingTypes: V, HourCancelTypes: j, FightTypes: W} = g
          , {F2: z} = i;
        function G(e, t) {
            if (null != e && (e.push(t),
            t && t.colspan > 1))
                for (let s = 1; s < t.colspan; s++)
                    e.push(null)
        }
        const Q = "Locked-"
          , Y = {
            1: "col-inprocess",
            2: "col-scheduled",
            88: "col-completed"
        }
          , K = {
            mixins: [P.A],
            data() {
                return {
                    atomic: 1,
                    loading: !1,
                    serverData: {
                        sportPlatformList: [],
                        sportPlatformPriceList: [],
                        sportPlatformHotBookingTimeList: [],
                        timeSlotList: [],
                        orderInfoList: [],
                        fightList: []
                    },
                    selectedCols: []
                }
            },
            computed: {
                scheduleLoadFlag() {
                    const {salesId: e, venueGroupId: t, dateTime: s, salesItem: i} = this.params
                      , {salesItemId: a} = i || {};
                    return `${e || 0}-${a || 0}-${t || 0}-${s || 0}-${this.atomic}`
                },
                isTicket() {
                    const {salesItem: e} = this.params;
                    return (null === e || void 0 === e ? void 0 : e.itemType) === E.Ticket.key
                },
                columns() {
                    let e = [];
                    const t = {
                        level1: [],
                        level2: []
                    }
                      , {sportPlatformList: s} = this.serverData
                      , i = s || [];
                    return i.forEach((s => {
                        0 === s.parentId ? t.level1.push(s) : e.push(s)
                    }
                    )),
                    t.level1.forEach((s => {
                        const i = [];
                        s.subCount = 0,
                        e.forEach((function(e) {
                            e.parentId === s.venueId ? (e.parentVenueName = s.venueName,
                            s.subCount++,
                            t.level2.push(e)) : i.push(e)
                        }
                        )),
                        e = i
                    }
                    )),
                    t
                },
                platformInColumns() {
                    const e = [];
                    let t = 0;
                    return this.columns.level1.forEach((s => {
                        if (0 === s.subCount) {
                            const {parentId: t, subCount: i, ...a} = s;
                            e.push({
                                ...a,
                                parentId: t,
                                brother: 1
                            })
                        } else
                            for (let i = 0; i < s.subCount; i++) {
                                const {parentId: i, subCount: a, ...r} = this.columns.level2[t++];
                                e.push({
                                    ...r,
                                    parentId: i,
                                    parentVenueName: s.venueName,
                                    parentVenuePriceId: s.venuePriceId,
                                    brother: s.subCount
                                })
                            }
                    }
                    )),
                    e
                },
                rows() {
                    const {orderInfoList: e, timeSlotList: t} = this.serverData
                      , s = t || []
                      , i = e || []
                      , a = [];
                    return s.forEach(( (e, t) => {
                        const r = []
                          , l = i.filter((t => t.startTime <= e.startTime && t.endTime >= e.endTime));
                        this.columns.level1.forEach((e => {
                            const i = l.filter((t => {
                                if (t.venueId === e.venueId)
                                    return !0;
                                const s = this.filterPlatformSubIds(t.platformSubIds);
                                return (null == s || 0 === s.length) && this.columns.level2.some((s => s.parentId === e.venueId && s.venueId === t.venueId))
                            }
                            ));
                            if (e.subCount > 0) {
                                const l = [];
                                this.columns.level2.filter((t => t.parentId === e.venueId)).forEach((e => {
                                    if (l.includes(e.venueId.toString()))
                                        return;
                                    const n = i.find((t => {
                                        if (t.venueId === e.venueId)
                                            return !0;
                                        if (this.isTicket)
                                            return !0;
                                        const s = this.filterPlatformSubIds(t.platformSubIds);
                                        return !!s && s.includes(e.venueId.toString())
                                    }
                                    ))
                                      , o = l.length;
                                    if (n) {
                                        const e = this.filterPlatformSubIds(n.platformSubIds);
                                        e && e.length > 0 ? l.push(...e) : l.push(n.venueId.toString())
                                    }
                                    const c = l.length - o;
                                    G(r, this.buildCol(a, n, s, t, r.length, Math.max(c, 1)))
                                }
                                ))
                            } else
                                G(r, this.buildCol(a, i[0], s, t, r.length))
                        }
                        )),
                        a.push(r)
                    }
                    )),
                    a
                },
                viewRows() {
                    const {timeSlotList: e, sessionEnd: t} = this.serverData
                      , {nextBtnDisText: s} = this.params
                      , i = e || []
                      , a = this.currentServerTime;
                    return this.rows.map(( (e, r) => e.map(( (e, l) => {
                        const n = this.platformInColumns[l];
                        return n.onlineBooking !== V.Open.key || this.notYetOpenTimeText && !this.isScheduleDataFirst || s ? this.buildCol(null, null, i, r, l) : (e && (e.expired = e.endTime <= a || t > 0 && e.endTime - t <= a),
                        e)
                    }
                    ))))
                },
                notYetOpenTimeText() {
                    const {bookStartTime: e} = this.serverData;
                    if (e) {
                        const t = this.currentServerTime;
                        if (t && e > t) {
                            const t = M().tz(e);
                            return t.format("MM/DD HH:mm")
                        }
                    }
                    return null
                }
            },
            watch: {
                rows() {
                    this.selectedCols.splice(0, this.selectedCols.length)
                }
            },
            methods: {
                initReload() {
                    this.atomic++
                },
                async loadSchaduleServerData(e) {
                    const {venueGroupId: t, dateTime: s, salesItem: i} = this.params
                      , {salesItemId: a} = i || {};
                    if (this.serverData = {},
                    !s || !a)
                        return;
                    const r = {
                        salesItemId: a,
                        curDate: s,
                        venueGroupId: t
                    };
                    let l;
                    this.loading = !0,
                    (0,
                    H.z)({
                        action: "scheduleTableLoad",
                        message: JSON.stringify(r)
                    });
                    try {
                        l = await Promise.all([this.$http.get("/pub/sport/venue/getSportVenueConfig", r), this.isTicket ? this.$http.get("/pub/sport/venue/getVenueTicketList", r) : this.$http.get("/pub/sport/venue/getVenueOrderList", r)])
                    } finally {
                        this.loading = !1
                    }
                    const n = l[0] || {}
                      , {venueTimeSlotResponses: o, venueResponses: c, venueHotBookingTimeResponses: d, venuePriceResponses: h, ...u} = n
                      , f = {
                        ...u,
                        timeSlotList: o,
                        sportPlatformList: c,
                        sportPlatformHotBookingTimeList: null === d || void 0 === d ? void 0 : d.map((e => ({
                            ...e,
                            color: `#${(0,
                            v.W2)(0, 15, 6, !0).map((e => e.toString(16))).join("")}`
                        }))),
                        sportPlatformPriceList: h
                    }
                      , m = l[1] || [];
                    if (this.isTicket)
                        f.orderInfoList = m;
                    else {
                        var p;
                        const e = Object.keys(Y)
                          , t = null === (p = f.sportPlatformList) || void 0 === p ? void 0 : p.filter((e => e.onlineBooking !== V.Open.key && (e.parentId > 0 || !f.sportPlatformList.some((t => t.parentId === e.venueId)))));
                        f.orderInfoList = m.reduce(( (s, i) => {
                            var a;
                            if (!(i.dealPlatformType === z.Locked.key || i.dealState && e.includes(i.dealState.toString())))
                                return s;
                            if (null !== t && void 0 !== t && t.some((e => e.venueId === i.venueId)))
                                return s;
                            i.dealPlatformType === z.Locked.key && (i.dealId = `${Q}${i.lockId}`);
                            const r = null === (a = i.platformSubIds) || void 0 === a ? void 0 : a.split(",").map((e => +e)).filter(Boolean);
                            if ((null === t || void 0 === t ? void 0 : t.length) > 0 && (null === r || void 0 === r ? void 0 : r.length) > 0) {
                                const e = t.filter((e => null === r || void 0 === r ? void 0 : r.includes(e.venueId)));
                                if (e.length > 0) {
                                    r.sort(( (e, t) => {
                                        const s = f.sportPlatformList.findIndex((t => t.venueId === e))
                                          , i = f.sportPlatformList.findIndex((e => e.venueId === t));
                                        return s - i || 0
                                    }
                                    ));
                                    const t = e.map((e => r.indexOf(e.venueId)))
                                      , a = [];
                                    let l = 0;
                                    for (let e = 0; e < r.length; e++) {
                                        const s = t[0];
                                        if (e === s || null == s) {
                                            const e = r.slice(l, s);
                                            e.length > 0 && a.push({
                                                ...i,
                                                platformSubIds: e.join(",")
                                            }),
                                            l = s + 1,
                                            t.shift()
                                        }
                                    }
                                    return [...s, ...a]
                                }
                            }
                            const l = m.find((e => e.createTime !== i.createTime && e.startTime < i.endTime && e.endTime > i.startTime && ((null === r || void 0 === r ? void 0 : r.includes(e.venueId)) || e.venueId === i.venueId)));
                            if (l) {
                                const e = [];
                                return null !== r && void 0 !== r && r.includes(l.venueId) ? r.forEach((t => {
                                    const s = {
                                        ...i,
                                        venueId: t,
                                        platformSubIds: ""
                                    }
                                      , a = m.find((e => e.startTime < i.endTime && e.endTime > i.startTime && e.venueId === t));
                                    a ? o.forEach((t => {
                                        t.startTime >= i.startTime && t.endTime <= i.endTime && e.push({
                                            ...s,
                                            startTime: t.startTime,
                                            endTime: t.endTime
                                        })
                                    }
                                    )) : e.push(s)
                                }
                                )) : o.forEach((t => {
                                    t.startTime >= i.startTime && t.endTime <= i.endTime && e.push({
                                        ...i,
                                        startTime: t.startTime,
                                        endTime: t.endTime
                                    })
                                }
                                )),
                                [...s, ...e]
                            }
                            return [...s, i]
                        }
                        ), [])
                    }
                    this.serverData = f || {},
                    this.loadFightInfo(),
                    "function" === typeof e && e()
                },
                loadFightInfo() {
                    if (this.isTicket)
                        return;
                    const e = this.serverData.orderInfoList.filter((e => null === e || void 0 === e ? void 0 : e.isFightDeal)).map((e => e.dealPlatformId));
                    e.length > 0 && this.$http.postJSON("/pub/member/fight/party/list", {
                        dealPlatformIds: e
                    }).then((e => {
                        this.serverData.fightList = e || []
                    }
                    ))
                },
                async check() {
                    if (this.notYetOpenTimeText)
                        throw B.A.alert("未到开放预订"),
                        new Error("check failed.");
                    if (0 === this.selectedCols.length)
                        throw B.A.alert("请先选择场地."),
                        new Error("check failed.");
                    const {ticketOrderBuyNum: e, maxBookingPiece: t, maxBookTime: s, singleMinBookTime: i, ticketDayMaxBuyNum: a, ticketOrderMaxBuyNum: r, orderInfoList: l, sportPlatformList: n, cancelOrderNotes: o} = this.serverData
                      , {hourCancel: c, cancelBooking: d, hourCancelType: h} = this.params.salesItem || {}
                      , u = new Set
                      , f = new Set;
                    if (this.selectedCols.forEach((e => {
                        const {platformInfo: {venueId: t, remark: s}} = e;
                        t && f.has(t) || (f.add(t),
                        s && u.add(s))
                    }
                    )),
                    t > 0 && f.size > t)
                        throw B.A.alert(`最大可预订 ${t} 个${this.isTicket ? "票面" : "场地"}，请取消部分后再试`),
                        new Error("check failed.");
                    if (this.isTicket) {
                        if (e > 0 && this.selectedCols.length > e)
                            throw B.A.alert(`最大可预订 ${e} 个场次 ，请取消部分后再试`),
                            new Error("check failed.");
                        const t = a > 0 && r > 0 ? Math.min(a, r) : Math.max(a || 0, r || 0, 0);
                        if (t > 0 && this.selectedCols.length > t)
                            throw B.A.alert(`每单限购 ${t} 张票`),
                            new Error("check failed.")
                    }
                    if (s) {
                        const e = []
                          , t = this.selectedCols.reduce(( (t, s) => {
                            const {platformInfo: {parentId: i, brother: a}, rowIndex: r, endTime: l, startTime: n} = s;
                            if (e.some(( ({parentId: e, rowIndex: t}) => e === i && t === r)))
                                return t;
                            if (a > 1) {
                                const t = this.selectedCols.filter(( ({platformInfo: {parentId: e}, rowIndex: t}) => i === e && t === r));
                                t.length === a && e.push(...t.map(( ({platformInfo: {parentId: e}, rowIndex: t}) => ({
                                    parentId: e,
                                    rowIndex: t
                                }))))
                            }
                            return t + (l - n)
                        }
                        ), 0);
                        if (t > s)
                            throw B.A.alert(`您选择的时段，已超过最大可预订（${this.formatTimeDuration(s)}）限制，请取消部分后再试;`),
                            new Error("check failed.")
                    }
                    if (this.selectedCols.filter((e => {
                        var t;
                        return null === (t = e.hotTimeBean) || void 0 === t ? void 0 : t.vaildMinBookingTime
                    }
                    )).some((e => {
                        const t = this.isUnBrokenHotTime(e);
                        if (!t) {
                            const t = this.getHotTimeSeriesCols(e)
                              , {hotTimeBean: {singleMinBookTime: s, startTime: i, endTime: a}, platformInfo: {parentVenueName: r, venueName: l}} = e;
                            if (t.reduce(( (e, t) => this.selectedCols.includes(t) ? e + (t.endTime - t.startTime) : e), 0) < s)
                                return B.A.alert(`${r || ""}${r ? "-" : ""}${l}此时段${this.formatHM(i)}-${this.formatHM(a)}起步预订需要${(0,
                                b.y4)(s, 6e4)}分钟`),
                                !0
                        }
                        return !1
                    }
                    )))
                        throw new Error("check failed.");
                    if (i) {
                        const e = [...this.selectedCols].sort(( (e, t) => e.colIndex < t.colIndex ? -1 : e.colIndex > t.colIndex ? 1 : e.rowIndex - t.rowIndex));
                        let t = 0;
                        if (e.some(( (s, a) => {
                            t += s.endTime - s.startTime;
                            const r = e[a + 1];
                            if (null == r || r.colIndex !== s.colIndex || r.startTime !== s.endTime) {
                                if (t < i) {
                                    var l, n;
                                    if (this.isUnBrokenHotTime(s))
                                        return !1;
                                    const t = s;
                                    let r = t
                                      , o = a;
                                    do {
                                        const s = e[o - 1];
                                        if (null == s || s.colIndex !== t.colIndex || s.endTime !== r.startTime)
                                            break;
                                        r = s,
                                        o--
                                    } while (1);
                                    if (r && this.isAvailable(null === (l = this.rows[r.rowIndex - 1]) || void 0 === l ? void 0 : l[r.colIndex], r) || t && this.isAvailable(null === (n = this.rows[t.rowIndex + 1]) || void 0 === n ? void 0 : n[t.colIndex], t)) {
                                        const {platformInfo: {parentVenueName: e, venueName: s}} = t;
                                        return B.A.alert(`${e || ""}${e ? "-" : ""}${s}单个场地每个已选的连续时间段起步预订需要${(0,
                                        b.y4)(i, 6e4)}分钟`),
                                        !0
                                    }
                                }
                                t = 0
                            }
                            return !1
                        }
                        )))
                            throw new Error("check failed.")
                    }
                    d || await B.A.confirm("您选择场次下单成功后不可退、换，请谨慎下单！确认继续？");
                    const m = this.selectedCols.sort(( (e, t) => e.startTime - t.startTime))[0]
                      , p = m.startTime - this.currentServerTime;
                    p < 0 && await B.A.confirm("您选择的场次时段已开场，若下单成功后，不可退、换，请谨慎下单！确认继续？");
                    const g = h === j.Start.key
                      , v = g ? p : m.endTime - this.currentServerTime;
                    if (v > 0 && v < c) {
                        const e = this.formatTimeDuration(c)
                          , t = `您选择的场次时段，离${g ? "开始" : "结束"}时间已不足${e}，若下单成功，不可退、换、更改，请谨慎下单！确认继续？`;
                        await B.A.confirm(t)
                    }
                    if (o && 0 === c && await B.A.confirm(o),
                    u.size > 0)
                        for (const b of u)
                            await B.A.confirm(b);
                    if (!this.isTicket && this.selectedCols.length > 1) {
                        const e = [];
                        l.forEach((t => {
                            if (t.isFightDeal === W.Required.key) {
                                const s = n.find((e => e.venueId === t.venueId && e.parentId > 0));
                                s && e.push({
                                    ...t,
                                    parentId: s.parentId
                                })
                            }
                        }
                        ));
                        let t = !1;
                        const s = [...this.selectedCols].sort(( (e, t) => e.rowIndex - t.rowIndex));
                        let i = !1
                          , a = !1;
                        const r = s.some(( (r, l) => {
                            var n;
                            const o = null === (n = r.platformInfo) || void 0 === n ? void 0 : n.parentId
                              , c = e.findIndex((e => e.parentId === o && r._startTime >= e.startTime && r._endTime <= e.endTime));
                            if (-1 === c) {
                                if (!a) {
                                    const t = e.findIndex((e => e.parentId === o && (r._startTime < e.startTime || r._endTime > e.endTime)));
                                    -1 !== t && (a = !0)
                                }
                            } else
                                i = !0;
                            return !t && o && (t = !0),
                            !(!(l > 0 && t) || r.colIndex === s[l - 1].colIndex && r.rowIndex === s[l - 1].rowIndex + 1)
                        }
                        ))
                          , o = "您选择的场地存在约战规则，不支持选择半场时，场地和场次间隔下单，请分开或连续选择后再下单！";
                        if (r) {
                            const e = s.some((e => {
                                var t;
                                const s = null === (t = e.platformInfo) || void 0 === t ? void 0 : t.parentId
                                  , i = n.filter((e => e.parentId === s))
                                  , a = this.selectedCols.filter((t => {
                                    var i;
                                    return s === (null === (i = t.platformInfo) || void 0 === i ? void 0 : i.parentId) && t.startTime === e.startTime && t.endTime === e.endTime
                                }
                                )).length;
                                return !(a === i.length || !s || !i[0].fight)
                            }
                            ));
                            if (e)
                                throw B.A.alert(o),
                                new Error("check failed.")
                        }
                        if (i && a)
                            throw B.A.alert(o),
                            new Error("check failed.")
                    }
                },
                isTicketDisabled(e) {
                    return this.isTicket && (null == e || e.salesState !== U.Unlimit.key)
                },
                isNoBook(e) {
                    if (e.noBook)
                        return !0;
                    const t = e.platformInfo.platformShareIds;
                    return !!(Array.isArray(t) && t.length > 0) && this.selectedCols.some(( ({rowIndex: s, platformInfo: {venueId: i}}) => s === e.rowIndex && t.includes(i)))
                },
                getHotTimeSeriesCols(e) {
                    if (null == e)
                        return null;
                    const {hotTimeBean: t, colIndex: s} = e;
                    if (null == t)
                        return null;
                    const {timeSlotList: i} = this.serverData
                      , a = i || [];
                    let r = -1
                      , l = -1;
                    const n = [];
                    return a.some(( (e, s) => (r < 0 && e.startTime === t.startTime && (r = s),
                    l < 0 && e.endTime === t.endTime && (l = s),
                    r >= 0 && n.push(this.rows[s]),
                    l >= 0))),
                    n.map((e => e[s]))
                },
                isUnBrokenHotTime(e, t=!0) {
                    if (this.isTicket)
                        return !1;
                    const s = this.getHotTimeSeriesCols(e);
                    return null != s && 0 !== s.length && s.every((e => !(null == e || !t && e.expired || null == e.priceBean || this.isNoBook(e) || e.platformInfo.onlineBooking !== V.Open.key || this.notYetOpenTimeText || e.className || e.rowspan > 1 || e.colspan > 1)))
                },
                isAvailableStatic(e) {
                    return !(null == e || e.expired || null == e.priceBean || this.isNoBook(e) || e.platformInfo.onlineBooking !== V.Open.key || this.notYetOpenTimeText || e.className || e.freeRange || e.rowspan > 1 || e.colspan > 1)
                },
                isAvailable(e) {
                    return !(!this.isAvailableStatic(e) || this.selectedCols.includes(e)) && (!!this.isTicket || null == e.orderInfo)
                },
                getHotTime(e, t) {
                    if (null == e || null == t || !(t.hotTimeId > 0))
                        return null;
                    const {sportPlatformHotBookingTimeList: s} = this.serverData
                      , i = s || [];
                    return i.find((s => s.hotId === t.hotTimeId && s.startTime <= e.startTime && s.endTime >= e.endTime))
                },
                getPriceConfig(e, t) {
                    if (null == e || null == t)
                        return {};
                    const {venuePriceId: s, parentVenuePriceId: i} = t
                      , {sportPlatformPriceList: a} = this.serverData
                      , r = a || [];
                    let l, n;
                    return r.some((t => (t.startTime <= e.startTime && t.endTime >= e.endTime && (t.priceId === s && (l = t),
                    t.priceId === i && (n = t)),
                    !(!l || !n)))),
                    l ? {
                        priceBean: l,
                        parentPriceBean: n
                    } : {}
                },
                filterPlatformSubIds(e) {
                    const {sportPlatformList: t} = this.serverData
                      , s = t || []
                      , i = null === e || void 0 === e ? void 0 : e.split(",").filter((e => {
                        const t = +e;
                        return t > 0 && s.some((e => e.venueId === t))
                    }
                    ));
                    return i
                },
                buildCol(e, t, s, i, a, r=1) {
                    var l;
                    let n = 1;
                    if (e) {
                        const l = e.filter(( (e, t) => t < i)).some(( (e, t) => {
                            const s = e[a];
                            return null != s && s.rowspan + t - i > 0
                        }
                        ));
                        if (l)
                            return null;
                        if (r < 2 && t) {
                            let e = i;
                            while (1) {
                                const i = s[e + 1];
                                if (null == i)
                                    break;
                                i.endTime <= t.endTime && n++,
                                e++
                            }
                        }
                    }
                    const o = s[i]
                      , c = this.platformInColumns[a]
                      , {priceBean: d, parentPriceBean: h} = this.getPriceConfig(o, c)
                      , u = this.getHotTime(o, c)
                      , f = this.isTicketDisabled(t)
                      , m = !f && t && t.surplusNum <= 0
                      , {dateTime: p, nextBtnDisText: g, salesItem: b} = this.params
                      , {salesItemId: T} = b || {}
                      , I = [];
                    g && I.push("col-booking-disabled");
                    const _ = [];
                    if ((null === (l = this.columns.level2) || void 0 === l ? void 0 : l.length) > 0 && this.platformInColumns.forEach(( (e, t) => {
                        e.parentId === c.parentId && e.venueId !== c.venueId && _.push(t)
                    }
                    )),
                    t) {
                        const e = Y[t.dealState];
                        e && I.push(e),
                        t.dealPlatformType === z.Locked.key && I.push("col-locked")
                    }
                    f && I.push("col-ticket-disabled"),
                    m && I.push("col-ticket-empty");
                    const {startTime: C, endTime: w, viewType: x, shareIds: y} = o;
                    let S = C
                      , k = w;
                    var D;
                    t && (S = t.startTime,
                    k = t.endTime,
                    t.dealPlatformType !== z.Platform.key && (S = C,
                    k = (null === (D = s[i + n - 1]) || void 0 === D ? void 0 : D.endTime) || t.endTime));
                    return {
                        key: `${T}-${p}-${i}-${a}`,
                        rowIndex: i,
                        colIndex: a,
                        _startTime: S,
                        _endTime: k,
                        startTime: (0,
                        v.T$)(p, S),
                        endTime: (0,
                        v.T$)(p, k, !0),
                        startTimeText: (0,
                        q.$X)(S),
                        endTimeText: (0,
                        q.L3)(k),
                        priceBean: d,
                        parentPriceBean: h,
                        hotTimeBean: u,
                        colspan: r,
                        rowspan: n,
                        freeRange: 2 === x,
                        platformInfo: c,
                        orderInfo: t,
                        className: I.join(" "),
                        noBook: null === y || void 0 === y ? void 0 : y.includes(c.venueId),
                        broColIdxList: _
                    }
                }
            }
        };
        var J = s(70607);
        const X = {
            "schedule-table__header-wrapper": "_a0c19560409312b7d27bdb209f0e3243 _4e63bc29a9684aa9125eb7a6a8289259 _cc3e71b1ebcd8b8d8873fb9f044f4d2f _1f7a3d10aa14cbe92c9d3975453ea9b2 _267f2d5a9f7a7b9dbbb1508c33ad0b2b _cbcd665f13c8aca0ec3cc16d0901cf27 _f08b7982229c6d32f4abf8441a9136e6 _7aeb4ebd5cc2eb9e3306522ae9bf3c34 _a2d2095348a5e8eb53a8252d32f2c3a8 _e7d9bdc0b34b485aef3af7625429a4cd _a465f69ab68a536984e96310aff2bdeb _6934f571c79ea77e515fe237f9434326 _081013fb8041b026b3f42d3ca99fea4e _bd2cae3aafc3926f5718f8a417c8aba9 _3161c42586a65ff82bf8602b23672b45 _dfbccbce5acb8a52af7514bf6b1c7603 _f7b3ae97e1fdbbd2fdcc85d7dfedcaaa _6e26f506e7117543e416e9b6661d4eb5 _c02e0366a44cecd8af7c48e132cd4340 _218b5757405309981d31916332d8ab47 _7855529dbebd5e9562dfb9e96f09df2e _2c3c50fd201963ebb1f3c6f93b6ef93a _cb9b18abb075037192e0d3022c4d50a6 _ab3b322c84a7c329c75fdc70bc4ed917 _3a26e01a1ce7eac7ea2909a55f2c37f6 _6214b91cfaf80e993475f6d87b69dc80 _dbe7cdc1419327bf7689d3af3304ea55",
            "schedule__body-wrapper": "_e6c982b1840bee804ab03922d22a1dbc _fca84323ff189db44dccc013dea1917f _25bf80c6914a8fcc7dcc7f6448b0bb41 _c72ce7fcb736e19e6839dea3f09dbb9e _877a0b5950120df644a5dd96d54c4028 _97fbd526e89263d3046ceeab54413a89 _c86787009f55998f130a546b33ba3654 _fcddf7e7eb2482a71bc28ae05bcd47f5 _c1780e881e56e2fc1ea4e63a88cc1e8f _db55790adceaf50da9fd74a5ca5ee9a8 _3b6718d8cd6b816fc800fe5948b85274 _fc96b1f778cb02681881be8e351e2516 _095dbe07b854b4a22da1df9af5526f0a _c6f328ea922555500a2144900802b6ad _406aa6bc9659f10df5171b06568475cb _43c137fab2a2553891e3acbf62c0cfda _184df8871bb7a0d3899362d238010994 _0892d83ac79b383338d98a043ac988dd _7b5de43a7065693d5acdca449ffada74 _e0cf178644a679cf3384f123a933c57c _e7107c6b8a2db787b929e52e8b163d43 _5df96eea7feedf249914b106ba934bb8 _16f4afa34c6076f5cc3e6b544c319b72 _e369930e723f9988464befbd6fc18814 _fcec24410954cdddf33b8145cb4ce0a7 _c8b2546a2bc53ab5a6b8ced5893f5aaa _31681ae2bbad31d854652d70e3563479 _f76060eeffedc6bf64436f900433fe67",
            alignmentRow: "_f2a44dd63bd79599f9ac51d56060b2bb _d6629250e884566005ab8725874a2261 _029bc5f353f52498082e1c7fae254dd5 _01d51d9e653fcced3fc3f042caa4be33 _cc6484dcce29b03f7d18638e9e06de08 _19514bd4867744d78ce697a5a636f1cf _9ea1729396ed90de1458f86df215b5a3 _6b92eb22ec83cd13a8e8737af533ad95 _6d224fe669321319b7e536f9c9b2b70b _1787c759b41ac7cd70382663825dbe24 _0b4bcbef1c17661a07ee6d6256d5ddad _1643a6c5775628ebf01777cb4e8f2291 _91c4fc5c856c69ecd02a32d936356097 _a31eda2c708033bb4f87463544e6df96 _93530321f06120522c6316170cf7d8ba _aadc4c774fd9ac27e7cbd6c0a5a0e9e7 _3cc1d4f40f030d194d1f4cc00d87c889 _3d2d5d57bc3c1c78341690665986f93b _c0d4d0740842c9818df9f97cebcf30e6 _4a582194a9d113e684b10aa0cbec9445 _244cc36f18e9adbf6aa312ea41c70585 _c5030c6f031733ec74e579cbcd5f4a00 _600cd1a66c39b57e5b8f3b4637275899 _05e5f9f72e4e1642eccd2053085eeed9 _138cc0e287bf0489570a77f1921767d0 _e58ca84155a13292aee745108714f3fe _101885df8b438ce30c1ae52b1bda3d19 _108b0dac37bb4e51a47c5440bd2e3fa6 _5f965b9c9aa9cd8cbc3bde8c2c458546 _54091323e4d9154766942638933f8c05 _bb4646d3a3c9aa9f40383381c7370d85 _d83ee01fe5d565a3a840e19b417800a6 _8ab1b7ac86f07610db09efaab5163c80 _2924888fa1fa09f575c8f7ba10bb5549 _921265a5619b65071a9a6a4e0b833b8b _7fa94f05017c4cb9d106d3b232f36752 _109e969545ba6ef738fbb031f538aa86 _6f80ec00cfa043f384eff1eb09032425 _fd2b749cbd8f9b2a5271b55143f2000b _5085f9c9c340df73f57847a367dd4621 _7096a858bbc94064c80b05ef7d21118d _c0f439188250bf2e2fd0364e0e9dd1e8 _87658b34d98a7012a63df58b74dcb479 _1b4688c0ebd2720a88cbc9b234653772 _7dc0c464d9790197bbf3c38a5a2e868d _87df6976d00d5cf93185d907f1f11003 _709eeb4d0078b6e8b6458a7e5b3e74fe _23a69329ac293d255066e548b3989c56",
            tablecell: "_faf5eee53577af3e233e9a6443e285ab _01b8be73576c8a0373d8cfc8fa2f9ce4 _6d033b5230e1cc54da6fa2e1bfd5e7eb _01ed6697c6ecb636746cd34b74a73e21 _f9e3e59222f4955c1cc78516c8831b9b _4116d2ad5d75a58edd25e745d05d9749",
            expired: "_c9f7acc456f0f4f16fb5fdc1cc7f875a _5515c0d960ea21ab4337bb5965263cc9",
            noBook: "_e48b3a8d221e9c3abf9ca211220eb8f3 _4c8322acc04043d74940049e4adf5849",
            "col-booking-disabled": "_046219dc22d40de1c4c87be0867a99c2 _9261f67b8ed1730d194ce25205c5c542",
            "col-ticket-empty": "_b5a3e26ad4b89f96af5673c011d79077 _6d91d895d6e2fe904acc3d4c0e9014bf",
            "col-ticket-disabled": "_4b81c009993d6aaf2aa9d834b6d42ce6 _452ac05951d4d07ca984df826e34ea2a",
            "col-inprocess": "_cb1bd6df0378bbc592d8851ceb17f102 _421262fe10211511811b10778cf292e9",
            "col-scheduled": "_1c89371c203a7229a1ab1def3ebb9b5b _89f7735a0a0d9a825cb5d081d5678c0c",
            "col-locked": "_e9d55e87ca8916f8f84c92d0dedd80e4 _5dcbbdf0848fa8079598d4076e51b7b3",
            "col-completed": "_69f0142958d96a5ad0a31424eb63fdc5 _db78e96429acd1054858c8ca19b0b6ef",
            "col-fight-ing": "_49b29262eae5314a07f621da1c710cf5 _c0c014d8d7da20ff3c3bac8a7c18a67f _ae1b2a2ed8107d0163b99a7bbfbe87ce _32ec7c38e3ad61d09173b7afaf509fbe",
            "fight-request-ing": "_71a4a840c7f161c4d96af421f10a7dd3 _738e6ae9089cb716676725e650e5c842 _b54e6299109d3fe0fcb49b737183ca91",
            "col-fight-request": "_3a0b93cb9dbdc592cb14b98277c882b6 _2bd886dd9f5b090a7ee3083951ef1b92",
            "fight-request": "_8766dcd4c15756b49587bfd35ae50755 _698f1d96d0a945bf5f6c4b2bf0c9fcf0 _f9dc1c09b17babfaa51e6b22affb8cdd",
            "col-fight-respond": "_beb49654fb78053ad5cb2f6f4eb3d6b8 _c6a532402f7f4874a29e5cb6563861c1",
            "fight-respond": "_50d88cf2f17c171a1535f31c7846dfac _d370739813d8272aa761ce739dd76b57 _15f37672043895a735e5a3da31ea71c9",
            noOnline: "_508fb50a9dd2942019c5db0fda915380 _a1d6f2cfea5235b8a604783b45cc3352",
            noOpen: "_c9af159b6a6d86ab5690f58f649d02d4 _a94f8f6f41713653a27c902a642bf5fd",
            selected: "_afd849df47da18c8fcc31197584f50ce _fec750721fd8229eb34723057a59c9c1",
            "schedule-table__empty-text": "_ae4c89ecc749743984e8a20aa4a0d8f9 _2a1b4f0a1f8a6d8df522c7e68ffa4029",
            truthy1: "_52ed9cfdacb68b0e05ceec9dc324c73d",
            truthy2: "_1731c1d52f3c3864a91aadcba6796302",
            truthy3: "_ad70aacc4e6c68318394661eef923135",
            truthy4: "_3820cee366dd05d2d94b918cfb3bdbf2",
            truthy5: "_0ddf958e444cd270c0e32ebe1f1ccc25",
            truthy6: "_13a66b04fe044a67df54d8f41602a7d1",
            truthy7: "_39522b661255a9ed432269058c34125f",
            truthy8: "_88c08336863d1dc978bea7c46cdb45bb",
            truthy9: "_690e73dfc436caf2eceaf71f9b2a8916",
            truthy10: "_9d8991f22002f71dbc5d217229f764ef",
            tabCell1: "_5a1c20c3cf10d23a9f687b2b6d069bd6",
            tabCell2: "_5ababd93f5eec097d3bd8f09e8a58761",
            tabCell3: "_1d7133c4d52c08161cd51f75899dc6e1",
            tabCell4: "_8c8dc4d903577e0fb6d3b25d48024672",
            tabCell5: "_59ed5556d51f8ce54880428d07da714d",
            tabCell6: "_a6249a2986c8810630e71debbd1e92e2",
            tabCell7: "_fdb1a17c92b41161443457f7e5f45c07",
            tabCell8: "_d363e4ec6d8da2f6321527de54f5c209",
            tabCell9: "_ab463aa83f3ae8ebee02e89332d6770b",
            tabCell10: "_1662d00b18bad028bb87319482674f90",
            tabCell11: "_ef1ad10ac760643a5f4f2ada1e333646",
            tabCell12: "_087b99940bfd919ca50ad63487563e5f",
            tabCell13: "_3475169e0a5d3c724081135a3b31a16f",
            tabCell14: "_2a6537c01e67fd19c2a4fe950a72e0a0",
            tabCell15: "_22987b0c4ea79c0898776f6a1c88a0f5",
            tabCell16: "_9be55aeb8ce192fecb24714ec3f08167",
            tabCell17: "_3460a01c66e9609faa825129200f0ca7",
            tabCell18: "_4d52c1657f36399c7b3352cc172bd299",
            tabCell19: "_13e4bca8703a3def6dd9e3b907cc00dc",
            tabCell20: "_f913919a61c5fadab3e242104a8b3c44",
            falsey1: "_e0dfa1537ae5ffc1b1a1438d6f18760c",
            falsey2: "_56bbe445bbc62ea55955e4193bcacc7b",
            falsey3: "_525f231efa18e8d39b49dbcb916be448",
            falsey4: "_bfcc8ac3efad61aca428462f227be270",
            falsey5: "_4c9126455124078fd5180925752491f0",
            falsey6: "_958d2887021d811979a2ad7f6a4c8ecb",
            falsey7: "_2a62d3b992b695be87f66131bfb8382a",
            falsey8: "_11f609d99498d643ad378d772996605d",
            falsey9: "_3db3ed8418fbf8be85e4d267b08c63ba",
            falsey10: "_2afa4a8b4d86d039c15dd712ad2d7740"
        }
          , {Careers: Z, BookingTypes: ee, OpenTimeShowTypes: te, SalesStates: se, OnlineBookingTypes: ie, CalcMode: ae} = g
          , re = "select-cols-cache"
          , le = {
            components: {
                Card: J.A,
                SpTicketCell: f.A,
                ScheduleColMsg: $
            },
            mixins: [K],
            props: {
                params: {
                    type: Object,
                    required: !0
                },
                maxHeight: Number
            },
            data() {
                const e = A.j.get(re)
                  , {__debug: t} = this.$route.query;
                return {
                    Careers: Z,
                    SalesStates: se,
                    OnlineBookingTypes: ie,
                    colWidth: 100,
                    selectedColsCache: e,
                    fightStates: {
                        request: 1,
                        requestIng: 2,
                        respond: 3
                    },
                    fightDialogShow: !1,
                    fightDialogCol: null,
                    form: {},
                    debug: !!t,
                    gridScrollCache: {
                        scrollLeft: null,
                        startTime: null
                    },
                    style: X
                }
            },
            computed: {
                truthyCls() {
                    const e = (0,
                    v.KQ)(1, 11);
                    return this.style[`truthy${e}`]
                },
                falseyClsList() {
                    return Array.from({
                        length: 3
                    }, ( () => {
                        const e = (0,
                        v.KQ)(1, 11);
                        return this.style[`falsey${e}`]
                    }
                    ))
                },
                tableCellClsList() {
                    return Array.from({
                        length: 5
                    }, ( () => {
                        const e = (0,
                        v.KQ)(1, 21);
                        return this.style[`tabCell${e}`]
                    }
                    ))
                },
                fightDialogUserCareerMapping() {
                    if (null == this.fightDialogCol)
                        return null;
                    const e = this.fightDialogCol.orderInfo.dealServiceUserList || []
                      , t = {};
                    return e.forEach((e => {
                        null == t[e.careerId] && (t[e.careerId] = []),
                        t[e.careerId].push(e)
                    }
                    )),
                    t
                },
                fightDialogBroCol() {
                    if (this.fightDialogState === this.fightStates.request || this.fightDialogState === this.fightStates.respond) {
                        const e = this.getFightBroCols(this.fightDialogCol);
                        return null === e || void 0 === e ? void 0 : e[0]
                    }
                    return null
                },
                fightDialogState() {
                    return this.getFightState(this.fightDialogCol)
                },
                isScheduleDataFirst() {
                    var e;
                    return (null === (e = this.params.salesItem) || void 0 === e ? void 0 : e.openTimeShowData) === te.ShowOccupyData.key
                },
                isReservation() {
                    var e;
                    return (null === (e = this.params.salesItem) || void 0 === e ? void 0 : e.bookingType) === ee.Reservation.key
                },
                isCalcMode() {
                    var e;
                    return this.params.calcMode === ae.DurationCalcMode.key && (null === (e = this.params.salesItem) || void 0 === e ? void 0 : e.bookingType) === ee.Booking.key
                },
                colLength() {
                    return this.platformInColumns.length
                },
                tableWidth() {
                    return this.colLength <= 3 ? null : this.colLength * this.colWidth
                },
                bodyStyle() {
                    return {
                        "max-height": this.maxHeight > 0 && this.maxHeight + "px"
                    }
                },
                maxNum() {
                    const {ticketDayMaxBuyNum: e, ticketOrderMaxBuyNum: t} = this.serverData;
                    return e > 0 && t > 0 ? Math.min(e, t) : Math.max(e || 0, t || 0, 0)
                },
                fightInfo() {
                    var e;
                    const t = null === (e = this.fightDialogCol) || void 0 === e || null === (e = e.orderInfo) || void 0 === e ? void 0 : e.dealPlatformId;
                    var s;
                    return t && (null === (s = this.serverData.fightList) || void 0 === s ? void 0 : s.find((e => t === e.dealPlatformId))) || {}
                },
                broFightInfo() {
                    var e;
                    const t = null === (e = this.fightDialogBroCol) || void 0 === e || null === (e = e.orderInfo) || void 0 === e ? void 0 : e.dealPlatformId;
                    var s;
                    return t && (null === (s = this.serverData.fightList) || void 0 === s ? void 0 : s.find((e => t === e.dealPlatformId))) || {}
                }
            },
            watch: {
                scheduleLoadFlag() {
                    this.loadSchaduleServerData(this.emitTableReload)
                },
                selectedCols() {
                    this.emitSelected();
                    const {salesId: e, venueGroupId: t, dateTime: s, salesItem: i, useCounterTemplate: a} = this.params;
                    this.isTicket;
                    const {itemId: r, salesItemId: l} = i || {};
                    A.j.put(re, {
                        itemId: r,
                        salesId: e,
                        salesItemId: l,
                        venueGroupId: t,
                        dateTime: s,
                        cols: this.selectedCols
                    })
                },
                "params.selectedSlotStartTime"() {
                    this.selectedCols = [],
                    this.resetForm();
                    const e = this.$refs["body-wrapper"];
                    e && (e.scrollTop = 0)
                },
                viewRows(e, t) {
                    (null === e || void 0 === e ? void 0 : e.length) > 0 && !((null === t || void 0 === t ? void 0 : t.length) > 0) && this.resetForm()
                }
            },
            mounted() {
                this.$nextTick(( () => {
                    const e = this.$refs["body-wrapper"];
                    null === e || void 0 === e || e.addEventListener("scroll", this.tableScrollFn)
                }
                ))
            },
            destroyed() {
                const e = this.$refs["body-wrapper"];
                null === e || void 0 === e || e.removeEventListener("scroll", this.tableScrollFn)
            },
            methods: {
                emitSelected() {
                    const {useCounterTemplate: e} = this.params
                      , t = []
                      , s = this.selectedCols.reduce(( (s, i) => {
                        const {platformInfo: a, priceBean: r, parentPriceBean: l, rowIndex: n, orderInfo: o} = i;
                        if (this.isTicket && e) {
                            const {venueId: e} = a
                              , {venueTicketId: t} = o
                              , {price: i} = r
                              , {value: l, calcTimeValue: n} = this.form[e][t] || {};
                            return (0,
                            b.WQ)(s, (0,
                            b.lK)(l || 0, i, n))
                        }
                        if (t.includes(i))
                            return s;
                        if (a.brother > 1 && l) {
                            const e = this.selectedCols.filter((e => e.platformInfo.parentId === a.parentId && n === e.rowIndex));
                            if (e.length === a.brother)
                                return t.push(...e),
                                (0,
                                b.WQ)(s, l.price || 0)
                        }
                        return (0,
                        b.WQ)(s, (null === r || void 0 === r ? void 0 : r.price) || 0)
                    }
                    ), 0);
                    this.$emit("selectedReload", this.selectedCols.length, s)
                },
                throttleScrollLeft: (0,
                l.throttle)(10, (function() {
                    const e = this.$refs["header-wrapper"]
                      , t = this.$refs["body-wrapper"];
                    e && t && (e.scrollLeft = t.scrollLeft),
                    this.cacheScroll()
                }
                )),
                cacheScroll: (0,
                l.debounce)(100, (function() {
                    if (0 === this.rows.length)
                        return;
                    const e = this.$refs["body-wrapper"];
                    if (e) {
                        this.gridScrollCache.scrollLeft = e.scrollLeft;
                        const t = e.getBoundingClientRect()
                          , s = [...e.querySelectorAll("tr")];
                        s.some(( (e, s) => {
                            const i = e.getBoundingClientRect()
                              , a = i.top - t.top;
                            if (a > -30) {
                                const e = this.rows[s];
                                if (e) {
                                    const t = e.find(Boolean);
                                    if (t)
                                        return this.gridScrollCache.startTime = t.startTime,
                                        !0
                                }
                            }
                            return !1
                        }
                        ))
                    }
                }
                )),
                tableScrollFn() {
                    window.requestAnimationFrame(this.throttleScrollLeft)
                },
                resetForm() {
                    var e;
                    const t = {};
                    null === (e = this.viewRows) || void 0 === e || e.forEach((e => {
                        null === e || void 0 === e || e.forEach((e => {
                            if (!e)
                                return;
                            const {orderInfo: s, platformInfo: i} = e;
                            if (s) {
                                const a = this.ifCounterShowCol(e) && !this.ifCounterDisableCol(e)
                                  , {venueId: r} = i;
                                t[r] = t[r] || {};
                                const l = a && 1 === this.viewRows[0].length ? 1 : 0;
                                t[r][s.venueTicketId] = {
                                    value: l,
                                    calcTimeValue: 1,
                                    col: e
                                },
                                l > 0 && a && this.onSelect(e)
                            }
                        }
                        ))
                    }
                    )),
                    this.form = t
                },
                emitTableReload() {
                    const {salesId: e, venueGroupId: t, dateTime: s, salesItem: i, useCounterTemplate: a} = this.params
                      , {itemId: r, salesItemId: l} = i || {}
                      , n = this.currentServerTime
                      , o = this.$refs["header-wrapper"]
                      , {sportPlatformList: c, timeSlotList: d, salesName: h, bookAlert: u, sliderCodeList: f} = this.serverData
                      , m = c || [];
                    this.$nextTick(( () => {
                        const {openTime: i, hourCancel: c, hourCancelType: p, cancelOrderNotes: g} = this.serverData;
                        this.$emit("hourFun", {
                            openTime: i,
                            hourCancel: c,
                            hourCancelType: p,
                            cancelOrderNotes: g
                        }),
                        this.$emit("dataReload", {
                            salesName: h,
                            marqueeText: u,
                            headerHeight: o ? Math.max(o.offsetHeight, o.clientHeight) : 0,
                            ifVerification: f,
                            timeSlotList: d,
                            someOneOnline: m.some((e => e.onlineBooking === ie.Open.key))
                        });
                        const b = this.selectedColsCache;
                        if (b && b.cols.length > 0 && b.salesId === e && b.itemId === r && b.salesItemId === l && b.venueGroupId === t && b.dateTime === s) {
                            const e = [];
                            b.cols.forEach((t => {
                                var s;
                                const {rowIndex: i, colIndex: a, startTime: r, endTime: l, hotTimeBean: n} = t
                                  , o = null === (s = this.rows[i]) || void 0 === s ? void 0 : s[a];
                                null != o ? this.isAvailableStatic(o) && r === o.startTime && l === o.endTime ? null == n && null != o.hotTimeBean || null != n && null == o.hotTimeBean ? console.log("热门时段变化1, 丢弃") : !n || !o.hotTimeBean || n.hotId === o.hotTimeBean.hotId && n.startTime === o.hotTimeBean.startTime && n.endTime === o.hotTimeBean.endTime ? this.checkAllFightColsAvailable(o) ? e.push(o) : console.log("不符合应战需要的整体，丢弃") : console.log("热门时段变化2, 丢弃") : console.log("不可用了，或者时间不对了, 丢弃") : console.log("nCol == null, 丢弃")
                            }
                            )),
                            this.selectedCols = e
                        }
                        if (this.isTicket && a)
                            return;
                        const T = this.$refs["body-wrapper"];
                        if (!T)
                            return;
                        const {scrollLeft: I, startTime: _} = this.gridScrollCache
                          , C = !_ && (0,
                        v.ro)(s, n) ? n : (0,
                        v.T$)(s, _)
                          , w = this.rows.findIndex((e => {
                            const t = e[0];
                            return null != t && t.startTime >= C
                        }
                        ));
                        if (-1 !== w) {
                            const e = [...T.querySelectorAll("tbody tr")];
                            setTimeout(( () => {
                                T.scrollTop = e[w].offsetTop
                            }
                            ), 0)
                        }
                        (0,
                        v.Et)(I) && setTimeout(( () => {
                            T.scrollLeft = I
                        }
                        ), 0)
                    }
                    ))
                },
                checkAllFightColsAvailable(e) {
                    const t = this.getFightBroCols(e);
                    if ((null === t || void 0 === t ? void 0 : t.length) > 0) {
                        const e = this.getFightBroCols(t[0]);
                        return e.length === t[0].rowspan && e.every((e => this.isAvailableStatic(e)))
                    }
                    return !0
                },
                ifCounterShowCol(e) {
                    const t = !(null == e || e.expired);
                    return !!t && this.params.selectedSlotStartTime === e._startTime
                },
                ifCounterDisableCol(e) {
                    const t = !!(null == e || null == e.priceBean || this.isNoBook(e) || e.platformInfo.onlineBooking !== ie.Open.key || this.notYetOpenTimeText || e.className);
                    return t
                },
                onTicketChange(e, t) {
                    this.form[e.platformInfo.venueId][e.orderInfo.venueTicketId].value = t;
                    const s = this.selectedCols.indexOf(e);
                    t > 0 ? -1 === s && this.onSelect(e) : -1 !== s && this.onSelect(e),
                    this.emitSelected()
                },
                onTimeChange(e, t) {
                    this.form[e.platformInfo.venueId][e.orderInfo.venueTicketId].calcTimeValue = t,
                    this.emitSelected()
                },
                getColClassNames(e) {
                    const t = this.tableCellClsList
                      , s = {
                        [X.selected]: this.selectedCols.includes(e),
                        [X[this.getFightClass(e)] || ""]: !0
                    };
                    return e.expired ? s[X.expired] = !0 : s[t[0]] = !0,
                    e.platformInfo.onlineBooking !== ie.Open.key ? s[X.noOnline] = !0 : s[t[1]] = !0,
                    this.isNoBook(e) || null == e.priceBean ? s[X.noBook] = !0 : s[t[2]] = !0,
                    this.isScheduleDataFirst && e.className || !this.notYetOpenTimeText ? s[t[3]] = !0 : s[X.noOpen] = !0,
                    e.className ? e.className.split(" ").forEach((e => {
                        e && (s[X[e]] = !0)
                    }
                    )) : s[t[4]] = !0,
                    s
                },
                onSelect(e, t) {
                    const s = e.expired || e.platformInfo.onlineBooking !== ie.Open.key || null == e.priceBean || this.notYetOpenTimeText || this.isNoBook(e);
                    if ((s || e.className) && !t)
                        return void (s || !e.orderInfo || 1 !== e.orderInfo.isFightDeal || e.colspan > 1 || (this.fightDialogCol = e,
                        this.fightDialogShow = !0));
                    const i = this.selectedCols.includes(e);
                    if (!i && !this.checkAllFightColsAvailable(e))
                        return B.A.alert("不满足应战规则，请联系服务人员下单"),
                        1;
                    const a = [];
                    if (this.getLinkageCols(e, i, a, e))
                        return;
                    if (i)
                        return void a.forEach((e => {
                            const t = this.selectedCols.indexOf(e);
                            -1 !== t && this.selectedCols.splice(t, 1)
                        }
                        ));
                    let r = 0;
                    a.forEach((e => {
                        this.selectedCols.includes(e) || (this.selectedCols.push(e),
                        r += e.endTime - e.startTime)
                    }
                    ));
                    const l = this.isUnBrokenHotTime(e);
                    if (this.isTicket || e.freeRange && !l)
                        return;
                    const n = this.serverData.everyAddTime;
                    if (n) {
                        let t = 1
                          , s = a[a.length - 1];
                        while (r < n) {
                            const i = this.isUnBrokenHotTime(s, !1)
                              , l = this.rows[s.rowIndex + t];
                            let n = null;
                            if (null == l || ( () => {
                                if (n = l[e.colIndex],
                                !this.isAvailableStatic(n) || this.selectedCols.includes(n))
                                    return !0;
                                if (this.isUnBrokenHotTime(n, !1)) {
                                    if (i) {
                                        const e = this.getHotTimeSeriesCols(s);
                                        return !e.includes(n)
                                    }
                                    return !0
                                }
                                const t = this.getFightBroCols(n);
                                return (null === t || void 0 === t ? void 0 : t.length) > 0
                            }
                            )()) {
                                if (t < 0)
                                    break;
                                t = -1,
                                s = a[0]
                            } else
                                r += n.endTime - n.startTime,
                                this.selectedCols.push(n),
                                s = n
                        }
                    }
                },
                checkOneInListMatchFight(e, t, s, i) {
                    const a = this.getFightBroCols(e);
                    if ((null === a || void 0 === a ? void 0 : a.length) > 0) {
                        if (!this.checkAllFightColsAvailable(e))
                            return B.A.alert("无法选中，本时段与对战规则冲突"),
                            !0;
                        const r = this.getFightBroCols(a[0])
                          , l = r.find((e => !s.includes(e)));
                        if (l) {
                            s.push(l);
                            const e = this.getLinkageCols(l, t, s, i);
                            if (e)
                                return !0
                        }
                    }
                },
                getLinkageCols(e, t, s, i) {
                    if (null == s)
                        return !0;
                    if (this.checkOneInListMatchFight(e, t, s, i))
                        return !0;
                    const a = this.isUnBrokenHotTime(e);
                    let r = [e];
                    if (a) {
                        const a = t ? [...s, ...this.selectedCols] : s
                          , {singleMinBookTime: l} = e.hotTimeBean
                          , n = this.getHotTimeSeriesCols(e).filter((e => !e.expired))
                          , o = a.filter((e => n.includes(e)))
                          , c = n.indexOf(e)
                          , d = n.indexOf(i);
                        if (-1 !== d && !o.includes(e)) {
                            const e = n[d - 1]
                              , s = n[d + 1];
                            if (t) {
                                if (e && a.includes(e) && s && a.includes(s))
                                    return B.A.alert("无法取消选中，本时段内预订不可间隔，请从上下边缘逐个取消选中"),
                                    !0
                            } else if (o.length > 0 && !(e && a.includes(e) || s && a.includes(s)))
                                return B.A.alert("无法选中，本时段内预订不可间隔"),
                                !0
                        }
                        if (l) {
                            const s = o.reduce(( (e, {endTime: t, startTime: s}) => e + (t - s)), 0);
                            if (t && s - (e.endTime - e.startTime) <= l)
                                r = o;
                            else {
                                const e = [];
                                let t = 0
                                  , s = 1
                                  , i = c;
                                do {
                                    const a = n[i];
                                    s > 0 ? e.push(a) : e.unshift(a);
                                    const {endTime: r, startTime: l} = a;
                                    if (t += r - l,
                                    i += s,
                                    s > 0 && i > n.length - 1 && (s = -1,
                                    i = c - 1),
                                    s < 0 && i < 0)
                                        break
                                } while (t < l);
                                r = e
                            }
                        } else
                            r = n
                    }
                    return r.forEach((e => {
                        s.includes(e) || s.push(e)
                    }
                    )),
                    !!r.some((e => this.checkOneInListMatchFight(e, t, s, i)))
                },
                cache() {
                    const e = []
                      , {salesId: t, dateTime: s, salesItem: i, useCounterTemplate: a} = this.params
                      , {salesItemId: r} = i || {}
                      , l = (e, t, i) => {
                        const {platformInfo: {venueId: r, parentId: l, parentVenueName: n, venueName: o, brother: c, selectPubStudy: d, validPubStudy: h, faceValidMode: u}, _startTime: f, _endTime: m, priceBean: p, colIndex: g, rowIndex: b, orderInfo: T} = e;
                        if (this.isTicket) {
                            const {venueTicketId: e} = T || {};
                            return {
                                venueId: r,
                                venueTicketId: e,
                                startTime: (0,
                                v.T$)(s, f),
                                endTime: (0,
                                v.T$)(s, m, !0),
                                priceBean: p,
                                platformInfo: {
                                    parentId: l,
                                    parentVenueName: n,
                                    venueName: o
                                },
                                maxBuyNum: this.maxNum,
                                buyNum: a ? this.form[r][e].value : null,
                                calcTimeValue: a ? this.form[r][e].calcTimeValue : null,
                                orderInfo: T,
                                selectPubStudy: d,
                                validPubStudy: h,
                                faceValidMode: u
                            }
                        }
                        return {
                            venueId: t ? l : r,
                            startTime: f,
                            endTime: m,
                            matchDealPlatformId: i,
                            selectPubStudy: d,
                            validPubStudy: h,
                            faceValidMode: u,
                            parentId: t ? 0 : l,
                            colspan: t ? c : 1,
                            rowspan: 1,
                            colIndex: g,
                            rowIndex: b
                        }
                    }
                    ;
                    this.isTicket ? this.selectedCols.forEach((t => {
                        e.push(l(t))
                    }
                    )) : this.selectedCols.sort(( (e, t) => e.rowIndex < t.rowIndex || e.colIndex < t.colIndex ? -1 : 1)).forEach((t => {
                        var s;
                        const {parentId: i, venueId: a, brother: r} = t.platformInfo
                          , n = this.getFightBroCols(t)
                          , o = null === n || void 0 === n || null === (s = n[0]) || void 0 === s || null === (s = s.orderInfo) || void 0 === s ? void 0 : s.orderId
                          , c = this.selectedCols.filter((e => e.platformInfo.parentId === i && t.rowIndex === e.rowIndex));
                        if (0 === i || c.length < r) {
                            if (0 === t.rowIndex)
                                return void e.push(l(t, !1, o));
                            const s = e.filter((e => e.venueId === a && e.colIndex === t.colIndex && e.rowIndex < t.rowIndex));
                            if (0 === s.length)
                                return void e.push(l(t, !1, o));
                            const i = s[s.length - 1];
                            if (i.rowIndex + 1 === t.rowIndex && i.endTime === t._startTime && i.matchDealPlatformId === o)
                                return i.endTime = t._endTime,
                                i.rowspan++,
                                void i.rowIndex++;
                            e.push(l(t, !1, o))
                        } else
                            e.some((e => 0 === e.parentId && e.venueId === i && e.rowIndex === t.rowIndex)) || e.push(l(t, r > 1))
                    }
                    ));
                    let n = -1;
                    return !this.isTicket && this.viewRows.length > 0 && (n = this.viewRows.flat().reduce(( (e, t) => this.isAvailable(t) ? e + 1 : e), 0)),
                    {
                        idleColLength: n,
                        bookStartTime: this.serverData.bookStartTime || 0,
                        ifVerification: this.serverData.sliderCodeList,
                        list: e,
                        selectSysUser: this.serverData.selectSysUser,
                        orderDate: s,
                        salesId: t,
                        salesItemId: r,
                        isCalcMode: this.isCalcMode
                    }
                },
                getFightBorderColor(e) {
                    return "white" === e || "#fff" === e || "#ffffff" === e ? "#000" : null
                },
                getFightBroCols(e) {
                    var t;
                    if (null == e)
                        return null;
                    const {broColIdxList: s, rowIndex: i, rowspan: a, orderInfo: r, platformInfo: l} = e;
                    if (0 === (null === s || void 0 === s ? void 0 : s.length))
                        return null;
                    if (r && (null === (t = r.platformSubIds) || void 0 === t ? void 0 : t.split(",").length) === l.brother)
                        return null;
                    if (r && 1 !== r.isFightDeal)
                        return null;
                    if (r) {
                        const e = s.reduce(( (e, t) => {
                            for (let r = i; r - i < a; r++) {
                                var s;
                                const i = null === (s = this.rows[r]) || void 0 === s ? void 0 : s[t];
                                i && e.push(i)
                            }
                            return e
                        }
                        ), []);
                        return e
                    }
                    const n = s.reduce(( (e, t) => {
                        for (let r = i; r >= 0; r--) {
                            var s;
                            const i = null === (s = this.rows[r]) || void 0 === s ? void 0 : s[t];
                            var a;
                            if (i)
                                return 1 === (null === (a = i.orderInfo) || void 0 === a ? void 0 : a.isFightDeal) && e.push(i),
                                e
                        }
                        return e
                    }
                    ), []);
                    return n
                },
                respondFight() {
                    if (this.fightDialogState !== this.fightStates.requestIng)
                        return;
                    const e = this.getFightBroCols(this.fightDialogCol);
                    if (null == e || 0 === e.length)
                        return void B.A.alert("不可应战");
                    this.selectedCols = [];
                    const t = this.onSelect(e[0], !0);
                    1 !== t && this.$emit("gotoNext", {
                        isTrusted: !0
                    })
                },
                getHotStyle(e) {
                    if (this.debug) {
                        const {color: t} = (null === e || void 0 === e ? void 0 : e.hotTimeBean) || {};
                        if (t)
                            return {
                                background: t,
                                color: (0,
                                N.qD)(t)
                            }
                    }
                    return null
                },
                getFightClass(e) {
                    const t = this.getFightState(e);
                    switch (t) {
                    case this.fightStates.request:
                        return "col-fight-request";
                    case this.fightStates.respond:
                        return "col-fight-respond";
                    case this.fightStates.requestIng:
                        return "col-fight-ing";
                    default:
                    }
                    return ""
                },
                getFightState(e) {
                    var t;
                    if (null == e)
                        return;
                    const {broColIdxList: s, orderInfo: i, platformInfo: a, rowIndex: r} = e;
                    if (0 === (null === s || void 0 === s ? void 0 : s.length))
                        return;
                    if (null == i || 1 !== i.isFightDeal)
                        return;
                    if ((null === (t = i.platformSubIds) || void 0 === t ? void 0 : t.split(",").length) === a.brother)
                        return;
                    const l = s.reduce(( (e, t) => {
                        for (let i = r; i >= 0; i--) {
                            var s;
                            const a = null === (s = this.rows[i]) || void 0 === s ? void 0 : s[t];
                            if (a) {
                                e.push(a);
                                break
                            }
                        }
                        return e
                    }
                    ), [])
                      , n = l.find((e => null != e && null != e.orderInfo));
                    return n ? n.orderInfo.createTime > i.createTime ? this.fightStates.request : this.fightStates.respond : this.fightStates.requestIng
                },
                popupFun() {
                    B.A.alert("超出最大限购数")
                }
            }
        }
          , ne = le;
        var oe = (0,
        w.A)(ne, h, u, !1, null, "0915a191", null);
        const ce = oe.exports;
        var de = s(90420)
          , he = s(63265)
          , ue = s(56898)
          , fe = s(75087)
          , me = function() {
            var e = this
              , t = e.$createElement
              , s = e._self._c || t;
            return s("van-popup", {
                staticClass: "min-w-[90%]",
                attrs: {
                    closeable: "",
                    round: "",
                    position: e.position
                },
                model: {
                    value: e.agreementShow,
                    callback: function(t) {
                        e.agreementShow = t
                    },
                    expression: "agreementShow"
                }
            }, [s("div", {
                staticClass: "text-center w-full text-[16px] text-[#333] leading-[50px] font-semibold"
            }, [e._v(" 订场须知"), e.count > 0 ? s("span", [e._v("（" + e._s(e.count) + "s）")]) : e._e()]), s("div", {
                ref: "scrollBox",
                staticClass: "min-h-[250px] max-h-[450px] overflow-auto px-[12px]",
                class: {
                    "mb-[72px]": e.numFlg && e.butDisplay,
                    "mb-[122px]": !e.numFlg && e.butDisplay
                },
                on: {
                    scroll: e.handleScroll
                }
            }, [s("NewsIframe", {
                staticClass: "desc-content",
                attrs: {
                    url: e.agreementUrl
                }
            })], 1), e.butDisplay ? s("section", {
                staticClass: "fixed-bt team-but p-[16px] bg-[#fff]"
            }, [s("van-row", {
                attrs: {
                    gutter: "12"
                }
            }, [s("van-col", {
                attrs: {
                    span: e.numFlg ? 12 : 24
                }
            }, [s("el-button", {
                staticClass: "full-width !rounded-3xl border-none !h-[40px] text-[16px]",
                class: [e.backFlg ? "!bg-[#F0F0F0] !text-[#333]" : "!bg-[#FFE0D6] !test-[#f63]"],
                attrs: {
                    type: "text",
                    disabled: e.repeatFlg && !e.backFlg
                },
                on: {
                    click: function(t) {
                        return e.goBack(t, e.backFlg)
                    }
                }
            }, [e._v(" " + e._s(e.backFlg ? "返回" : "接受") + " ")])], 1), s("van-col", {
                attrs: {
                    span: e.numFlg ? 12 : 24
                }
            }, [s("el-button", {
                staticClass: "full-width !rounded-3xl border-none !h-[40px] text-[16px]",
                class: [e.backFlg ? "!bg-[#FFE0D6] !test-[#f63]" : "!bg-[#F0F0F0] !text-[#333]", e.numFlg ? "" : "mt-[10px]"],
                attrs: {
                    type: "text",
                    disabled: e.repeatFlg && e.backFlg
                },
                on: {
                    click: function(t) {
                        return e.goBack(t, !e.backFlg)
                    }
                }
            }, [e._v(" " + e._s(e.backFlg ? "接受" : "返回") + " ")])], 1)], 1)], 1) : e._e()])
        }
          , pe = []
          , ge = s(6271);
        const be = {
            components: {
                NewsIframe: ge.A
            },
            props: {
                agreementUrl: String,
                agreementTime: {
                    type: Number,
                    default: 0
                },
                agreementRead: {
                    type: Number,
                    default: 0
                },
                butDisplay: {
                    type: Boolean,
                    default: !0
                }
            },
            data() {
                return {
                    agreementShow: !1,
                    position: "center",
                    type: 1,
                    count: 0,
                    timeIt: null,
                    scrollFlg: !1,
                    canScroll: !1,
                    repeatFlg: !1
                }
            },
            computed: {
                numFlg() {
                    return 1 === this.type || 2 === this.type
                },
                backFlg() {
                    return 1 === this.type || 3 === this.type
                }
            },
            watch: {
                agreementShow(e) {
                    this.scrollFlg = !1,
                    this.canScroll = !1,
                    e && (this.butDisplay ? this.position = Math.round(Math.random()) ? "center" : "bottom" : this.position = "bottom",
                    this.type = Math.floor(4 * Math.random()) + 1,
                    this.agreementTime && this.butDisplay && (this.count = (0,
                    b.y4)(this.agreementTime, 1e3),
                    this.setTimeoutFun()),
                    this.$nextTick(( () => {
                        const e = this.$refs.scrollBox;
                        e && (e.scrollTop = 0,
                        setTimeout(( () => {
                            this.canScroll = !0
                        }
                        ), 0))
                    }
                    )))
                }
            },
            methods: {
                agreementFun(e) {
                    this.agreementShow = e
                },
                setTimeoutFun() {
                    clearTimeout(this.timeIt),
                    this.count <= 0 || (this.timeIt = setTimeout(( () => {
                        this.count -= 1,
                        this.setTimeoutFun()
                    }
                    ), 1e3))
                },
                handleScroll() {
                    if (this.scrollFlg)
                        return;
                    if (!(this.agreementRead && this.butDisplay && this.canScroll))
                        return;
                    const e = this.$refs.scrollBox;
                    e.scrollTop + e.clientHeight + 5 >= e.scrollHeight && (this.scrollFlg = !0,
                    (0,
                    H.z)({
                        action: "hasScrollBottom-2"
                    }))
                },
                goBack(e, t) {
                    try {
                        if (!e.isTrusted)
                            return B.A.alert("禁止脚本操作，请按正常流程下单")
                    } catch (s) {
                        return
                    }
                    if (t)
                        this.agreementFun(!1);
                    else {
                        if (this.handleScroll(),
                        this.agreementRead && (this.count > 0 || !this.scrollFlg))
                            return B.A.alert("请先阅读完整协议");
                        this.repeatFlg = !0,
                        this.$emit("sureFun")
                    }
                }
            }
        }
          , ve = be;
        var Te = (0,
        w.A)(ve, me, pe, !1, null, null, null);
        const Ie = Te.exports
          , {SalesBookingTypes: _e, ProfessionalTypes: Ce, BookingTempTypes: we, HourCancelTypes: xe} = g
          , ye = {
            components: {
                Slider: c.A,
                ScheduleTable: ce,
                MarqueeBox: d.A,
                NeVerify: de.A,
                HomeWeather: o.A,
                OpenShareTip: ue.A,
                CustMap: fe.A,
                Agreement: Ie
            },
            mixins: [P.A, he.A],
            validate({params: e}) {
                return /^\d+$/.test(e.id)
            },
            data() {
                return {
                    SERIAL_ID: (0,
                    v.uR)().replace(/-/g, ""),
                    SalesBookingTypes: _e,
                    HourCancelTypes: xe,
                    tableMaxHeight: 0,
                    totalPrice: 0,
                    colLength: 0,
                    flushData: {},
                    serverData: {
                        bookingType: null,
                        templateType: null,
                        picUrl: null,
                        address: null,
                        location: null,
                        salesTelList: [],
                        itemDataList: [],
                        dateDataList: []
                    },
                    salesId: +this.$route.params.id || null,
                    salesItemId: null,
                    calcMode: null,
                    curDate: null,
                    venueGroupId: null,
                    selectedSlotStartTime: null,
                    ready: !1,
                    hourObj: {},
                    weatherShow: !1,
                    agreementShow: !1,
                    menuShow: !1,
                    mapVisible: !1,
                    collectFlg: null,
                    repeatFlg: !0,
                    butDisplay: !1,
                    menuList: [{
                        path: "/",
                        icon: "i-home",
                        name: "首页"
                    }, {
                        path: "/order2",
                        icon: "i-order",
                        name: "我的订单"
                    }, {
                        path: "/event",
                        icon: "i-activity",
                        name: "我的活动"
                    }, {
                        path: "navigate",
                        icon: "i-navigate-line",
                        name: "一键导航"
                    }, {
                        path: "/user/collection",
                        icon: "i-collector",
                        name: "我的收藏"
                    }, {
                        path: "/user/my",
                        icon: "icon-pt-user",
                        name: "个人中心",
                        flg: !0
                    }, {
                        path: "share",
                        icon: "icon-pt-share2",
                        name: "分享",
                        flg: !0
                    }, {
                        path: "collection",
                        icon: "i-collection",
                        selectIcon: "i-collection-block",
                        name: "收藏",
                        selectName: "取消收藏"
                    }]
                }
            },
            head() {
                const e = {
                    title: this.flushData.salesName || "预订"
                };
                return e
            },
            computed: {
                nextBtnDisText() {
                    const {bookingType: e} = this.serverData;
                    if (null == e)
                        return "无数据";
                    switch (e) {
                    case _e.Booking.key:
                    case _e.Reservation.key:
                    case _e.FreeBooking.key:
                        return null;
                    default:
                    }
                    return this.formatModel(_e, e)
                },
                canNext() {
                    return !this.nextBtnDisText && this.colLength > 0 && this.repeatFlg
                },
                isTicket() {
                    var e;
                    return (null === (e = this.item) || void 0 === e ? void 0 : e.itemType) === Ce.Ticket.key
                },
                agreementUrl() {
                    var e;
                    return null === (e = this.item) || void 0 === e ? void 0 : e.agreementUrl
                },
                agreementTime() {
                    var e;
                    return (null === (e = this.item) || void 0 === e ? void 0 : e.agreementTime) || 0
                },
                agreementRead() {
                    var e;
                    return (null === (e = this.item) || void 0 === e ? void 0 : e.agreementRead) || 0
                },
                entranceRequire() {
                    var e;
                    return null === (e = this.item) || void 0 === e ? void 0 : e.entranceRequire
                },
                item() {
                    var e;
                    return null === (e = this.serverData.itemDataList) || void 0 === e ? void 0 : e.find((e => e.salesItemId === this.salesItemId))
                },
                useCounterTemplate() {
                    const {templateType: e} = this.serverData;
                    return e === we.Counter.key
                },
                scheduleTableParams() {
                    return {
                        salesId: this.salesId,
                        dateTime: this.curDate,
                        venueGroupId: this.venueGroupId,
                        salesItem: this.item,
                        useCounterTemplate: this.useCounterTemplate,
                        selectedSlotStartTime: this.selectedSlotStartTime,
                        nextBtnDisText: this.nextBtnDisText,
                        calcMode: this.calcMode
                    }
                },
                saveSupportInfo() {
                    const {ifVerification: e} = this.flushData || {};
                    return {
                        salesItemId: this.salesItemId,
                        salesId: this.salesId,
                        orderDate: this.curDate,
                        ifVerification: e
                    }
                },
                noRefund() {
                    const {hourCancel: e, cancelOrderNotes: t} = this.hourObj
                      , s = "不可退订";
                    return 0 === e ? {
                        flg: !0,
                        msg: t || s
                    } : {
                        flg: !1,
                        msg: ""
                    }
                },
                weatherName() {
                    var e, t;
                    return null !== (e = null === (t = this.$refs.weatherBox) || void 0 === t ? void 0 : t.name) && void 0 !== e && e
                },
                weatherObj() {
                    return (this.serverData.dateDataList || []).find((e => e.day === this.curDate)) || {}
                },
                lng() {
                    return +(this.serverData.location || "").split(",")[0] || 0
                },
                lat() {
                    return +(this.serverData.location || "").split(",")[1] || 0
                }
            },
            watch: {
                salesItemId() {
                    this.onSwitchItem()
                },
                selectedSlotStartTime() {
                    this.adjustSlotStartTime()
                },
                curDate() {
                    this.adjustSlotStartTime()
                }
            },
            mounted() {
                this.$http.get("/pub/sport/venue/getSalesItemList", {
                    salesId: this.salesId
                }).then((e => {
                    const {bookingType: t, templateType: s, salesItemVOList: i, salesTelVOList: a, address: r, location: l, picUrl: n} = e || {};
                    Object.assign(this.serverData, {
                        itemDataList: i || [],
                        bookingType: t,
                        templateType: s,
                        salesTelList: null === a || void 0 === a ? void 0 : a.filter((e => e.salesTel)),
                        address: r,
                        location: l,
                        picUrl: n
                    });
                    const o = +this.$route.query.itemid
                      , c = +this.$route.query.salesItemId;
                    if (c) {
                        const e = this.serverData.itemDataList.find((e => e.salesItemId === c));
                        e && (this.salesItemId = e.salesItemId)
                    } else if (o) {
                        const e = this.serverData.itemDataList.find((e => e.itemId === o));
                        e && (this.salesItemId = e.salesItemId)
                    }
                    this.ready = !0
                }
                )),
                window.addEventListener("resize", this.windowResizeListener)
            },
            destroyed() {
                this.windowResizeListener && window.removeEventListener("resize", this.windowResizeListener)
            },
            methods: {
                adjustSlotStartTime() {
                    if (null == this.flushData.timeSlotList || null == this.selectedSlotStartTime)
                        return;
                    const e = this.flushData.timeSlotList.findIndex((e => e.startTime === this.selectedSlotStartTime));
                    if (-1 === e)
                        return;
                    const t = this.flushData.timeSlotList[e];
                    this.checkSlotTimeDisable(t) && this.$nextTick(( () => {
                        if (e < this.flushData.timeSlotList.length - 1)
                            for (let t = e + 1; t < this.flushData.timeSlotList.length; t++) {
                                const e = this.flushData.timeSlotList[t];
                                if (!this.checkSlotTimeDisable(e))
                                    return void (this.selectedSlotStartTime = e.startTime)
                            }
                        this.selectedSlotStartTime = null
                    }
                    ))
                },
                checkSlotTimeDisable(e) {
                    const t = this.currentServerTime;
                    if ((0,
                    v.ro)(t, this.curDate)) {
                        const s = (0,
                        v.T$)(t, e.endTime, !0);
                        return s <= t
                    }
                    return !1
                },
                onGroupChange(e) {
                    this.venueGroupId = e
                },
                windowResizeListener: (0,
                l.throttle)(50, (function() {
                    setTimeout(( () => {
                        this.recalculateMaxHeight()
                    }
                    ), (0,
                    v.OF)() && (0,
                    v.tR)() ? 500 : 0)
                }
                )),
                recalculateMaxHeight() {
                    this.tableMaxHeight = (0,
                    v.es)().height - (this.flushData.headerHeight || 0) - (["operation", "others", "marqueeBox"].map((e => this.$refs[e])).filter((e => !!e)).reduce(( (e, t) => (t instanceof n["default"] && (t = t.$el),
                    e + (Math.max(t.offsetHeight, t.clientHeight) || 0))), 0) || 0) - 8
                },
                onDateTimeReload() {
                    const e = this.$refs.scheduleTable;
                    e.initReload()
                },
                onDataReload(e) {
                    e = e || {},
                    this.flushData = e,
                    this.$nextTick(( () => {
                        this.recalculateMaxHeight()
                    }
                    ))
                },
                onSelectedReload(e, t) {
                    this.colLength = e,
                    this.totalPrice = t
                },
                async sure(e) {
                    try {
                        if (!e.isTrusted)
                            return B.A.alert("禁止脚本操作，请按正常流程下单")
                    } catch (s) {
                        return
                    }
                    (0,
                    H.z)({
                        action: "scheduleTableNextClick"
                    });
                    const t = this.$refs.Agreement;
                    if (!t.agreementShow) {
                        this.repeatFlg = !1;
                        try {
                            await this.nextClick()
                        } catch (i) {} finally {
                            this.repeatFlg = !0
                        }
                    }
                },
                async agreementSure() {
                    const e = this.$refs.Agreement;
                    try {
                        await this.nextClick()
                    } catch (t) {} finally {
                        e.repeatFlg = !1,
                        e.agreementFun(!1)
                    }
                },
                async nextClick() {
                    const e = this.$refs.scheduleTable
                      , t = this.$refs.Agreement;
                    try {
                        t.agreementShow || await e.check()
                    } catch (d) {
                        return
                    }
                    const {salesItemId: s} = this.item || {};
                    if (this.agreementUrl && !t.agreementShow)
                        return this.butDisplay = !0,
                        void t.agreementFun(!0);
                    const i = e.cache()
                      , {idleColLength: a, ...r} = i
                      , {bookStartTime: l, orderDate: n, list: o} = r;
                    if ((0,
                    H.z)({
                        action: "scheduleTableCache",
                        message: `${r.salesItemId},${this.formatDate(n)},${o.map((e => `${this.formatHM(e.startTime)}-${this.formatHM(e.endTime)}`)).join("|")},${l > 0 ? this.formatDateTime(l) : 0},${a}`
                    }),
                    this.isTicket) {
                        if (this.useCounterTemplate) {
                            const e = o.map(( ({venueId: e, venueTicketId: t, buyNum: s, selectPubStudy: i, validPubStudy: a, faceValidMode: r, calcTimeValue: l, priceBean: n}) => ({
                                venueId: e,
                                stockId: t,
                                buyNum: s,
                                selectPubStudy: i,
                                validPubStudy: a,
                                faceValidMode: r,
                                durationNum: l && null !== n && void 0 !== n && n.calcTimeValue ? (0,
                                b.lK)(n.calcTimeValue, l || 0) : 0
                            })));
                            return void await this.ticketSave(e)
                        }
                    } else {
                        const e = await this.$http.get("/pub/basic/isLogin");
                        e && await this.$http.postJSON("/sport/venueOrder/verifyVenue", {
                            orderDate: this.curDate,
                            salesId: this.salesId,
                            salesItemId: s,
                            sportPlatformList: o.map(( ({venueId: e, startTime: t, endTime: s}) => ({
                                venueId: e,
                                startTime: t,
                                endTime: s
                            })))
                        })
                    }
                    const c = await this.$http.postJSON("/pub/sport/venue/setVenueValue", r, {
                        rsaEncryptArray: !0
                    });
                    this.$router.push({
                        path: `/booking/${this.isTicket ? "ticket" : "service"}/${this.salesId}`,
                        query: {
                            salesItemId: s,
                            dataKey: c
                        }
                    })
                },
                onSwitchItem() {
                    if (this.item) {
                        const {salesItemId: e, calcMode: t} = this.item;
                        this.calcMode = t,
                        window.history.replaceState({}, null, `?salesItemId=${e}`),
                        this.serverData.dateDataList = null,
                        this.curDate = null,
                        this.$nextTick(( () => {
                            this.$http.get("/pub/sport/venue/getVenueCalendarList", {
                                salesItemId: e
                            }).then((e => {
                                Object.assign(this.serverData, {
                                    dateDataList: (e || []).map((e => ({
                                        ...e,
                                        dayName: this.formatMD(e.day)
                                    })))
                                })
                            }
                            ))
                        }
                        ))
                    }
                },
                onHourFun(e) {
                    const {openTime: t, hourCancel: s, hourCancelType: i, cancelOrderNotes: a} = e;
                    this.hourObj = {
                        hourCancelType: i,
                        hourCancel: s,
                        openTime: t,
                        cancelOrderNotes: a
                    }
                },
                gobackFun(e) {
                    "collection" !== e.path ? (this.menuShow = !1,
                    "share" !== e.path ? "navigate" !== e.path ? this.$router.push(e.path) : this.mapVisible = !0 : this.shareFun()) : this.$http.postJSON("/memberAccountCollection/toggle", {
                        collectionType: 1,
                        url: location.href,
                        dataId: this.salesId,
                        name: this.flushData.salesName || "预订"
                    }).then(( () => {
                        this.collectFlg = !this.collectFlg
                    }
                    ))
                },
                shareFun() {
                    this.$refs.OpenShareTip && (this.$refs.OpenShareTip.reg({
                        title: this.flushData.salesName || "预订",
                        link: window.location.href,
                        img: this.serverData.picUrl,
                        desc: "快来参与吧"
                    }),
                    this.$nextTick(( () => {
                        this.$refs.OpenShareTip.show()
                    }
                    )))
                },
                menuFun() {
                    this.menuShow = !0,
                    null === this.collectFlg && this.$http.get("/pub/memberAccountCollection/isCollection", {
                        collectionType: 1,
                        dataId: this.salesId
                    }).then((e => {
                        this.collectFlg = e
                    }
                    ))
                },
                agreementShowFun() {
                    this.butDisplay = !1;
                    const e = this.$refs.Agreement;
                    e.agreementFun(!0)
                }
            }
        }
          , Se = ye;
        var ke = (0,
        w.A)(Se, a, r, !1, null, "393b48a6", null);
        const De = ke.exports
    }
    ,
    9805: (e, t, s) => {
        s.d(t, {
            qD: () => c
        });
        s(44114),
        s(27495),
        s(25440);
        const i = /^#([\dA-Fa-f]{3}|[\dA-Fa-f]{6})$/;
        function a(e) {
            if (!e || e.startsWith("#"))
                return e;
            const t = e.split(",")
              , s = Number.parseInt(t[0].split("(")[1], 10)
              , i = Number.parseInt(t[1], 10)
              , a = Number.parseInt(t[2].split(")")[0], 10);
            let r = 1;
            4 === t.length && (r = Number.parseFloat(t[3].split(")")[0]));
            const l = Math.round(255 * r).toString(16).padStart(2, "0")
              , n = `#${((1 << 24) + (s << 16) + (i << 8) + a).toString(16).slice(1)}`;
            return "ff" === l ? n : `${n}${l}`
        }
        let r;
        function l(e) {
            let t = e;
            return null == t ? null : (t = t.trim().toLowerCase(),
            t.startsWith("#") ? t : t.startsWith("rgb") ? a(t) : (null == r && (r = document.createElement("canvas").getContext("2d")),
            r.fillStyle = t,
            a(r.fillStyle)))
        }
        function n(e, t) {
            let s = e;
            if (null == s)
                return null;
            if (s = s.trim().toLowerCase(),
            s.startsWith("rgb"))
                return s;
            let a = l(s);
            if (a && i.test(a)) {
                if (4 === a.length) {
                    let e = "#";
                    for (let t = 1; t < 4; t += 1)
                        e += a.slice(t, t + 1) + a.slice(t, t + 1);
                    a = e
                }
                const e = [];
                for (let t = 1; t < 7; t += 2)
                    e.push(Number.parseInt(a.slice(t, t + 2), 16));
                const s = e.join(",");
                return t ? `rgba(${s}, ${t})` : `rgb(${s})`
            }
            return a
        }
        function o(e) {
            const t = n(e);
            if (t) {
                const e = t.replace("rgb(", "").replace(")", "").split(",")
                  , s = .299 * e[0] + .587 * e[1] + .114 * e[2];
                return s
            }
            return 0
        }
        function c(e, t) {
            const {level: s, compareColor: i, darkColor: a, lightColor: r} = t || {}
              , l = o(e);
            if (l > 0) {
                const t = o(i);
                if (t > 0 && l > t)
                    return e;
                if (l > (s || 192))
                    return a || "#000"
            }
            return r || "#fff"
        }
    }
    ,
    64880: (e, t, s) => {
        s.d(t, {
            A: () => l
        });
        var i = s(95353)
          , a = s(25800);
        const {mapGetters: r} = (0,
        i.$t)("global")
          , l = {
            data() {
                const e = Date.now();
                return {
                    ST_serverTimeInfo: {
                        nowTime: e,
                        timer: null
                    }
                }
            },
            computed: {
                ...r(["getCurrentServerTimeDuration"]),
                currentServerTime() {
                    const e = this.getCurrentServerTimeDuration()
                      , {nowTime: t} = this.ST_serverTimeInfo
                      , s = t - e;
                    return s
                }
            },
            watch: {
                currentServerTime(e, t) {
                    var s;
                    (0,
                    a.ro)(e, t) || null === (s = this.tickToNewDay) || void 0 === s || s.call(this)
                }
            },
            mounted() {
                this.ST_selfTimeUpdater()
            },
            destroyed() {
                this.ST_serverTimeInfo.timer && clearTimeout(this.ST_serverTimeInfo.timer)
            },
            methods: {
                ST_selfTimeUpdater() {
                    const e = Date.now();
                    Math.abs(e - this.ST_serverTimeInfo.nowTime) > 1e4 && this.$http.get("/pub/basic/getConfig", null, {
                        silent: !0
                    }).then((e => {
                        this.$store.commit("global/setServerTime", e)
                    }
                    )),
                    this.ST_serverTimeInfo.nowTime = e,
                    this.ST_serverTimeInfo.timer = setTimeout(this.ST_selfTimeUpdater, 1e3)
                }
            }
        }
    }
    ,
    46449: (e, t, s) => {
        var i = s(46518)
          , a = s(70259)
          , r = s(48981)
          , l = s(26198)
          , n = s(91291)
          , o = s(1469);
        i({
            target: "Array",
            proto: !0
        }, {
            flat: function() {
                var e = arguments.length ? arguments[0] : void 0
                  , t = r(this)
                  , s = l(t)
                  , i = o(t, 0);
                return i.length = a(i, t, t, s, 0, void 0 === e ? 1 : n(e)),
                i
            }
        })
    }
    ,
    93514: (e, t, s) => {
        var i = s(6469);
        i("flat")
    }
}]);