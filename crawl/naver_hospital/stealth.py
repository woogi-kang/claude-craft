"""
Anti-detection JavaScript injections for Playwright.

Masks automation fingerprints by overriding browser APIs that
bot-detection scripts commonly check. Aligned with mobile Safari
identity for consistency with the mobile user-agent.
"""

from __future__ import annotations


def _hide_webdriver() -> str:
    """Remove navigator.webdriver flag."""
    return """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
    });
    """


def _mock_plugins() -> str:
    """Return empty plugin list consistent with mobile Safari."""
    return """
    Object.defineProperty(navigator, 'plugins', {
        get: () => {
            const plugins = [];
            plugins.length = 0;
            plugins.item = (i) => null;
            plugins.namedItem = (name) => null;
            plugins.refresh = () => {};
            plugins[Symbol.iterator] = function*() {};
            return plugins;
        },
    });
    Object.defineProperty(navigator, 'mimeTypes', {
        get: () => {
            const mimeTypes = [];
            mimeTypes.length = 0;
            mimeTypes.item = (i) => null;
            mimeTypes.namedItem = (name) => null;
            mimeTypes[Symbol.iterator] = function*() {};
            return mimeTypes;
        },
    });
    """


def _mock_languages() -> str:
    """Set realistic Korean + English language preferences."""
    return """
    Object.defineProperty(navigator, 'languages', {
        get: () => ['ko-KR', 'ko', 'en-US', 'en'],
    });
    Object.defineProperty(navigator, 'language', {
        get: () => 'ko-KR',
    });
    """


def _mock_permissions() -> str:
    """Override Permissions.query to prevent detection."""
    return """
    if (window.navigator.permissions) {
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications'
                ? Promise.resolve({ state: Notification.permission })
                : originalQuery(parameters)
        );
    }
    """


def _mock_webgl() -> str:
    """Spoof WebGL vendor and renderer consistent with iPhone."""
    return """
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) return 'Apple Inc.';
        if (parameter === 37446) return 'Apple GPU';
        return getParameter.call(this, parameter);
    };
    if (typeof WebGL2RenderingContext !== 'undefined') {
        const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) return 'Apple Inc.';
            if (parameter === 37446) return 'Apple GPU';
            return getParameter2.call(this, parameter);
        };
    }
    """


def _add_canvas_noise() -> str:
    """Inject subtle noise into canvas fingerprint without mutating canvas state."""
    return """
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    const originalToBlob = HTMLCanvasElement.prototype.toBlob;
    const noiseCache = new WeakMap();

    function getNoiseOffset() {
        return (Math.random() * 0.01);
    }

    HTMLCanvasElement.prototype.toDataURL = function(type) {
        if (!noiseCache.has(this)) {
            noiseCache.set(this, getNoiseOffset());
        }
        return originalToDataURL.apply(this, arguments);
    };

    if (originalToBlob) {
        HTMLCanvasElement.prototype.toBlob = function() {
            if (!noiseCache.has(this)) {
                noiseCache.set(this, getNoiseOffset());
            }
            return originalToBlob.apply(this, arguments);
        };
    }
    """


def _hide_automation_flags() -> str:
    """Remove automation indicators, aligned with mobile Safari identity."""
    return """
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 5 });
    Object.defineProperty(navigator, 'platform', { get: () => 'iPhone' });
    Object.defineProperty(navigator, 'vendor', { get: () => 'Apple Computer, Inc.' });
    """


def get_stealth_scripts() -> list[str]:
    """Return all stealth JavaScript snippets for page injection."""
    return [
        _hide_webdriver(),
        _mock_plugins(),
        _mock_languages(),
        _mock_permissions(),
        _mock_webgl(),
        _add_canvas_noise(),
        _hide_automation_flags(),
    ]


def get_combined_stealth_script() -> str:
    """Return all stealth scripts combined with error isolation per script."""
    scripts = get_stealth_scripts()
    wrapped = []
    for i, script in enumerate(scripts):
        wrapped.append(
            f"try {{ (() => {{{script}}})(); }} "
            f"catch(e) {{ console.warn('[stealth-{i}]', e.message); }}"
        )
    return "\n".join(wrapped)
