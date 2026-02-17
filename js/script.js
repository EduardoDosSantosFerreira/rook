// script.js - Versão Ultra-Otimizada com Efeitos Premium

(function() {
    'use strict';

    // ===== CONFIGURAÇÕES GLOBAIS =====
    const CONFIG = {
        smoothScroll: true,
        magneticStrength: 0.3,
        tiltMax: 15,
        particleCount: 3000,
        cursorEnabled: true,
        debug: false
    };

    // ===== UTILITIES =====
    const Util = {
        lerp: (start, end, factor) => start + (end - start) * factor,
        clamp: (num, min, max) => Math.min(Math.max(num, min), max),
        map: (num, inMin, inMax, outMin, outMax) => 
            (num - inMin) * (outMax - outMin) / (inMax - inMin) + outMin,
        debounce: (func, wait) => {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        throttle: (func, limit) => {
            let inThrottle;
            return function(...args) {
                if (!inThrottle) {
                    func.apply(this, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        }
    };

    // ===== LOCOMOTIVE SCROLL INIT =====
    class SmoothScroll {
        constructor() {
            this.scroll = null;
            this.init();
        }

        init() {
            if (!CONFIG.smoothScroll) return;

            const scrollContainer = document.querySelector('[data-scroll-container]');
            if (!scrollContainer) return;

            this.scroll = new LocomotiveScroll({
                el: scrollContainer,
                smooth: true,
                multiplier: 0.8,
                lerp: 0.08,
                smartphone: { smooth: true },
                tablet: { smooth: true },
                reloadOnContextChange: true,
                touchMultiplier: 2,
                inertia: 0.8
            });

            this.setupGSAP();
        }

        setupGSAP() {
            gsap.registerPlugin(ScrollTrigger);

            this.scroll.on('scroll', ScrollTrigger.update);

            ScrollTrigger.scrollerProxy('[data-scroll-container]', {
                scrollTop: value => {
                    if (arguments.length) {
                        this.scroll.scrollTo(value, 0, 0);
                    }
                    return this.scroll.scroll.instance.scroll.y;
                },
                getBoundingClientRect: () => ({
                    top: 0,
                    left: 0,
                    width: window.innerWidth,
                    height: window.innerHeight
                }),
                pinType: document.querySelector('[data-scroll-container]').style.transform 
                    ? 'transform' : 'fixed'
            });

            ScrollTrigger.addEventListener('refresh', () => this.scroll.update());
            ScrollTrigger.refresh();
        }

        scrollTo(target) {
            if (this.scroll) {
                this.scroll.scrollTo(target, {
                    offset: -50,
                    duration: 1.2,
                    easing: [0.25, 0.0, 0.35, 1.0]
                });
            }
        }
    }

    // ===== CURSOR PERSONALIZADO AVANÇADO =====
    class CustomCursor {
        constructor() {
            this.cursor = document.querySelector('.cursor');
            this.trail = document.querySelector('.cursor-trail');
            this.pos = { x: 0, y: 0 };
            this.mouse = { x: 0, y: 0 };
            this.speed = 0.15;
            this.trailSpeed = 0.08;
            this.init();
        }

        init() {
            if (!CONFIG.cursorEnabled || !this.cursor || !this.trail) return;

            this.bindEvents();
            this.animate();
        }

        bindEvents() {
            document.addEventListener('mousemove', (e) => {
                this.mouse.x = e.clientX;
                this.mouse.y = e.clientY;
            });

            document.querySelectorAll('a, button, .benefit-card, .feature-item, .tilt-3d')
                .forEach(el => {
                    el.addEventListener('mouseenter', () => {
                        this.cursor.classList.add('hover');
                        this.trail.classList.add('hover');
                    });
                    el.addEventListener('mouseleave', () => {
                        this.cursor.classList.remove('hover');
                        this.trail.classList.remove('hover');
                    });
                });

            document.addEventListener('mousedown', () => {
                this.cursor.classList.add('click');
            });

            document.addEventListener('mouseup', () => {
                this.cursor.classList.remove('click');
            });

            document.addEventListener('mouseleave', () => {
                this.cursor.style.opacity = '0';
                this.trail.style.opacity = '0';
            });

            document.addEventListener('mouseenter', () => {
                this.cursor.style.opacity = '1';
                this.trail.style.opacity = '1';
            });
        }

        animate() {
            this.pos.x = Util.lerp(this.pos.x, this.mouse.x, this.speed);
            this.pos.y = Util.lerp(this.pos.y, this.mouse.y, this.speed);

            gsap.set(this.cursor, {
                x: this.pos.x - 10,
                y: this.pos.y - 10,
                rotation: gsap.utils.mapRange(0, window.innerWidth, -10, 10, this.mouse.x)
            });

            gsap.set(this.trail, {
                x: this.mouse.x - 20,
                y: this.mouse.y - 20,
                scale: 1 + (Math.abs(this.mouse.x - this.pos.x) * 0.01)
            });

            requestAnimationFrame(() => this.animate());
        }
    }

    // ===== PROGRESS BAR + NAVEGAÇÃO =====
    class NavigationManager {
        constructor() {
            this.progressBar = document.getElementById('progressBar');
            this.sections = document.querySelectorAll('section[id]');
            this.navLinks = document.querySelectorAll('.nav-link');
            this.currentSection = '';
            this.isScrolling = false;
            this.scrollTimeout = null;
            this.init();
        }

        init() {
            this.updateProgress();
            this.setupScrollSpy();
            this.setupSmoothScroll();
            this.setupNavHighlight();
        }

        updateProgress() {
            if (!this.progressBar) return;

            const update = Util.throttle(() => {
                const winScroll = window.scrollY;
                const height = document.documentElement.scrollHeight - window.innerHeight;
                const scrolled = (winScroll / height) * 100;
                
                gsap.to(this.progressBar, {
                    width: scrolled + '%',
                    duration: 0.2,
                    ease: 'power1.out'
                });

                // Efeito de glow baseado no progresso
                this.progressBar.style.boxShadow = `0 0 ${10 + scrolled * 0.5}px rgba(81, 109, 219, ${0.3 + scrolled * 0.005})`;
            }, 50);

            window.addEventListener('scroll', update);
            window.addEventListener('resize', update);
        }

        setupScrollSpy() {
            const observerOptions = {
                root: null,
                rootMargin: '-20% 0px -35% 0px',
                threshold: [0, 0.25, 0.5, 0.75, 1]
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.currentSection = entry.target.id;
                        this.updateActiveNav();
                        
                        // Efeito de glow na seção ativa
                        entry.target.style.transition = 'box-shadow 0.5s ease';
                        entry.target.style.boxShadow = '0 0 30px rgba(81, 109, 219, 0.1)';
                        
                        setTimeout(() => {
                            entry.target.style.boxShadow = 'none';
                        }, 500);
                    }
                });
            }, observerOptions);

            this.sections.forEach(section => observer.observe(section));
        }

        setupSmoothScroll() {
            this.navLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const targetId = link.getAttribute('href').substring(1);
                    const targetSection = document.getElementById(targetId);
                    
                    if (targetSection) {
                        this.isScrolling = true;
                        
                        // Animação de clique
                        link.style.transform = 'scale(0.95)';
                        setTimeout(() => link.style.transform = '', 200);

                        window.scrollTo({
                            top: targetSection.offsetTop - 80,
                            behavior: 'smooth'
                        });

                        clearTimeout(this.scrollTimeout);
                        this.scrollTimeout = setTimeout(() => {
                            this.isScrolling = false;
                        }, 1000);
                    }
                });
            });
        }

        setupNavHighlight() {
            // Efeito de underline animado
            this.navLinks.forEach(link => {
                const underline = document.createElement('span');
                underline.classList.add('nav-underline');
                link.appendChild(underline);

                link.addEventListener('mouseenter', () => {
                    gsap.to(underline, {
                        width: '100%',
                        duration: 0.3,
                        ease: 'power2.out'
                    });
                });

                link.addEventListener('mouseleave', () => {
                    if (!link.classList.contains('active')) {
                        gsap.to(underline, {
                            width: '0%',
                            duration: 0.3,
                            ease: 'power2.out'
                        });
                    }
                });
            });
        }

        updateActiveNav() {
            if (this.isScrolling) return;

            this.navLinks.forEach(link => {
                const href = link.getAttribute('href').substring(1);
                const isActive = href === this.currentSection;
                
                link.classList.toggle('active', isActive);
                
                const underline = link.querySelector('.nav-underline');
                if (underline) {
                    gsap.to(underline, {
                        width: isActive ? '100%' : '0%',
                        duration: 0.3,
                        ease: 'power2.out'
                    });
                }
            });
        }
    }

    // ===== MAGNETIC BUTTONS OTIMIZADO =====
    class MagneticButtons {
        constructor() {
            this.buttons = document.querySelectorAll('.magnetic-btn');
            this.init();
        }

        init() {
            this.buttons.forEach(btn => {
                let bound = btn.getBoundingClientRect();
                
                btn.addEventListener('mouseenter', () => {
                    bound = btn.getBoundingClientRect();
                });

                btn.addEventListener('mousemove', (e) => {
                    const x = e.clientX - bound.left - bound.width / 2;
                    const y = e.clientY - bound.top - bound.height / 2;
                    
                    const distance = Math.sqrt(x * x + y * y);
                    const maxDistance = 100;
                    const strength = Util.map(Math.min(distance, maxDistance), 0, maxDistance, 1, 0);
                    
                    gsap.to(btn, {
                        x: x * CONFIG.magneticStrength * strength,
                        y: y * CONFIG.magneticStrength * strength,
                        scale: 1.05,
                        duration: 0.4,
                        ease: 'power2.out',
                        overwrite: true
                    });
                });

                btn.addEventListener('mouseleave', () => {
                    gsap.to(btn, {
                        x: 0,
                        y: 0,
                        scale: 1,
                        duration: 0.6,
                        ease: 'elastic.out(1, 0.3)',
                        overwrite: true
                    });
                });
            });
        }
    }

    // ===== 3D TILT CARDS AVANÇADO =====
    class TiltCards {
        constructor() {
            this.cards = document.querySelectorAll('.tilt-3d, .tilt-card');
            this.init();
        }

        init() {
            this.cards.forEach(card => {
                let rect = card.getBoundingClientRect();
                
                card.addEventListener('mouseenter', () => {
                    rect = card.getBoundingClientRect();
                    card.style.transition = 'none';
                });

                card.addEventListener('mousemove', (e) => {
                    const x = (e.clientX - rect.left) / rect.width - 0.5;
                    const y = (e.clientY - rect.top) / rect.height - 0.5;
                    
                    const rotateY = x * CONFIG.tiltMax;
                    const rotateX = -y * CONFIG.tiltMax;
                    
                    // Efeito de profundidade baseado na posição do mouse
                    const shadowX = x * 20;
                    const shadowY = y * 20;
                    
                    gsap.to(card, {
                        rotateY: rotateY,
                        rotateX: rotateX,
                        boxShadow: `${shadowX}px ${shadowY}px 30px rgba(81, 109, 219, 0.3)`,
                        duration: 0.3,
                        ease: 'power2.out',
                        overwrite: 'auto'
                    });

                    // Efeito de brilho especular
                    const glare = card.querySelector('.card-glow') || this.createGlare(card);
                    if (glare) {
                        gsap.to(glare, {
                            background: `radial-gradient(circle at ${x * 100 + 50}% ${y * 100 + 50}%, rgba(255,255,255,0.2), transparent 70%)`,
                            duration: 0.3
                        });
                    }
                });

                card.addEventListener('mouseleave', () => {
                    gsap.to(card, {
                        rotateY: 0,
                        rotateX: 0,
                        boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
                        duration: 0.5,
                        ease: 'power2.out'
                    });

                    const glare = card.querySelector('.card-glow');
                    if (glare) {
                        gsap.to(glare, {
                            background: 'none',
                            duration: 0.3
                        });
                    }
                });
            });
        }

        createGlare(card) {
            const glare = document.createElement('div');
            glare.classList.add('card-glow');
            glare.style.cssText = `
                position: absolute;
                inset: 0;
                pointer-events: none;
                z-index: 2;
                border-radius: inherit;
            `;
            card.appendChild(glare);
            return glare;
        }
    }

    // ===== TEXT SPLIT ANIMATION =====
    class TextSplitter {
        constructor() {
            this.elements = document.querySelectorAll('.split-text, .split-text-reveal');
            this.init();
        }

        init() {
            this.elements.forEach(el => {
                const text = el.textContent;
                const chars = text.split('');
                
                el.innerHTML = '';
                
                chars.forEach((char, i) => {
                    const span = document.createElement('span');
                    span.textContent = char === ' ' ? '\u00A0' : char;
                    span.style.cssText = `
                        display: inline-block;
                        opacity: 0;
                        transform: translateY(20px);
                        transition: opacity 0.4s ease, transform 0.4s ease;
                        transition-delay: ${i * 0.02}s;
                    `;
                    el.appendChild(span);
                });
            });
        }

        reveal(element) {
            const spans = element.querySelectorAll('span');
            spans.forEach(span => {
                span.style.opacity = '1';
                span.style.transform = 'translateY(0)';
            });
        }
    }

    // ===== SCROLL REVEAL OTIMIZADO =====
    class ScrollReveal {
        constructor() {
            this.elements = document.querySelectorAll('.reveal');
            this.textSplitter = new TextSplitter();
            this.init();
        }

        init() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.revealElement(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.15,
                rootMargin: '0px 0px -50px 0px'
            });

            this.elements.forEach(el => observer.observe(el));
        }

        revealElement(el) {
            // Animação principal
            gsap.to(el, {
                opacity: 1,
                y: 0,
                duration: 0.8,
                ease: 'power2.out',
                delay: parseFloat(el.dataset.delay) || 0
            });

            // Reveal de textos divididos
            const splitTexts = el.querySelectorAll('.split-text, .split-text-reveal');
            splitTexts.forEach(text => {
                const spans = text.querySelectorAll('span');
                gsap.to(spans, {
                    opacity: 1,
                    y: 0,
                    duration: 0.5,
                    stagger: 0.02,
                    delay: 0.2,
                    ease: 'power2.out'
                });
            });

            // Animar contadores
            const counters = el.querySelectorAll('.stat-number');
            counters.forEach(counter => this.animateCounter(counter));
        }

        animateCounter(element) {
            const target = parseInt(element.getAttribute('data-target'));
            const suffix = element.nextElementSibling?.textContent || '';
            let current = 0;
            
            gsap.to({ val: 0 }, {
                val: target,
                duration: 2,
                ease: 'power2.out',
                onUpdate: function() {
                    element.textContent = Math.floor(this.targets()[0].val);
                }
            });
        }
    }

    // ===== THREE.JS PARTICLE BACKGROUND AVANÇADO =====
    class ParticleBackground {
        constructor() {
            this.canvas = document.getElementById('particleCanvas');
            if (!this.canvas) return;
            
            this.scene = null;
            this.camera = null;
            this.renderer = null;
            this.particles = null;
            this.mouse = { x: 0, y: 0 };
            
            this.init();
        }

        init() {
            this.setupScene();
            this.setupParticles();
            this.setupLights();
            this.bindEvents();
            this.animate();
        }

        setupScene() {
            this.scene = new THREE.Scene();
            this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            this.renderer = new THREE.WebGLRenderer({ 
                canvas: this.canvas, 
                alpha: true,
                antialias: true,
                powerPreference: "high-performance"
            });
            
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            
            this.camera.position.z = 8;
        }

        setupParticles() {
            const geometry = new THREE.BufferGeometry();
            const count = CONFIG.particleCount;
            
            const positions = new Float32Array(count * 3);
            const colors = new Float32Array(count * 3);
            const sizes = new Float32Array(count);

            const color1 = new THREE.Color(0x516DDB);
            const color2 = new THREE.Color(0x8E51DB);
            const color3 = new THREE.Color(0xBC51DB);

            for (let i = 0; i < count; i++) {
                // Posições em esfera
                const r = 5 + Math.random() * 3;
                const theta = Math.random() * Math.PI * 2;
                const phi = Math.acos(2 * Math.random() - 1);
                
                positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
                positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
                positions[i * 3 + 2] = r * Math.cos(phi);

                // Cores aleatórias
                const color = Math.random() < 0.33 ? color1 : Math.random() < 0.5 ? color2 : color3;
                colors[i * 3] = color.r;
                colors[i * 3 + 1] = color.g;
                colors[i * 3 + 2] = color.b;

                // Tamanhos variados
                sizes[i] = Math.random() * 0.05 + 0.02;
            }

            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
            geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

            const material = new THREE.PointsMaterial({
                size: 0.05,
                vertexColors: true,
                transparent: true,
                opacity: 0.6,
                blending: THREE.AdditiveBlending,
                sizeAttenuation: true
            });

            this.particles = new THREE.Points(geometry, material);
            this.scene.add(this.particles);
        }

        setupLights() {
            const ambientLight = new THREE.AmbientLight(0x404060);
            this.scene.add(ambientLight);
        }

        bindEvents() {
            document.addEventListener('mousemove', (e) => {
                this.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
                this.mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
            });

            window.addEventListener('resize', Util.debounce(() => {
                this.camera.aspect = window.innerWidth / window.innerHeight;
                this.camera.updateProjectionMatrix();
                this.renderer.setSize(window.innerWidth, window.innerHeight);
            }, 250));
        }

        animate() {
            requestAnimationFrame(() => this.animate());

            if (this.particles) {
                // Rotação baseada no mouse
                this.particles.rotation.y += 0.0005 + this.mouse.x * 0.0002;
                this.particles.rotation.x += 0.0002 + this.mouse.y * 0.0001;
                
                // Efeito de pulsação
                const time = Date.now() * 0.001;
                this.particles.material.opacity = 0.5 + Math.sin(time) * 0.1;
            }

            this.renderer.render(this.scene, this.camera);
        }
    }

    // ===== FLOATING CTA INTELIGENTE =====
    class FloatingCTA {
        constructor() {
            this.cta = document.querySelector('.floating-cta');
            this.lastScrollY = 0;
            this.isVisible = false;
            this.init();
        }

        init() {
            if (!this.cta) return;

            window.addEventListener('scroll', Util.throttle(() => {
                const scrollY = window.scrollY;
                const docHeight = document.documentElement.scrollHeight - window.innerHeight;
                const scrollPercent = (scrollY / docHeight) * 100;

                // Mostrar apenas entre 20% e 80% do scroll
                if (scrollPercent > 20 && scrollPercent < 80) {
                    if (!this.isVisible) {
                        this.show();
                    }
                } else {
                    if (this.isVisible) {
                        this.hide();
                    }
                }

                this.lastScrollY = scrollY;
            }, 100));
        }

        show() {
            this.isVisible = true;
            gsap.to(this.cta, {
                opacity: 1,
                y: 0,
                duration: 0.5,
                ease: 'power2.out'
            });
        }

        hide() {
            this.isVisible = false;
            gsap.to(this.cta, {
                opacity: 0,
                y: 20,
                duration: 0.5,
                ease: 'power2.out'
            });
        }
    }

    // ===== RIPPLE EFFECT =====
    class RippleEffect {
        constructor() {
            this.buttons = document.querySelectorAll('.btn-primary, .btn-cta');
            this.init();
        }

        init() {
            this.buttons.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const ripple = document.createElement('span');
                    ripple.classList.add('ripple');
                    
                    const rect = btn.getBoundingClientRect();
                    const size = Math.max(rect.width, rect.height);
                    
                    ripple.style.cssText = `
                        position: absolute;
                        width: ${size}px;
                        height: ${size}px;
                        left: ${e.clientX - rect.left - size / 2}px;
                        top: ${e.clientY - rect.top - size / 2}px;
                        background: radial-gradient(circle, rgba(255,255,255,0.6) 0%, rgba(255,255,255,0) 70%);
                        border-radius: 50%;
                        pointer-events: none;
                        transform: scale(0);
                        animation: rippleExpand 0.6s ease-out forwards;
                    `;
                    
                    btn.style.position = 'relative';
                    btn.style.overflow = 'hidden';
                    btn.appendChild(ripple);
                    
                    setTimeout(() => ripple.remove(), 700);
                });
            });
        }
    }

    // ===== DYNAMIC SHADOWS =====
    class DynamicShadows {
        constructor() {
            this.elements = document.querySelectorAll('.dynamic-shadow');
            this.init();
        }

        init() {
            this.elements.forEach(el => {
                el.addEventListener('mousemove', (e) => {
                    const rect = el.getBoundingClientRect();
                    const x = (e.clientX - rect.left) / rect.width - 0.5;
                    const y = (e.clientY - rect.top) / rect.height - 0.5;
                    
                    el.style.setProperty('--shadow-x', x * 20 + 'px');
                    el.style.setProperty('--shadow-y', y * 20 + 'px');
                    el.style.setProperty('--shadow-blur', (30 + Math.abs(x * 20)) + 'px');
                });
            });
        }
    }

    // ===== PARALLAX LAYERS =====
    class ParallaxLayers {
        constructor() {
            this.layers = document.querySelectorAll('.parallax-layer');
            this.init();
        }

        init() {
            window.addEventListener('scroll', Util.throttle(() => {
                const scrollY = window.scrollY;
                
                this.layers.forEach(layer => {
                    const speed = parseFloat(layer.dataset.speed) || 0.1;
                    const y = scrollY * speed;
                    
                    gsap.to(layer, {
                        y: y,
                        duration: 0.3,
                        ease: 'power1.out'
                    });
                });
            }, 16));
        }
    }

    // ===== ANIMATED UNDERLINE =====
    class AnimatedUnderline {
        constructor() {
            this.links = document.querySelectorAll('.animated-underline');
            this.init();
        }

        init() {
            this.links.forEach(link => {
                const underline = document.createElement('span');
                underline.classList.add('underline-effect');
                underline.style.cssText = `
                    position: absolute;
                    bottom: -2px;
                    left: 50%;
                    width: 0;
                    height: 2px;
                    background: linear-gradient(90deg, var(--accent-1), var(--accent-5));
                    transition: width 0.3s ease, left 0.3s ease;
                `;
                
                link.style.position = 'relative';
                link.appendChild(underline);

                link.addEventListener('mouseenter', () => {
                    underline.style.width = '100%';
                    underline.style.left = '0';
                });

                link.addEventListener('mouseleave', () => {
                    underline.style.width = '0';
                    underline.style.left = '50%';
                });
            });
        }
    }

    // ===== MORPHING MENU =====
    class MorphingMenu {
        constructor() {
            this.btn = document.querySelector('.mobile-menu-btn');
            this.menu = document.querySelector('.morphing-menu');
            this.isOpen = false;
            this.init();
        }

        init() {
            if (!this.btn || !this.menu) return;

            this.btn.addEventListener('click', () => {
                this.isOpen = !this.isOpen;
                
                if (this.isOpen) {
                    this.open();
                } else {
                    this.close();
                }
            });

            // Fechar ao clicar em links
            this.menu.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', () => this.close());
            });
        }

        open() {
            gsap.to(this.menu, {
                clipPath: 'circle(150% at 100% 0%)',
                duration: 0.6,
                ease: 'power2.inOut'
            });
            
            gsap.to(this.btn, {
                rotate: 90,
                duration: 0.3,
                ease: 'power2.out'
            });
        }

        close() {
            gsap.to(this.menu, {
                clipPath: 'circle(0% at 100% 0%)',
                duration: 0.6,
                ease: 'power2.inOut'
            });
            
            gsap.to(this.btn, {
                rotate: 0,
                duration: 0.3,
                ease: 'power2.out'
            });

            this.isOpen = false;
        }
    }

    // ===== INICIALIZAÇÃO PRINCIPAL =====
    document.addEventListener('DOMContentLoaded', () => {
        // Adicionar estilos dinâmicos
        const style = document.createElement('style');
        style.textContent = `
            @keyframes rippleExpand {
                0% { transform: scale(0); opacity: 0.5; }
                100% { transform: scale(4); opacity: 0; }
            }
            
            .nav-underline {
                position: absolute;
                bottom: -4px;
                left: 0;
                width: 0;
                height: 2px;
                background: linear-gradient(90deg, var(--accent-1), var(--accent-5));
                transition: width 0.3s ease;
            }
            
            .nav-link.active {
                color: var(--text-primary);
            }
            
            .cursor.hover {
                transform: scale(1.5);
                background: rgba(81, 109, 219, 0.2);
            }
            
            .cursor-trail.hover {
                transform: scale(1.2);
            }
            
            .cursor.click {
                transform: scale(0.8);
            }
            
            @media (max-width: 768px) {
                .cursor, .cursor-trail {
                    display: none;
                }
            }
        `;
        document.head.appendChild(style);

        // Inicializar todos os módulos
        const smoothScroll = new SmoothScroll();
        const cursor = new CustomCursor();
        const navigation = new NavigationManager();
        const magnetic = new MagneticButtons();
        const tiltCards = new TiltCards();
        const scrollReveal = new ScrollReveal();
        const particles = new ParticleBackground();
        const floatingCTA = new FloatingCTA();
        const ripple = new RippleEffect();
        const shadows = new DynamicShadows();
        const parallax = new ParallaxLayers();
        const underline = new AnimatedUnderline();
        const morphingMenu = new MorphingMenu();

        // Expor scroll global para debugging
        if (CONFIG.debug) {
            window.scroll = smoothScroll;
        }
    });
})();
// Gráfico animado no mockup
const miniChart = document.getElementById('miniChart');
if (miniChart) {
    const ctx = miniChart.getContext('2d');
    let width = miniChart.width;
    let height = miniChart.height;
    
    function drawChart() {
        ctx.clearRect(0, 0, width, height);
        
        // Dados do gráfico
        const data1 = [20, 35, 25, 45, 30, 50, 40, 55, 35, 48, 42, 38];
        const data2 = [15, 25, 20, 35, 25, 40, 30, 45, 28, 38, 32, 28];
        
        const barWidth = (width - 40) / data1.length;
        
        // Desenhar linhas
        ctx.beginPath();
        ctx.strokeStyle = '#516DDB';
        ctx.lineWidth = 2;
        ctx.shadowColor = '#516DDB';
        ctx.shadowBlur = 10;
        
        for (let i = 0; i < data1.length; i++) {
            const x = 20 + i * barWidth + barWidth / 2;
            const y = height - 20 - (data1[i] / 60) * (height - 40);
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.stroke();
        
        // Desenhar pontos
        ctx.shadowBlur = 15;
        for (let i = 0; i < data1.length; i++) {
            const x = 20 + i * barWidth + barWidth / 2;
            const y = height - 20 - (data1[i] / 60) * (height - 40);
            
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fillStyle = '#516DDB';
            ctx.fill();
        }
        
        // Segunda linha
        ctx.beginPath();
        ctx.strokeStyle = '#BC51DB';
        
        for (let i = 0; i < data2.length; i++) {
            const x = 20 + i * barWidth + barWidth / 2;
            const y = height - 20 - (data2[i] / 60) * (height - 40);
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.stroke();
        
        // Pontos da segunda linha
        for (let i = 0; i < data2.length; i++) {
            const x = 20 + i * barWidth + barWidth / 2;
            const y = height - 20 - (data2[i] / 60) * (height - 40);
            
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fillStyle = '#BC51DB';
            ctx.fill();
        }
        
        requestAnimationFrame(drawChart);
    }
    
    drawChart();
}