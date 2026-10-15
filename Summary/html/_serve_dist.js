const http=require('http'),fs=require('fs'),p=require('path');
const D=p.join(__dirname,'dist');
http.createServer((q,s)=>{
  let f=q.url.split('?')[0]; if(f==='/') f='/index.html';
  fs.readFile(p.join(D,f),(e,d)=>{
    if(e){s.writeHead(404);s.end('404:'+f);return;}
    const ct=f.endsWith('.js')?'text/javascript':f.endsWith('.css')?'text/css':'text/html; charset=utf-8';
    s.writeHead(200,{'Content-Type':ct});s.end(d);
  });
}).listen(8793,()=>console.log('up 8793'));
