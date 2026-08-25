µµimport json

import streamlit as st
from streamlit.components.v1 import html

from PATHS import NAVBAR_PATHS, SETTINGS


CSS_FILE = 'src/assets/styles.css'


def inject_custom_css():
    with open(CSS_FILE, encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def navbar_component():
    # NB: on utilise des <span> (pas des <a href>) pour les liens de nav.
    # Streamlit intercepte les clics sur les vraies balises <a> internes pour
    # gerer sa propre navigation, ce qui bloquait ces liens. Un element non-
    # anchor + navigation geree entierement en JS contourne le probleme.
    navbar_items = ''.join(
        f'<li><span class="navitem" data-path="/{value}" data-href="/?nav=%2F{value}" '
        f'role="link" tabindex="0">{key}</span></li>'
        for key, value in NAVBAR_PATHS.items()
    )

    mobile_items = ''.join(
        f'<span class="mobile-navitem" data-path="/{value}" data-href="/?nav=%2F{value}" '
        f'role="link" tabindex="0">{key}</span>'
        for key, value in NAVBAR_PATHS.items()
    )

    settings_items = ''.join(
        f'<span data-href="/?nav={value}" class="settingsNav" role="link" tabindex="0">{key}</span>'
        for key, value in SETTINGS.items()
    )

    nav_html = f'''
    <div class="navbar-wrap" id="navbar-wrap-root">
        <nav class="navbar" id="navbar">
            <div class="nav-container">
                <div class="brand">
                    <span data-href="/?nav=%2Fhome" class="brand-link" role="link" tabindex="0">🚗 Accidents FR</span>
                </div>

                <ul class="navlist">
                    {navbar_items}
                </ul>

                <div class="nav-actions">
                    <button class="hamburger" id="hamburgerBtn" aria-label="Menu" type="button">
                        <span id="hb1"></span>
                        <span id="hb2"></span>
                        <span id="hb3"></span>
                    </button>

                    <div class="dropdown" id="settingsDropDown">
                        <div class="dropbtn" aria-label="Paramètres">⚙</div>
                        <div id="myDropdown" class="dropdown-content">
                            {settings_items}
                        </div>
                    </div>
                </div>
            </div>

            <div class="mobile-menu" id="mobileMenu">
                {mobile_items}
            </div>
        </nav>
    </div>
    '''

    nav_html_js = json.dumps(nav_html)

    component = f"""
    <script>
    (function() {{
        const doc = window.parent.document;
        const win = window.parent;

        function mountNavbar() {{
            const existing = doc.getElementById('navbar-wrap-root');
            if (existing) existing.remove();

            const wrapper = doc.createElement('div');
            wrapper.innerHTML = {nav_html_js};
            doc.body.insertBefore(wrapper, doc.body.firstChild);
        }}

        mountNavbar();

        const navbarWrap = doc.getElementById('navbar-wrap-root');
        const navbar = doc.getElementById('navbar');
        const btn = doc.getElementById('hamburgerBtn');
        const menu = doc.getElementById('mobileMenu');
        const hb1 = doc.getElementById('hb1');
        const hb2 = doc.getElementById('hb2');
        const hb3 = doc.getElementById('hb3');
        const dropdown = doc.getElementById('settingsDropDown');
        const dropdownWindow = doc.getElementById('myDropdown');

        let isOpen = false;
        let dropdownOpen = false;
        let ticking = false;
        let lastScrollY = 0;

        function getPossibleScrollElements() {{
            const els = [
                win,
                doc,
                doc.documentElement,
                doc.body,
                doc.scrollingElement,
                doc.querySelector('[data-testid="stAppViewContainer"]'),
                doc.querySelector('.stAppViewContainer'),
                doc.querySelector('[data-testid="stMain"]'),
                doc.querySelector('section.main'),
                doc.querySelector('.main')
            ].filter(Boolean);

            return [...new Set(els)];
        }}

        function getScrollTop() {{
            const candidates = [
                doc.querySelector('[data-testid="stAppViewContainer"]'),
                doc.querySelector('.stAppViewContainer'),
                doc.querySelector('[data-testid="stMain"]'),
                doc.querySelector('section.main'),
                doc.scrollingElement,
                doc.documentElement,
                doc.body
            ].filter(Boolean);

            for (const el of candidates) {{
                if (typeof el.scrollTop === 'number' && el.scrollTop > 0) {{
                    return el.scrollTop;
                }}
            }}

            return win.pageYOffset || doc.documentElement.scrollTop || doc.body.scrollTop || 0;
        }}

        function closeMobileMenu() {{
            if (!menu) return;
            isOpen = false;
            menu.classList.remove('open');
            if (hb1) hb1.style.transform = '';
            if (hb2) hb2.style.opacity = '1';
            if (hb3) hb3.style.transform = '';
        }}

        function openMobileMenu() {{
            if (!menu) return;
            isOpen = true;
            menu.classList.add('open');
            if (hb1) hb1.style.transform = 'translateY(8px) rotate(45deg)';
            if (hb2) hb2.style.opacity = '0';
            if (hb3) hb3.style.transform = 'translateY(-8px) rotate(-45deg)';
        }}

        function closeDropdown() {{
            if (!dropdownWindow) return;
            dropdownOpen = false;
            dropdownWindow.classList.remove('open');
        }}

        function openDropdown() {{
            if (!dropdownWindow) return;
            dropdownOpen = true;
            dropdownWindow.classList.add('open');
        }}

        function setActiveLink() {{
            const params = new URLSearchParams(win.location.search);
            const nav = params.get('nav') || '/home';

            doc.querySelectorAll('.navitem, .mobile-navitem').forEach(function(link) {{
                const path = link.getAttribute('data-path');
                if (path === nav) {{
                    link.classList.add('active');
                }} else {{
                    link.classList.remove('active');
                }}
            }});
        }}

        setActiveLink();

        console.log('[navbar-debug] mount OK, links found:',
            doc.querySelectorAll('.navitem, .mobile-navitem, .settingsNav, .brand-link').length);

        doc.querySelectorAll('.navitem, .mobile-navitem, .settingsNav, .brand-link').forEach(function(el) {{
            function goTo() {{
                const target = el.getAttribute('data-href');
                console.log('[navbar-debug] goTo() called, target =', target);
                closeMobileMenu();
                closeDropdown();
                win.location.href = target;
                console.log('[navbar-debug] win.location.href assigned');
            }}
            el.addEventListener('click', function(e) {{
                console.log('[navbar-debug] click event fired on', el.className, el.textContent.trim());
                e.stopPropagation();
                goTo();
            }});
            // Ce ne sont plus des <a>, donc on garde le clavier accessible
            // (Entree / Espace) puisque le role="link" ne l'active pas nativement.
            el.addEventListener('keydown', function(e) {{
                if (e.key === 'Enter' || e.key === ' ') {{
                    e.preventDefault();
                    goTo();
                }}
            }});
        }});

        if (btn && menu) {{
            btn.onclick = function(e) {{
                e.stopPropagation();
                closeDropdown();
                if (isOpen) {{
                    closeMobileMenu();
                }} else {{
                    openMobileMenu();
                }}
            }};
        }}

        if (dropdown && dropdownWindow) {{
            dropdown.onclick = function(e) {{
                e.stopPropagation();
                closeMobileMenu();
                if (dropdownOpen) {{
                    closeDropdown();
                }} else {{
                    openDropdown();
                }}
            }};
        }}

        doc.addEventListener('click', function(e) {{
            if (isOpen && btn && menu && !btn.contains(e.target) && !menu.contains(e.target)) {{
                closeMobileMenu();
            }}

            if (dropdownOpen && dropdown && dropdownWindow &&
                !dropdown.contains(e.target) && !dropdownWindow.contains(e.target)) {{
                closeDropdown();
            }}
        }});

        function handleNavbarOnScroll() {{
            if (!navbarWrap) return;

            const currentScrollY = getScrollTop();

            if (currentScrollY <= 20) {{
                navbarWrap.classList.remove('nav-hidden');
                navbarWrap.classList.remove('nav-scrolled');
                if (navbar) navbar.classList.remove('nav-compact');
            }} else {{
                navbarWrap.classList.add('nav-scrolled');
                if (navbar) navbar.classList.add('nav-compact');

                if (!isOpen && !dropdownOpen) {{
                    if (currentScrollY > lastScrollY + 8) {{
                        navbarWrap.classList.add('nav-hidden');
                    }} else if (currentScrollY < lastScrollY - 8) {{
                        navbarWrap.classList.remove('nav-hidden');
                    }}
                }}
            }}

            lastScrollY = currentScrollY;
            ticking = false;
        }}

        function onScroll() {{
            if (!ticking) {{
                win.requestAnimationFrame(handleNavbarOnScroll);
                ticking = true;
            }}
        }}

        lastScrollY = getScrollTop();

        getPossibleScrollElements().forEach(function(el) {{
            el.addEventListener('scroll', onScroll, {{ passive: true }});
        }});

        win.addEventListener('resize', function() {{
            if (win.innerWidth > 768) {{
                closeMobileMenu();
            }}
            handleNavbarOnScroll();
        }});

        setInterval(handleNavbarOnScroll, 300);
        handleNavbarOnScroll();
    }})();
    </script>
    """

    html(component, height=0)