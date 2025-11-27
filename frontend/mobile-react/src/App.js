import React, { useEffect, useState } from "react";
import Login from "./screens/Login";
import Home from "./screens/Home";
import { uploadSync, listUnsynced } from "./api/syncService";
import "./testApi";

function App(){
  const [token,setToken] = useState(localStorage.getItem("token"));
  const [unsyncedCount,setUnsyncedCount] = useState(0);

  useEffect(()=>{
    const check = async ()=>{
      const l = await listUnsynced();
      setUnsyncedCount(l.length);
    }
    check();
  },[]);

  // auto sync when app gains online
  useEffect(()=>{
    const handler = async ()=> {
      if (navigator.onLine) {
        await uploadSync();
        const l = await listUnsynced();
        setUnsyncedCount(l.length);
      }
    };
    window.addEventListener("online", handler);
    return ()=> window.removeEventListener("online", handler);
  },[]);

  if (!token) return <Login onLogin={(t)=>{ setToken(t); localStorage.setItem("token", t); }} />;
  return <Home token={token} unsyncedCount={unsyncedCount} />;
}

export default App;
