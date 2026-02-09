---
<div class="code-output">
  <div class="code">
    
```js
const scale = [0, 2, 4, 7, 9]
Array.from({ length: 16 }, (_, i) =>
  scale[i % scale.length]
)
```
  </div>


  <div class="output">
    <pre>[0, 2, 4, 7, 9, 0, 2, 4, 7, 9, …]</pre>
  </div>
</div>