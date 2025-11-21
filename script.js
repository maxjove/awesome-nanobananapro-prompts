// 全局配置
const CONFIG = {
    animations: {
        enabled: true,
        duration: 300,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
    },
    breakpoints: {
        mobile: 768,
        tablet: 1024,
        desktop: 1280
    },
    performance: {
        lazyLoad: true,
        throttleDelay: 100,
        debounceDelay: 300
    }
};

// 工具函数
const utils = {
    // 节流函数
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    // 防抖函数
    debounce(func, wait, immediate) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            const later = () => {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },

    // 获取元素在视口中的位置
    getElementPosition(element) {
        const rect = element.getBoundingClientRect();
        return {
            top: rect.top + window.pageYOffset,
            left: rect.left + window.pageXOffset,
            height: rect.height,
            width: rect.width
        };
    },

    // 检查元素是否在视口中
    isElementInViewport(element, threshold = 0.1) {
        const rect = element.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        const windowWidth = window.innerWidth || document.documentElement.clientWidth;

        const verticalThreshold = windowHeight * threshold;
        const horizontalThreshold = windowWidth * threshold;

        return (
            rect.top <= windowHeight - verticalThreshold &&
            rect.bottom >= verticalThreshold &&
            rect.left <= windowWidth - horizontalThreshold &&
            rect.right >= horizontalThreshold
        );
    }
};

// 应用初始化
class NanoBananaApp {
    constructor() {
        this.isLoaded = false;
        this.sections = [];
        this.navigationElements = [];
        this.theme = this.loadTheme();
        this.init();
    }

    init() {
        this.setupLoadingScreen();
        this.setupNavigation();
        this.setupScrollEffects();
        this.setupAnimations();
        this.setupTheme();
        this.setupImageHandling();
        this.setupInteractions();
        this.setupPerformanceOptimizations();
    }

