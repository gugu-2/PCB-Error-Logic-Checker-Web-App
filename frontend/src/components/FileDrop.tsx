
import React, { useCallback, useState } from 'react'

export default function FileDrop({ onFiles }: { onFiles: (files: File[]) => void }) {
  const [hover, setHover] = useState(false)
  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files)
    onFiles(files)
    setHover(false)
  }, [onFiles])

  return (
    <div
      onDragOver={(e)=>{e.preventDefault(); setHover(true)}}
      onDragLeave={()=>setHover(false)}
      onDrop={onDrop}
      style={{border:'2px dashed #bbb', padding:24, borderRadius:12, textAlign:'center', background:hover?'#f9f9f9':'#fff'}}>
      <p><b>Drag & drop</b> Gerbers / netlists here, or
        <label style={{ color:'#2563eb', cursor:'pointer', marginLeft:6 }}>
          browse<input type="file" multiple style={{ display:'none' }} onChange={(e)=> onFiles(Array.from(e.target.files||[]))} />
        </label>
      </p>
    </div>
  )
}
