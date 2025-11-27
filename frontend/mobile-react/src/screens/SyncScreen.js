import React, {useState} from "react";
import {uploadSync, listUnsynced} from "../api/syncService";

export default function SyncScreen(){
  const [status,setStatus]=useState("");
  const [count,setCount]=useState(0);

  const doSync = async ()=>{
    setStatus("Syncing...");
    try {
      const res = await uploadSync();
      const l = await listUnsynced();
      setCount(l.length);
      setStatus("Sync done");
    } catch (err) {
      setStatus("Sync failed: " + (err.message || ""));
    }
  };

  return (
    <div style={{padding:12, background:"#fff", borderRadius:8, boxShadow:"0 2px 6px rgba(0,0,0,.05)"}}>
      <h3>Manual Sync</h3>
      <button onClick={doSync}>Sync Now</button>
      <div>{status} — Unsynced items left: {count}</div>
    </div>
  );
}
