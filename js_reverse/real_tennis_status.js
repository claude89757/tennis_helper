// ==UserScript==
// @name         场地预订助手
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  福田体育显示场地真实状态
// @author       zacks
// @match        *://*/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    const log = (...args) => {
        console.log('%c[预订助手]', 'color: #1890ff', ...args);
    };

    function injectCode() {
        log('开始注入代码');

        const script = document.createElement('script');
        script.textContent = `
            (function() {
                const log = (...args) => {
                    console.log('%c[预订助手]', 'color: #1890ff', ...args);
                };

                // 查找Vue实例的函数
                function findVueInstance() {
                    const elements = document.querySelectorAll('*');
                    for(const el of elements) {
                        if(el.__vue__) {
                            const vm = el.__vue__;
                            if(vm.onSelect || vm.$refs.scheduleTable) {
                                log('找到目标Vue实例');
                                return vm;
                            }
                            if(vm.$children) {
                                for(const child of vm.$children) {
                                    if(child.onSelect || child.$refs.scheduleTable) {
                                        log('在子组件中找到目标Vue实例');
                                        return child;
                                    }
                                }
                            }
                        }
                    }
                    return null;
                }

                // 劫持组件方法
                function hackComponent(vm) {
                    if(!vm || vm._hacked) return;

                    // 获取scheduleTable组件
                    const scheduleTable = vm.$refs.scheduleTable || vm;

                    // 劫持方法
                    const methods = {
                        isAvailable: () => true,
                        isAvailableStatic: () => true,
                        check: async () => true
                    };

                    // 应用劫持
                    Object.keys(methods).forEach(key => {
                        if(scheduleTable[key]) {
                            scheduleTable[key] = methods[key].bind(scheduleTable);
                        }
                    });

                    // 劫持计算属性
                    const computed = {
                        notYetOpenTimeText: null,
                        nextBtnDisText: "不可预订",
                        canNext: false,
                        repeatFlg: true
                    };

                    Object.keys(computed).forEach(key => {
                        Object.defineProperty(scheduleTable, key, {
                            get: () => computed[key],
                            configurable: true
                        });
                    });

                    vm._hacked = true;
                    log('组件劫持完成');
                }

                // 定时检查并劫持组件
                const hackInterval = setInterval(() => {
                    const vm = findVueInstance();
                    if(vm) {
                        hackComponent(vm);
                        if(vm._hacked) {
                            clearInterval(hackInterval);
                        }
                    }
                }, 1000);
            })();
        `;

        // 注入样式
        const style = document.createElement('style');
        style.textContent = `
            .schedule-table td,
            .schedule-table td.col-booking-disabled,
            .schedule-table td.noBook,
            .schedule-table td.expired {
                cursor: default !important;
                opacity: 1 !important;
                pointer-events: none !important;
                background-color: white !important;
            }

            .primary-button,
            .primary-button[disabled] {
                opacity: 0.5 !important;
                cursor: not-allowed !important;
                pointer-events: none !important;
                background: #ccc !important;
            }
        `;

        (document.head || document.documentElement).appendChild(script);
        (document.head || document.documentElement).appendChild(style);

        log('代码注入完成');
    }

    injectCode();
})();