    // 加载屏幕
    setupLoadingScreen() {
        const loadingScreen = document.getElementById('loadingScreen');
        if (loadingScreen) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    loadingScreen.classList.add('fade-out');
                    setTimeout(() => {
                        loadingScreen.style.display = 'none';
                    }, 500);
                }, 1000);
            });
        }
    }

    // 初始化动画元素
    initAnimatedElements() {
        const animatedElements = document.querySelectorAll('.feature-card, .example-card, .tip-card, .resource-card');
        animatedElements.forEach(el => {
            el.style.opacity = '0';
            el.setAttribute('data-animate', 'fadeInUp');
            if (this.animationObserver) {
                this.animationObserver.observe(el);
            }
        });
    }

    // 导航设置
    setupNavigation() {
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');
        const navToggle = document.getElementById('navToggle');

        // 移动端菜单切换
        if (hamburger && navMenu) {
            hamburger.addEventListener('click', () => {
                hamburger.classList.toggle('active');
                navMenu.classList.toggle('active');
                document.body.classList.toggle('nav-open');
            });

            // 关闭移动端菜单当点击链接时
            document.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', (e) => {
                    const href = link.getAttribute('href');
                    if (href.startsWith('#')) {
                        e.preventDefault();
                        this.scrollToSection(href);
                    }

                    hamburger.classList.remove('active');
                    navMenu.classList.remove('active');
                    document.body.classList.remove('nav-open');
                });
            });
        }

        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = anchor.getAttribute('href');
                this.scrollToSection(targetId);
            });
        });
    }

    // 滚动到指定部分
    scrollToSection(targetId) {
        const target = document.querySelector(targetId);
        if (target) {
            const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
            const targetPosition = utils.getElementPosition(target).top - headerHeight - 20;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    }

    // 滚动效果
    setupScrollEffects() {
        const header = document.querySelector('.header');

        // 导航栏滚动效果
        const scrollHandler = utils.throttle(() => {
            const scrollY = window.pageYOffset;

            // 头部阴影效果
            if (header) {
                if (scrollY > 100) {
                    header.classList.add('scrolled');
                } else {
                    header.classList.remove('scrolled');
                }
            }

            // 进度指示器
            this.updateScrollIndicator();

            // 视差效果
            this.updateParallaxEffects();

            // 滚动动画
            this.updateScrollAnimations();
        }, CONFIG.performance.throttleDelay);

        window.addEventListener('scroll', scrollHandler);
    }

    // 更新滚动指示器
    updateScrollIndicator() {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;

        const progressBar = document.querySelector('.scroll-progress');
        if (progressBar) {
            progressBar.style.width = `${scrollPercent}%`;
        }
    }

    // 视差效果
    updateParallaxEffects() {
        const scrollY = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('[data-parallax]');

        parallaxElements.forEach(element => {
            const speed = parseFloat(element.dataset.parallax) || 0.5;
            const yPos = -(scrollY * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    }

    // 动画设置
    setupAnimations() {
        this.animationObserver = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.animateElement(entry.target);
                        this.animationObserver.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }
        );

        // 初始化需要动画的元素
        setTimeout(() => {
            this.initAnimatedElements();
        }, 100);
    }

    // 动画元素
    animateElement(element) {
        const animation = element.dataset.animate;
        const delay = element.dataset.delay || 0;

        setTimeout(() => {
            element.classList.add('animated', animation);
        }, delay);
    }

    // 主题设置
    setupTheme() {
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }

        // 应用保存的主题
        this.applyTheme(this.theme);
    }

    toggleTheme() {
        this.theme = this.theme === 'dark' ? 'light' : 'dark';
        this.applyTheme(this.theme);
        this.saveTheme(this.theme);
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        document.body.classList.toggle('dark-theme', theme === 'dark');

        // 更新主题切换按钮
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
    }

    saveTheme(theme) {
        localStorage.setItem('nanobanana-theme', theme);
    }

    loadTheme() {
        return localStorage.getItem('nanobanana-theme') ||
               (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    }

    // 图片处理
    setupImageHandling() {
        // 懒加载图片
        if (CONFIG.performance.lazyLoad) {
            this.setupLazyLoading();
        }

        // 图片错误处理
        document.querySelectorAll('img').forEach(img => {
            img.addEventListener('error', () => {
                img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBmaWxsPSIjRjVGNUY1Ii8+CjxwYXRoIGQ9Ik0yMCAxNkMxNy4yIDE2IDE1IDE4LjIgMTUgMjFDMTUgMjMuOCAxNy4yIDI2IDIwIDI2QzIyLjggMjYgMjUgMjMuOCAyNSAyMUMyNSAxOC4yIDIyLjggMTYgMjAgMTZaIiBmaWxsPSIjQzNDNUMzIi8+CjxwYXRoIGQ9Ik04IDMySDE2VjI4SDhWMzJaIiBmaWxsPSIjQzNDNUMzIi8+CjxwYXRoIGQ9Ik0yNCAzMkgzMlYyOEgyNFYzMloiIGZpbGw9IiNDM0M1QzMiLz4KPC9zdmc+';
                img.classList.add('error-image');
            });
        });

        // 图片缩放功能
        this.setupImageZoom();
    }

    setupLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');

        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        } else {
            // 降级处理
            images.forEach(img => {
                img.src = img.dataset.src;
            });
        }
    }

    setupImageZoom() {
        const zoomableImages = document.querySelectorAll('.zoomable-image');

        zoomableImages.forEach(img => {
            img.addEventListener('click', () => {
                this.openImageModal(img);
            });
        });
    }

    openImageModal(img) {
        const modal = document.createElement('div');
        modal.className = 'image-modal';
        modal.innerHTML = `
            <div class="modal-backdrop"></div>
            <div class="modal-content">
                <img src="${img.src}" alt="${img.alt}">
                <button class="modal-close">&times;</button>
            </div>
        `;

        document.body.appendChild(modal);

        // 关闭模态框
        const close = () => {
            modal.classList.add('closing');
            setTimeout(() => modal.remove(), 300);
        };

        modal.querySelector('.modal-close').addEventListener('click', close);
        modal.querySelector('.modal-backdrop').addEventListener('click', close);

        // ESC 键关闭
        const escHandler = (e) => {
            if (e.key === 'Escape') {
                close();
                document.removeEventListener('keydown', escHandler);
            }
        };
        document.addEventListener('keydown', escHandler);
    }

    // 交互功能
    setupInteractions() {
        // 标签页切换
        this.setupTabs();

        // 复制功能
        this.setupCopyToClipboard();

        // 搜索功能
        this.setupSearch();

        // 工具提示
        this.setupTooltips();
    }

    setupTabs() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetId = button.getAttribute('data-target') ||
                               button.getAttribute('data-category');

                // 移除所有活动状态
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));

                // 添加活动状态
                button.classList.add('active');
                const targetContent = document.getElementById(targetId);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            });
        });
    }

    setupCopyToClipboard() {
        const copyButtons = document.querySelectorAll('[data-copy]');

        copyButtons.forEach(button => {
            button.addEventListener('click', async () => {
                const text = button.getAttribute('data-copy');

                try {
                    await navigator.clipboard.writeText(text);
                    this.showCopyFeedback(button);
                } catch (err) {
                    // 降级方法
                    this.fallbackCopyToClipboard(text);
                    this.showCopyFeedback(button);
                }
            });
        });
    }

    fallbackCopyToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            document.execCommand('copy');
        } catch (err) {
            console.error('Fallback: Oops, unable to copy', err);
        }

        document.body.removeChild(textArea);
    }

    showCopyFeedback(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> 已复制!';
        button.classList.add('copied');

        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('copied');
        }, 2000);
    }

    setupSearch() {
        const searchInput = document.querySelector('[data-search]');
        if (!searchInput) return;

        const searchHandler = utils.debounce((e) => {
            const query = e.target.value.toLowerCase();
            this.performSearch(query);
        }, CONFIG.performance.debounceDelay);

        searchInput.addEventListener('input', searchHandler);
    }

    performSearch(query) {
        const searchableElements = document.querySelectorAll('[data-searchable]');
        let visibleCount = 0;

        searchableElements.forEach(element => {
            const text = element.textContent.toLowerCase();
            const isMatch = text.includes(query);

            if (isMatch) {
                element.style.display = '';
                element.classList.remove('search-hidden');
                visibleCount++;
            } else {
                element.style.display = 'none';
                element.classList.add('search-hidden');
            }
        });

        // 显示搜索结果统计
        this.updateSearchResults(visibleCount, query);
    }

    updateSearchResults(count, query) {
        const resultsElement = document.querySelector('[data-search-results]');
        if (resultsElement) {
            if (query) {
                resultsElement.textContent = `找到 ${count} 个结果`;
                resultsElement.style.display = 'block';
            } else {
                resultsElement.style.display = 'none';
            }
        }
    }

    setupTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');

        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                this.showTooltip(e.target);
            });

            element.addEventListener('mouseleave', (e) => {
                this.hideTooltip(e.target);
            });
        });
    }

    showTooltip(element) {
        const text = element.getAttribute('data-tooltip');
        if (!text) return;

        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip-popup';
        tooltip.textContent = text;
        document.body.appendChild(tooltip);

        const rect = element.getBoundingClientRect();
        tooltip.style.left = `${rect.left + rect.width / 2}px`;
        tooltip.style.top = `${rect.top - 10}px`;

        // 触发重排以应用过渡效果
        requestAnimationFrame(() => {
            tooltip.classList.add('visible');
        });
    }

    hideTooltip(element) {
        const tooltip = document.querySelector('.tooltip-popup');
        if (tooltip) {
            tooltip.classList.remove('visible');
            setTimeout(() => tooltip.remove(), 200);
        }
    }

    // 滚动动画
    updateScrollAnimations() {
        const animatedElements = document.querySelectorAll('[data-scroll-animate]');

        animatedElements.forEach(element => {
            if (utils.isElementInViewport(element)) {
                const animation = element.dataset.scrollAnimate;
                element.classList.add(animation);
            }
        });
    }

    // 性能优化
    setupPerformanceOptimizations() {
        // 预加载关键资源
        this.preloadCriticalResources();

        // 错误监控
        this.setupErrorMonitoring();

        // 性能监控
        this.setupPerformanceMonitoring();
    }

    preloadCriticalResources() {
        const criticalImages = document.querySelectorAll('[data-critical]');
        criticalImages.forEach(img => {
            if (img.dataset.src) {
                img.src = img.dataset.src;
            }
        });
    }

    setupErrorMonitoring() {
        window.addEventListener('error', (e) => {
            console.error('JavaScript error:', e.error);
            // 可以发送错误报告到分析服务
        });

        window.addEventListener('unhandledrejection', (e) => {
            console.error('Unhandled promise rejection:', e.reason);
        });
    }

    setupPerformanceMonitoring() {
        // 监控页面加载性能
        window.addEventListener('load', () => {
            if ('performance' in window) {
                const timing = performance.timing;
                const loadTime = timing.loadEventEnd - timing.navigationStart;
                console.log(`Page load time: ${loadTime}ms`);
            }
        });
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    window.nanobananaApp = new NanoBananaApp();
    console.log('🎨 Nano Banana Pro 提示词整理网站已加载完成!');
});

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// 标签页切换
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetCategory = this.getAttribute('data-category');

            // 移除所有活动状态
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // 添加活动状态到当前选中的标签
            this.classList.add('active');
            const targetContent = document.getElementById(targetCategory);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
});

