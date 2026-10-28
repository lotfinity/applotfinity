"""One-time targeted energy-use fix for the original minified 3D scene.

The original bundle includes Three.js, GSAP and a full-window shader. Its
unbounded requestAnimationFrame renderer is expensive even on idle mobile tabs.
This small, exact-match patch keeps scene initialization, animation and mouse /
scroll effects, while limiting resolution, frame rate and idle GPU usage.

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
        'this.renderer=new gd({antialias:!("ontouchstart"in document.documentElement),alpha:!0}),this.renderer.setPixelRatio(Math.min(window.devicePixelRatio,"ontouchstart"in document.documentElement?.6:.85))',
    ),
    (
        'this.init(),this.animate()',
        'this.init(),this._lastInput=performance.now(),this._lastDraw=0,this._sleeping=!1,this._tick=this.animate.bind(this),this._idleWake=0,((t)=>{["pointermove","wheel","touchstart","touchmove","keydown"].forEach((e)=>window.addEventListener(e,()=>{t._lastInput=performance.now(),t._sleeping&&!document.hidden&&(clearTimeout(t._idleWake),t._sleeping=!1,t._tick())},{passive:!0})),document.addEventListener("visibilitychange",()=>{document.hidden||(t._lastInput=performance.now())})})(this),this.animate()',
    ),
    (
        '{key:"animate",value:function(){var t=this.clock.getElapsedTime();requestAnimationFrame(this.animate.bind(this)),this.mesh.rotation.x=.01*t,"ontouchstart"in document.documentElement?this.renderMobile():this.render()}}',
        '{key:"animate",value:function(){var t=performance.now(),e="ontouchstart"in document.documentElement;if(document.hidden||t-this._lastInput>3800||((window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches||navigator.connection&&navigator.connection.saveData)&&this._lastDraw))return this._sleeping=!0,void(this._idleWake=setTimeout(this._tick,800));t-this._lastDraw>=(e?180:80)&&(this._lastDraw=t,this.mesh.rotation.x=.01*this.clock.getElapsedTime(),e?this.renderMobile():this.render()),requestAnimationFrame(this._tick)}}',
    ),
]
for old, new in patches:
    count = body.count(old)
    if count != 1:
        raise RuntimeError(f'Expected exactly one matching WebGL patch point, got {count}: {old[:75]}')
    body = body.replace(old, new, 1)
SRC.write_text(body)
print('WebGL scene now respects idle/battery limits: desktop <=12.5 FPS, touch <=5.6 FPS, idle after 3.8s, paused in hidden tabs.')
