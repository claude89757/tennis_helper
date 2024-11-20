// ==UserScript==
// @name         Zacks网球场预定小助手(浏览器插件)
// @namespace    http://zacks.com.cn/
// @version      0.1
// @description  显示场地状态
// @author       claude89757
// @match        *://*.ydmap.cn/*
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
            function showVenueStatus(allVenueSlots, isInitialLoad = false) {
                // 过滤出6号场地的数据
                const venueSlots = allVenueSlots.filter(slot => slot.venueId === 102930);

                if (venueSlots.length === 0) {
                    log('没有找到6号场地的数据');
                    return;
                }

                // 只在初次加载时显示弹窗
                if (isInitialLoad) {
                    createStatusModal(venueSlots);
                }

                // 检查可预订状态并发送通知
                checkAndNotify(venueSlots);
            }

            // 创建状态弹窗
            function createStatusModal(venueSlots) {
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
                    min-width: 600px;
                    max-height: 80vh;
                    overflow-y: auto;
                `;

                // 创建标题和倒计时容器
                const titleContainer = document.createElement('div');
                titleContainer.style.cssText = `
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin: 0 0 15px 0;
                    padding-bottom: 10px;
                    border-bottom: 1px solid #eee;
                `;

                const title = document.createElement('h3');
                title.textContent = '6号场地预订状态';
                title.style.margin = '0';

                const countdown = document.createElement('span');
                countdown.style.cssText = `
                    color: #999;
                    font-size: 14px;
                `;

                titleContainer.appendChild(title);
                titleContainer.appendChild(countdown);
                modal.appendChild(titleContainer);

                // 创建表格
                const table = document.createElement('table');
                table.style.cssText = `
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 15px;
                `;

                const thead = document.createElement('thead');
                thead.innerHTML = `
                    <tr>
                        <th style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5;">开始时间</th>
                        <th style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5;">结束时间</th>
                        <th style="padding: 8px; border: 1px solid #ddd; background: #f5f5f5;">状态</th>
                    </tr>
                `;
                table.appendChild(thead);

                const tbody = document.createElement('tbody');
                venueSlots.forEach(slot => {
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

                // 关闭函数
                const closeModal = () => {
                    if (document.body.contains(modal)) {
                        document.body.removeChild(modal);
                    }
                };

                // 倒计时更新函数
                let remainingSeconds = 5;
                const updateCountdown = () => {
                    countdown.textContent = `${remainingSeconds}秒后自动关闭`;
                    if (remainingSeconds > 0) {
                        remainingSeconds--;
                        setTimeout(updateCountdown, 1000);
                    }
                };

                // 启动倒计时显示
                updateCountdown();

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

                closeBtn.onclick = closeModal;
                modal.appendChild(closeBtn);

                document.body.appendChild(modal);

                // 5秒后自动关闭
                setTimeout(closeModal, 5000);
            }

            // 检查并发送通知
            function checkAndNotify(venueSlots) {
                const availableSlots = venueSlots.filter(s => s.dealState !== 2);
                if (availableSlots.length > 0) {
                    try {
                        if (Notification.permission === "granted") {
                            new Notification("6号场地可预订提醒", {
                                body: `6号场地有${availableSlots.length}个时段可预订\n时间: ${new Date(availableSlots[0].startTime).toLocaleTimeString()}-${new Date(availableSlots[availableSlots.length-1].endTime).toLocaleTimeString()}`,
                                icon: "/favicon.ico"
                            });
                        } else if (Notification.permission !== "denied") {
                            Notification.requestPermission().then(permission => {
                                if (permission === "granted") {
                                    new Notification("6号场地可预订提醒", {
                                        body: `6号场地有${availableSlots.length}个时段可预订\n时间: ${new Date(availableSlots[0].startTime).toLocaleTimeString()}-${new Date(availableSlots[availableSlots.length-1].endTime).toLocaleTimeString()}`,
                                        icon: "/favicon.ico"
                                    });
                                }
                            });
                        }
                    } catch (e) {
                        log('通知发送失败:', e);
                    }
                }
            }

            // 查找Vue实例的函数
            function findVueInstance() {
                const elements = document.querySelectorAll('*');
                for (const el of elements) {
                    if (el.__vue__) {
                        const vm = el.__vue__;
                        if (vm.onSelect || vm.$refs.scheduleTable) {
                            log('找到目标Vue实例');
                            return vm;
                        }
                        if (vm.$children) {
                            for (const child of vm.$children) {
                                if (child.onSelect || child.$refs.scheduleTable) {
                                    log('在子组件中找到目标Vue实例');
                                    return child;
                                }
                            }
                        }
                    }
                }
                return null;
            }

            // 组件方法
            function hackComponent(vm) {
                if (!vm || vm._hacked) return;

                const scheduleTable = vm.$refs.scheduleTable || vm;

                // 保存原始方法
                const originalMethods = {
                    isAvailable: scheduleTable.isAvailable,
                    isAvailableStatic: scheduleTable.isAvailableStatic,
                    check: scheduleTable.check,
                    loadSchaduleServerData: scheduleTable.loadSchaduleServerData
                };

                // 劫持方法
                const methods = {
                    isAvailable: () => true,
                    isAvailableStatic: () => true,
                    check: async() => true
                };

                // 应用劫持
                Object.keys(methods).forEach(key => {
                    if (scheduleTable[key]) {
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

                // 添加定时任务函数
                function scheduleCheck() {
                    const today = new Date();
                    const dateStr = today.toISOString().split('T')[0];
                    const timeStr = today.toLocaleTimeString();

                    log(`[定时任务] ${timeStr} 开始执行场地查询...`);

                    // 查找Vue实例
                    const vm = findVueInstance();
                    if (!vm) {
                        log('[定时任务] 未找到Vue实例，跳过查询');
                        return;
                    }

                    // 使用原有的请求方法
                    try {
                        // 获取原始请求方法
                        const originRequest = vm.$refs.scheduleTable && vm.$refs.scheduleTable.loadSchaduleServerData;

                        if (typeof originRequest === 'function') {
                            log('[定时任务] 使用原有请求方法');
                            originRequest.call(vm.$refs.scheduleTable, () => {
                                log('[定时任务] 请求完成回调');
                            });
                        } else {
                            log('[定时任务] 未找到原有请求方法');
                        }
                    } catch (error) {
                        log('[定时任务] 执行出错:', error);
                    }
                }

                // 设置100秒定时任务
                log('[系统] 启动定时查询任务 (间隔: 100秒)');
                const checkInterval = setInterval(scheduleCheck, 100000);

                // 保持原有的请求监听代码
                XMLHttpRequest.prototype.open = function(method, url, ...rest) {
                    if (url.includes('/pub/sport/venue/getVenueOrderList')) {
                        this._isTargetRequest = true;
                        log('[请求监听] 检测到场地查询请求:', { method, url });
                    }
                    return originalOpen.call(this, method, url, ...rest);
                };

                XMLHttpRequest.prototype.send = function(body) {
                    if (this._isTargetRequest) {
                        log('[请求监听] 发送请求数据:', body ? JSON.parse(body) : null);

                        this.addEventListener('load', function() {
                            try {
                                const response = JSON.parse(this.responseText);
                                log('[请求监听] 收到响应:', {
                                    code: response.code,
                                    message: response.message,
                                    场地数量: response.data ? (response.data.length || 0) : 0,
                                    场地详情: response.data ? response.data.map(slot => ({
                                        场地名称: slot.venueName,
                                        开始时间: new Date(slot.startTime).toLocaleTimeString(),
                                        结束时间: new Date(slot.endTime).toLocaleTimeString(),
                                        状态: slot.dealState === 2 ? '已预订' : '可预订'
                                    })) : []
                                });

                                if (response.data && response.data.length > 0) {
                                    // 第一次加载时显示弹
                                    const isInitialLoad = !this._hasShownModal;
                                    if (isInitialLoad) {
                                        this._hasShownModal = true;
                                    }
                                    showVenueStatus(response.data, isInitialLoad);
                                }
                            } catch (err) {
                                log('[请求监听] 处理响应失败:', err);
                            }
                        });
                    }
                    return originalSend.call(this, body);
                };
            }

            // 定时检查并劫持组件
            const hackInterval = setInterval(() => {
                const vm = findVueInstance();
                if (vm) {
                    hackComponent(vm);
                    if (vm._hacked) {
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