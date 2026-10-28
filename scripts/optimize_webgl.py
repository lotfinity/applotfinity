"""One-time targeted energy-use fix for the original minified 3D scene.

The original bundle includes Three.js, GSAP and a full-window shader. Its
unbounded requestAnimationFrame renderer is expensive even on idle mobile tabs.
This small, exact-match patch keeps scene initialization, animation and mouse /
scroll effects, while reducing mesh complexity and idle GPU usage, without sacrificing interaction smoothness.

Re-run only against the *original* minified bundle. It intentionally fails if
its inputs change or if the patch has already been applied; do not silently
re-patch an incompatible future JS bundle. Never add this script as a runtime
browser dependency: the edited main.js is the normal browser asset.
"""
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / 'website/static/js/main.js'
body = SRC.read_text()
patches = [
    (
        'this.renderer=new gd({antialias:!0,alpha:!0}),this.renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.5))',
        'this.renderer=new gd({antialias:!0,alpha:!0}),this.renderer.setPixelRatio(Math.min(window.devicePixelRatio,"ontouchstart"in document.documentElement?1.15:1.25))',
    ),
    (
        'new xd(1,32)',
        'new xd(1,"ontouchstart"in document.documentElement?12:16)',
    ),
    (
        'this.init(),this.animate()',
        'this.init(),this._lastInput=performance.now(),this._lastDraw=0,this._sleeping=!1,this._tick=this.animate.bind(this),this._idleWake=0,((t)=>{["pointermove","wheel","touchstart","touchmove","keydown"].forEach((e)=>window.addEventListener(e,()=>{t._lastInput=performance.now(),t._sleeping&&!document.hidden&&(clearTimeout(t._idleWake),t._sleeping=!1,t._tick())},{passive:!0})),document.addEventListener("visibilitychange",()=>{document.hidden||(t._lastInput=performance.now())})})(this),this.animate()',
    ),
    (
        '{key:"animate",value:function(){var t=this.clock.getElapsedTime();requestAnimationFrame(this.animate.bind(this)),this.mesh.rotation.x=.01*t,"ontouchstart"in document.documentElement?this.renderMobile():this.render()}}',
        '{key:"animate",value:function(){var t=performance.now(),e="ontouchstart"in document.documentElement;if(document.hidden||t-this._lastInput>6500||((window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches||navigator.connection&&navigator.connection.saveData)&&this._lastDraw))return this._sleeping=!0,void(this._idleWake=setTimeout(this._tick,800));t-this._lastDraw>=(e?22:16)&&(this._lastDraw=t,this.mesh.rotation.x=.01*this.clock.getElapsedTime(),e?this.renderMobile():this.render()),requestAnimationFrame(this._tick)}}',
    ),
]
for old, new in patches:
    count = body.count(old)
    if count != 1:
        raise RuntimeError(f'Expected exactly one matching WebGL patch point, got {count}: {old[:75]}')
    body = body.replace(old, new, 1)
SRC.write_text(body)
print('WebGL energy optimization: 60 FPS desktop / 45 FPS touch targets, 3.8–6.5x less geometry, idle after 6.5s.')
