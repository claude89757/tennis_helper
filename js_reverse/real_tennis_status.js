// ==UserScript==
// @name         场地预订助手
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  显示场地状态
// @author       claude89757
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
        script.textContent = '(' + function() {
            const log = function(...args) {
                console.log('%c[预订助手]', 'color: #1890ff', ...args);
            };

            // 创建弹窗显示场地状态
            function showVenueStatus(slots) {
                // 尝试发送系统通知
                try {
                    if (Notification.permission === "granted") {
                        new Notification("6号场地状态更新", {
                            body: `有${slots.filter(s => s.dealState !== 2).length}个时段可预订`
                        });
                    } else if (Notification.permission !== "denied") {
                        Notification.requestPermission().then(permission => {
                            if (permission === "granted") {
                                new Notification("6号场地状态更新", {
                                    body: `有${slots.filter(s => s.dealState !== 2).length}个时段可预订`
                                });
                            }
                        });
                    }
                } catch(e) {
                    log('通知发送失败:', e);
                }

                // 创建弹窗容器
                const modal = document.createElement('div');
                modal.style.cssText = `
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                    z-index: 9999;
                    min-width: 300px;
                `;

                // 创建标题
                const title = document.createElement('h3');
                title.textContent = '6号场地状态';
                title.style.cssText = `
                    margin: 0 0 15px 0;
                    padding-bottom: 10px;
                    border-bottom: 1px solid #eee;
                `;
                modal.appendChild(title);

                // 创建表格
                const table = document.createElement('table');
                table.style.cssText = `
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 15px;
                `;

                // 添加表头
                const thead = document.createElement('thead');
                thead.innerHTML = `
                    <tr>
                        <th style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5;">开始时间</th>
                        <th style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5;">结束时间</th>
                        <th style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5;">状态</th>
                    </tr>
                `;
                table.appendChild(thead);

                // 添加表格内容
                const tbody = document.createElement('tbody');
                slots.forEach(slot => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td style="padding: 8px; border: 1px solid #ddd;">${new Date(slot.startTime).toLocaleTimeString()}</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">${new Date(slot.endTime).toLocaleTimeString()}</td>
                        <td style="padding: 8px; border: 1px solid #ddd; color: ${slot.dealState === 2 ? 'red' : 'green'};">
                            ${slot.dealState === 2 ? '已预订' : '可预订'}
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
                table.appendChild(tbody);
                modal.appendChild(table);

                // 添加关闭按钮
                const closeBtn = document.createElement('button');
                closeBtn.textContent = '关闭';
                closeBtn.style.cssText = `
                    padding: 6px 15px;
                    background: #1890ff;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    display: block;
                    margin: 0 auto;
                `;
                closeBtn.onclick = () => document.body.removeChild(modal);
                modal.appendChild(closeBtn);

                document.body.appendChild(modal);
            }

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

            // 监听getVenueOrderList请求
            function monitorRequests() {
                const originalOpen = XMLHttpRequest.prototype.open;
                const originalSend = XMLHttpRequest.prototype.send;

                XMLHttpRequest.prototype.open = function(method, url, ...rest) {
                    this._isTargetRequest = url.includes('/pub/sport/venue/getVenueOrderList');
                    return originalOpen.call(this, method, url, ...rest);
                };

                XMLHttpRequest.prototype.send = function(body) {
                    if (this._isTargetRequest) {
                        this.addEventListener('load', function() {
                            try {
                                const response = JSON.parse(this.responseText);
                                log('getVenueOrderList响应:', response);

                                // 过滤出6号场地的数据并显示弹窗
                                const venueSlots = response.data.filter(s => s.venueId === 102930);
                                if (venueSlots.length > 0) {
                                    showVenueStatus(venueSlots);
                                }

                                // 更新所有场地状态
                                const vm = findVueInstance();
                                if (vm && vm.$refs.scheduleTable) {
                                    hackComponent(vm);
                                }
                            } catch (err) {
                                log('处理响应失败:', err);
                            }
                        });
                    }
                    return originalSend.call(this, body);
                };
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

            // 开始监听请求
            monitorRequests();
        } + ')();';

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

            .schedule-table td.col-scheduled {
                background-color: #ffccc7 !important;
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