// 滚动时的导航栏效果
window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    } else {
        header.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
    }
});

// 图片懒加载
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
});

// 添加滚动动画
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeIn 0.6s ease-in-out';
            entry.target.style.opacity = '1';
        }
    });
}, observerOptions);

// 观察需要动画的元素
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.feature-card, .example-card, .tip-card, .resource-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
});

// 复制提示词功能
document.addEventListener('DOMContentLoaded', function() {
    const copyButtons = document.querySelectorAll('.copy-prompt');

    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const promptText = this.getAttribute('data-prompt');
            navigator.clipboard.writeText(promptText).then(() => {
                // 临时更改按钮文本
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> 已复制!';
                this.classList.add('copied');

                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                console.error('复制失败:', err);
            });
        });
    });
});

// 搜索功能（可选）
function searchPrompts(query) {
    const examples = document.querySelectorAll('.example-card');
    const searchQuery = query.toLowerCase();

    examples.forEach(example => {
        const title = example.querySelector('.example-title').textContent.toLowerCase();
        const description = example.querySelector('.example-description').textContent.toLowerCase();
        const prompt = example.querySelector('.prompt-text').textContent.toLowerCase();

        if (title.includes(searchQuery) ||
            description.includes(searchQuery) ||
            prompt.includes(searchQuery)) {
            example.style.display = 'block';
        } else {
            example.style.display = 'none';
        }
    });
}

// 统计功能（可选）
function trackView(element) {
    // 这里可以添加分析代码
    console.log('Viewed:', element);
}

// 错误处理
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
});

// 性能优化
document.addEventListener('DOMContentLoaded', function() {
    // 预加载关键图片
    const criticalImages = document.querySelectorAll('.hero-image img, .feature-icon img');
    criticalImages.forEach(img => {
        if (img.dataset.src) {
            img.src = img.dataset.src;
        }
    });
});

// 主题切换功能（可选）
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
}

// 加载保存的主题
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
});

console.log('Nano Banana Pro 提示词整理网站已加载完成!');