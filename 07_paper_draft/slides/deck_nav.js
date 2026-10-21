(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var deck=document.getElementById('deck'), notes=document.getElementById('notes');
  var i=Math.max(0,Math.min(slides.length-1,(parseInt(location.hash.slice(1),10)||1)-1));
  function fit(){
    var s=Math.min(innerWidth/1920,innerHeight/1080);
    deck.style.transform='translate('+((innerWidth-1920*s)/2)+'px,'+((innerHeight-1080*s)/2)+'px) scale('+s+')';
  }
  function show(n){
    i=Math.max(0,Math.min(slides.length-1,n));
    slides.forEach(function(el,k){el.classList.toggle('active',k===i)});
    var a=slides[i].querySelector('.notes');
    notes.innerHTML='<div class="h">GHI CHÚ NGƯỜI NÓI · TỜ '+(i+1)+' / '+slides.length+'</div>'+(a?a.innerHTML:'');
    history.replaceState(null,'','#'+(i+1));
  }
  addEventListener('keydown',function(e){
    if(e.metaKey||e.ctrlKey||e.altKey)return;
    var k=e.key;
    if(k==='ArrowRight'||k===' '||k==='PageDown'){show(i+1);e.preventDefault()}
    else if(k==='ArrowLeft'||k==='PageUp'){show(i-1);e.preventDefault()}
    else if(k==='Home'){show(0)}
    else if(k==='End'){show(slides.length-1)}
    else if(k==='n'||k==='N'){notes.classList.toggle('on')}
    else if(k==='f'||k==='F'){
      if(document.fullscreenElement)document.exitFullscreen();
      else document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen();
    }
  });
  addEventListener('resize',fit);
  fit();show(i);
})();
