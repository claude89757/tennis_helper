// ==UserScript==
// @name         验证码助手终极版
// @namespace    http://tampermonkey.net/
// @version      0.7
// @description  跳过图片验证码
// @author       You
// @match        *://*/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    // 添加安全的序列化函数
    function safeStringify(obj) {
        try {
            return JSON.stringify(obj, (key, value) => {
                if (typeof value === 'function') {
                    return 'function';
                }
                if (value instanceof Error) {
                    return value.message;
                }
                if (value instanceof Node) {
                    return '[DOM Node]';
                }
                if (value instanceof Window) {
                    return '[Window]';
                }
                if (value === document) {
                    return '[Document]';
                }
                if (typeof value === 'object' && value !== null) {
                    const seen = new WeakSet();
                    if (seen.has(value)) {
                        return '[Circular]';
                    }
                    seen.add(value);
                }
                return value;
            }, 2);
        } catch (err) {
            return `[无法序列化: ${err.message}]`;
        }
    }

    const logger = {
        debug: (msg, data) => {
            console.debug(`%c[验证码助手|DEBUG] ${msg}`, 'color: gray',
                data ? (typeof data === 'object' ? safeStringify(data) : data) : '');
        },
        info: (msg, data) => {
            console.log(`%c[验证码助手|INFO] ${msg}`, 'color: green',
                data ? (typeof data === 'object' ? safeStringify(data) : data) : '');
        },
        warn: (msg, data) => {
            console.warn(`%c[验证码助手|WARN] ${msg}`, 'color: orange',
                data ? (typeof data === 'object' ? safeStringify(data) : data) : '');
        },
        error: (msg, err) => {
            console.error(`%c[验证码助手|ERROR] ${msg}`, 'color: red', err);
            if(err && err.stack) {
                console.error(`%c[验证码助手|STACK] ${err.stack}`, 'color: red');
            }
        }
    };

    // 缓存验证码结果和状态
    let verifyCache = null;
    let isVerifying = false;

    // 监听验证码API
    function setupVerifyListener() {
        // 监听动态添加的script标签
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if(node.tagName === 'SCRIPT') {
                        const src = node.src;
                        if(src && src.includes('c.dun.163.com/api/v3/check')) {
                            logger.info('捕获到网易易盾验证码请求', {
                                src,
                                params: new URL(src).searchParams
                            });

                            // 获取callback参数
                            const url = new URL(src);
                            const callback = url.searchParams.get('callback');
                            const token = url.searchParams.get('token');

                            if(callback) {
                                logger.info('找到callback参数', {
                                    callback,
                                    token
                                });

                                // 保存原始callback
                                const originalCallback = window[callback];

                                // 替换callback
                                window[callback] = function(response) {
                                    logger.info('验证码callback被调用', response);

                                    // 检查验证结果
                                    if(response.data?.validate) {
                                        // 从URL中获取iv参数作为验证码类型
                                        const iv = url.searchParams.get('iv');
                                        logger.info('获取到验证码类型参数', {iv});

                                        verifyCache = {
                                            validate: response.data.validate,
                                            token: token,
                                            captchaStyleIndex: parseInt(iv) || 4  // 使用iv参数，如果没有就用4
                                        };
                                        isVerifying = true;
                                        logger.info('从callback中获取验证结果', verifyCache);

                                        // 返回一个假的成功响应
                                        return {
                                            data: {
                                                result: false,  // 返回false，让验证码组件认为验证失败
                                                validate: null
                                            },
                                            error: 0,
                                            msg: "ok"
                                        };
                                    }

                                    // 如果没有validate，才调用原始callback
                                    if(originalCallback) {
                                        return originalCallback.apply(this, arguments);
                                    }
                                };
                            }
                        }
                    }
                });
            });
        });

        // 监听DOM变化
        observer.observe(document.documentElement, {
            childList: true,
            subtree: true
        });
    }

    // 启动监听
    setupVerifyListener();

    // 监听下一步按钮点击
    function setupNextButtonListener() {
        const checkButton = () => {
            const nextButton = document.querySelector('.primary-button');
            if (nextButton && !nextButton._hasClickListener) {
                nextButton._hasClickListener = true;
                logger.info('找到下一步按钮,添加点击监听');

                // 保存原始的点击事件处理函数
                const originalClick = nextButton.onclick;

                // 替换点击事件处理函数
                nextButton.onclick = async function(e) {
                    e.preventDefault();
                    e.stopPropagation();

                    const scope = window.__EXEC_CALLBACK_SCOPE;
                    if (!scope || !scope.execSaveData) {
                        logger.error('未找到订单数据');
                        if(originalClick) {
                            return originalClick.call(this, e);
                        }
                        return;
                    }

                    // 如果有验证码缓存，直接使用缓存下单
                    if(verifyCache) {
                        logger.info('使用缓存的验证码结果下单', verifyCache);

                        // 获取Vue组件实例
                        const vm = document.querySelector('#app').__vue__;
                        if(vm) {
                            try {
                                // 递归查找所有子组件
                                function findComponent(component) {
                                    if(component.onVerifyConfirm) {
                                        return component;
                                    }

                                    if(component.$children) {
                                        for(let child of component.$children) {
                                            const found = findComponent(child);
                                            if(found) return found;
                                        }
                                    }

                                    return null;
                                }

                                // 从根组件开始查找
                                const component = findComponent(vm);

                                if(component) {
                                    logger.info('找到onVerifyConfirm方法，开始执行下单');

                                    // 依次尝试类型3和4
                                    const types = [3, 4];
                                    let successType = null;

                                    for(const type of types) {
                                        try {
                                            // 构造验证结果
                                            const verifyResult = {
                                                validate: verifyCache.validate,
                                                captchaStyleIndex: type
                                            };
                                            logger.info(`尝试验证码类型${type}`, verifyResult);

                                            // 调用onVerifyConfirm方法
                                            await component.onVerifyConfirm(verifyResult);
                                            logger.info(`验证码类型${type}成功`);
                                            successType = type;
                                        } catch(err) {
                                            logger.warn(`验证码类型${type}失败`, err);
                                        }
                                    }

                                    if(successType !== null) {
                                        logger.info(`成功使用验证码类型${successType}`);
                                        return;
                                    } else {
                                        logger.warn('所有验证码类型都失败了，尝试执行原始点击事件');
                                        if(originalClick) {
                                            originalClick.call(this, e);
                                        }
                                    }
                                } else {
                                    logger.warn('未找到onVerifyConfirm方法，尝试执行原始点击事件');
                                    if(originalClick) {
                                        originalClick.call(this, e);
                                    }
                                }
                            } catch(err) {
                                logger.error('执行onVerifyConfirm失败', err);
                                if(originalClick) {
                                    originalClick.call(this, e);
                                }
                            }
                        } else {
                            logger.warn('未找到Vue实例');
                            if(originalClick) {
                                originalClick.call(this, e);
                            }
                        }
                        return;
                    }

                    // 如果正在验证，只缓存结果不下单
                    if(isVerifying) {
                        logger.info('正在进行人工验证，缓存验证码结果');
                        isVerifying = false; // 重置状态
                        return; // 阻止下单
                    }

                    // 没有缓存也不是正验证，执行原始点击事件
                    logger.warn('未找到验证码缓存，需要进行人工验证');
                    if(originalClick) {
                        originalClick.call(this, e);
                    }
                };
            }
        };

        setInterval(checkButton, 500);
        checkButton();
    }

    // 等待DOM加载完成后启动监听
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupNextButtonListener);
    } else {
        setupNextButtonListener();
    }

    logger.info('验证码助手初始化完成');
})();