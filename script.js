document.addEventListener('DOMContentLoaded', function() {
  
  // ===============================
  // Dark Mode Toggle
  // ===============================
  (function initTheme() {
    const toggle = document.getElementById('theme-toggle');
    if (!toggle) return;
    
    // Check localStorage or system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme) {
      document.documentElement.setAttribute('data-theme', savedTheme);
    } else if (systemPrefersDark) {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
    
    toggle.addEventListener('click', function() {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      
      if (newTheme === 'light') {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
      } else {
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
      }
    });
  })();
  
  
  // ===============================
  // Scroll Animation (IntersectionObserver)
  // ===============================
  (function initScrollAnimation() {
    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1
    };
    
    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);
    
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach(function(el) {
      observer.observe(el);
    });
  })();
  
  
  // ===============================
  // Blog list — load from posts/index.json or posts/index-zh.json
  // ===============================
  (function initBlogList() {
    const list = document.getElementById('blog-list');
    if (!list) return;

    // Determine path prefix (posts are one level deeper)
    const isPost = window.location.pathname.includes('/posts/');
    const prefix = isPost ? '../' : '';

    var path = window.location.pathname;
    var isZh = path.indexOf('index-zh.html') !== -1 || /-zh\.html$/i.test(path);
    var indexName = isZh ? 'posts/index-zh.json' : 'posts/index.json';
    var emptyMsg = isZh ? '敬請期待…' : 'Coming soon...';

    fetch(prefix + indexName)
      .then(function(r) { return r.json(); })
      .then(function(posts) {
        if (!posts.length) {
          list.innerHTML = '<p style="color: var(--text-secondary);">' + emptyMsg + '</p>';
          return;
        }
        list.innerHTML = posts.map(function(p) {
          return '<a href="' + prefix + p.url + '" class="note-item">'
            + '<span class="note-date">' + p.date + '</span>'
            + '<span class="note-title">' + p.title + '</span>'
            + '</a>';
        }).join('');
      })
      .catch(function() {
        list.innerHTML = '<p style="color: var(--text-secondary);">' + emptyMsg + '</p>';
      });
  })();


  // ===============================
  // Active nav link based on current page
  // ===============================
  (function initNavLinks() {
    var path = window.location.pathname;
    var file = path.split('/').pop();
    if (!file || file === '') file = 'index.html';

    var isZhContext = file === 'index-zh.html' || (/-zh\.html$/i.test(file));

    document.querySelectorAll('.nav-link').forEach(function(link) {
      var href = link.getAttribute('href');
      link.classList.remove('active');

      var targetsZh = href.indexOf('index-zh') !== -1;
      var targetsEn = href === 'index.html' || href.slice(-10) === 'index.html';

      if (isZhContext && targetsZh) {
        link.classList.add('active');
      } else if (!isZhContext && file === 'index.html' && targetsEn) {
        link.classList.add('active');
      }
    });
  })();
  
});